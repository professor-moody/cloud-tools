import platform
import os
import json
import argparse
import operator
import sys
import pprint
import traceback
from roadtools.roadlib.metadef.database import ServicePrincipal, User, Group, DirectoryRole, Application, Device, Policy, Base, lnk_policy_user_include, lnk_policy_user_exclude, lnk_policy_user_include_allusers
import roadtools.roadlib.metadef.database as database
from sqlalchemy import and_, or_
from sqlalchemy import bindparam, func, text
from sqlalchemy.dialects.postgresql import insert as pginsert
DESCRIPTION = '''
Analyze Condtional Access policies and determine users in scope
'''

def commitlink(session, cachedict, ignore=False):
    global dburl
    for linktable, cache in cachedict.items():
        if not cache:
            continue
        if 'postgresql' in dburl and ignore:
            insertst = pginsert(linktable)
            statement = insertst.on_conflict_do_nothing(
                index_elements=['objectId']
            )
        elif 'sqlite' in dburl and ignore:
            statement = linktable.insert().prefix_with('OR IGNORE')
        else:
            statement = linktable.insert()
        session.execute(
            statement,
            cache
        )

class PoliciesPlugin():
    def __init__(self, session, printlogs=False):
        # SQLAlchemy session
        self.session = session
        self.printlogs = printlogs

    def _get_group(self, gid):
        if isinstance(gid, list):
            return self.session.query(Group).filter(Group.objectId.in_(gid)).all()
        return self.session.query(Group).filter(Group.objectId == gid).first()

    def _get_application(self, aid):
        if isinstance(aid, list):
            res = self.session.query(Application).filter(Application.appId.in_(aid)).all()
            # if no result, query the ServicePrincipals
            if len(res) != len(aid):
                return self.session.query(ServicePrincipal).filter(ServicePrincipal.appId.in_(aid)).all()
            else:
                return res
        else:
            res = self.session.query(Application).filter(Application.appId == aid).first()
            # if no result, query the ServicePrincipals
            if res is None or len(res) == 0:
                return self.session.query(ServicePrincipal).filter(ServicePrincipal.appId == aid).first()

    def _get_user(self, uid):
        if isinstance(uid, list):
            return self.session.query(User).filter(User.objectId.in_(uid)).all()
        return self.session.query(User).filter(User.objectId == uid).first()

    def _get_guests(self):
        return self.session.query(User).filter(User.userType == 'Guest').all()

    def _get_serviceprincipal(self, uid):
        if isinstance(uid, list):
            return self.session.query(ServicePrincipal).filter(ServicePrincipal.objectId.in_(uid)).all()
        return self.session.query(ServicePrincipal).filter(ServicePrincipal.objectId == uid).first()

    def _get_serviceprincipalrule(self, rule):
        if isinstance(rule, list):
            return [', '.join(rule)]
        return [rule]

    def _get_role(self, rid):
        if isinstance(rid, list):
            return self.session.query(DirectoryRole).filter(DirectoryRole.roleTemplateId.in_(rid)).all()
        return self.session.query(DirectoryRole).filter(DirectoryRole.roleTemplateId == rid).first()

    def _print_object(self, obj):
        if obj is None:
            return
        if isinstance(obj, list):
            for objitem in obj:
                self._print_object(objitem)
        else:
            print('\t  ', end='')
            print(obj.objectId
                  + ': '
                  + obj.displayName
                  , end='')
            try:
                print(' (' + obj.appId + ')', end='')
                print(' (' + obj.objectType+ ')', end='')
            except:
                pass
            print()

    def _translate_guestsexternal(self, value):
        return [value['GuestOrExternalUserTypes'], ]

    def _translate_authstrength(self, authstrengthguid):
        built_in = {
            '00000000-0000-0000-0000-000000000002': 'Multi-factor authentication',
            '00000000-0000-0000-0000-000000000003': 'Passwordless MFA',
            '00000000-0000-0000-0000-000000000004': 'Phishing-resistant MFA'
        }
        try:
            return built_in[authstrengthguid]
        except KeyError:
            return f"Unknown authentication strengh policy: {authstrengthguid} (probably custom)"

    def _add_recursive_groupmembers(self, inscope_uids, groups, processedgroups):
        inscope_uids.extend([uobj.objectId for group in groups for uobj in group.memberUsers])
        # handle subgroups
        for group in groups:
            if group.objectId not in processedgroups:
                processedgroups.add(group.objectId)
                self._add_recursive_groupmembers(inscope_uids, group.memberGroups, processedgroups)

    def _parse_ucrit(self, crit):
        funct = {
            'Applications' : self._get_application,
            'Users' : self._get_user,
            'Groups' : self._get_group,
            'Roles': self._get_role,
            'ServicePrincipals': self._get_serviceprincipal,
            'ServicePrincipalFilterRule': self._get_serviceprincipalrule,
            'GuestsOrExternalUsers': self._translate_guestsexternal,
            'AgenticServicePrincipals': self._get_serviceprincipal
        }
        inscope_uids = []
        for ctype, clist in crit.items():
            # Figure out what this is later, for now solve this breaking the policies parsing
            if ctype == 'IsAgentic':
                continue
            if 'All' in clist:
                return ['ALLUSERS']
            if 'None' in clist:
                return []
            if 'Guests' in clist:
                # Fetch all guests
                inscope_uids = inscope_uids + [guest.objectId for guest in self._get_guests()]
            try:
                objects = funct[ctype](clist)
            except KeyError:
                raise Exception('Unsupported criterium type: {0}'.format(ctype))
            if len(objects) > 0:
                if ctype == 'Users':
                    # maybe move this as we are now resolving objects which we already have the ID of
                    # but this solves the problem with non-existing accounts in scope of policies
                    inscope_uids.extend([uobj.objectId for uobj in objects])
                elif ctype == 'ServicePrincipals':
                    if self.printlogs:
                        print('Skip SP for now')
                elif ctype == 'Groups':
                    processedgroups = set()
                    self._add_recursive_groupmembers(inscope_uids, objects, processedgroups)
                elif ctype == 'Roles':
                    inscope_uids.extend([uobj.objectId for role in objects for uobj in role.memberUsers ])
                elif ctype == 'GuestsOrExternalUsers':
                    if self.printlogs:
                        print('Skip external user types for now')
                elif ctype == 'ServicePrincipalFilterRule':
                    if self.printlogs:
                        print('Skip SP filter for now')
                else:
                    raise Exception('Unsupported criterium type: {0}'.format(ctype))
            else:
                if self.printlogs:
                    print('Unknown object(s) {0}'.format(', '.join(clist)))
                    print('Warning: Not all object IDs could be resolved for this policy')
        return inscope_uids

    def _parse_who(self, cond):
        ucond = cond['Users']
        include = []
        exclude = []
        if len(ucond['Include']) == 1 and 'Nobody' in self._parse_ucrit(ucond['Include'][0]) and 'ServicePrincipals' in cond:
            if self.printlogs:
                print('Skipping SP policy')
        else:
            for icrit in ucond['Include']:
                include += self._parse_ucrit(icrit)

            if 'Exclude' in ucond:
                for icrit in ucond['Exclude']:
                    exclude += self._parse_ucrit(icrit)
        return include, exclude

    @staticmethod
    def parse_wrapper(func, conditions, policy):
        """
        Wrapper to handle failures in parsing policy body better
        """
        try:
            return func(conditions)
        except Exception as exc:
            print(f'Error parsing condition in policy {policy.displayName}')
            traceback.print_exc()
            return 'Error in parsing: ' + str(exc)

    def main(self):
        alluser_policies = []
        for policy in self.session.query(Policy).filter(Policy.policyType == 18).order_by(Policy.displayName):
            detail = json.loads(policy.policyDetail[0])
            # pprint.pprint(detail)
            try:
                conditions = detail['Conditions']
            except KeyError:
                conditions = None
            if conditions is None:
                if self.printlogs:
                    print('Invalid policy - no conditions')
                continue
            includeusers, excludeusers =  self.parse_wrapper(self._parse_who, conditions, policy)
            # print(f"Included: {includeusers}")
            # print(f"Excluded: {excludeusers}")
            if 'ALLUSERS' in includeusers:
                alluser_policies.append(policy.objectId)
                includeusers = []
            cache = {
                lnk_policy_user_include: [{'Policy':policy.objectId, 'User':uid} for uid in includeusers],
                lnk_policy_user_exclude: [{'Policy':policy.objectId, 'User':uid} for uid in excludeusers],
            }
            commitlink(self.session, cache, True)
        cache = {
            lnk_policy_user_include_allusers: [{'Policy':policy} for policy in alluser_policies]
        }
        commitlink(self.session, cache, True)
        self.session.commit()

def add_args(parser):
    pass

def main(args=None):
    global dburl
    if args is None:
        parser = argparse.ArgumentParser(add_help=True, description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('-d',
                            '--database',
                            action='store',
                            help='Database file. Can be the local database name for SQLite, or an SQLAlchemy compatible URL such as postgresql+psycopg2://dirkjan@/roadtools',
                            default='roadrecon.db')
        add_args(parser)
        args = parser.parse_args()
    dburl = database.parse_db_argument(args.database)
    engine = database.init(dburl=dburl)
    Base.metadata.create_all(engine)
    session = database.get_session(engine)
    plugin = PoliciesPlugin(session, printlogs=True)
    plugin.main()

if __name__ == '__main__':
    main()
