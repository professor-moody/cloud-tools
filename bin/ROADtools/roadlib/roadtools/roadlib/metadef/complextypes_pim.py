from roadtools.roadlib.metadef.basetypes import Edm, Collection
import enum

PIMFeatureScope_data = {

}
PIMFeatureScope = enum.Enum('PIMFeatureScope', PIMFeatureScope_data)


PIMFeatureState_data = {

}
PIMFeatureState = enum.Enum('PIMFeatureState', PIMFeatureState_data)


class PIMgovernancePermission(object):
    props = {
        'accessLevel': Edm.String,
        'isActive': Edm.Boolean,
        'isEligible': Edm.Boolean,
    }


class PIMgovernanceSchedule(object):
    props = {
        'type': Edm.String,
        'startDateTime': Edm.DateTimeOffset,
        'endDateTime': Edm.DateTimeOffset,
        'duration': Edm.Duration,
    }


class PIMtriggeredByTarget(object):
    props = {
        'id': Edm.String,
        'type': Edm.String,
        'subType': Edm.String,
    }


class PIMKeyValuePair_2OfString_String(object):
    props = {
        'key': Edm.String,
        'value': Edm.String,
    }


class PIMKeyValue(object):
    props = {
        'key': Edm.String,
        'value': Edm.String,
    }


class PIMgovernanceRuleSetting(object):
    props = {
        'ruleIdentifier': Edm.String,
        'setting': Edm.String,
    }


class PIMgovernanceRoleAssignmentRequestStatus(object):
    props = {
        'status': Edm.String,
        'subStatus': Edm.String,
        'statusDetails': Collection,
    }


class PIMmetadata(object):
    props = {

    }


class PIMKeyValueList(object):
    props = {
        'item': Collection,
    }


class PIMgovernanceLifeCycleManagementSetting(object):
    props = {
        'caller': Edm.String,
        'operation': Edm.String,
        'level': Edm.String,
        'value': Collection,
    }

