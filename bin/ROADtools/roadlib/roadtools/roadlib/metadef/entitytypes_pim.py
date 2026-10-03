from roadtools.roadlib.metadef.basetypes import Edm, Collection
from roadtools.roadlib.metadef.complextypes_pim import *

class PIMtenant(object):
    props = {
        'id': Edm.String,
        'initialDomainName': Edm.String,
        'displayName': Edm.String,
        'status': Edm.String,
        'additionalInformation': Edm.String,
    }
    rels = [

    ]


class PIMprivilegedFeatureFlight(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'settings': Edm.String,
        'scope': PIMFeatureScope,
        'state': PIMFeatureState,
        'createdDate': Edm.DateTimeOffset,
        'updatedDate': Edm.DateTimeOffset,
    }
    rels = [

    ]


class PIMprivilegedAccess(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
    }
    rels = [
        'registration',
        'resources',
        'roleDefinitions',
        'roleAssignments',
        'roleAssignmentRequests',
        'roleSettings',
        'roleSettingsV2',
        'alerts',
        'activities',
    ]


class PIMgovernanceResource(object):
    props = {
        'id': Edm.String,
        'externalId': Edm.String,
        'type': Edm.String,
        'displayName': Edm.String,
        'status': Edm.String,
        'onboardDateTime': Edm.DateTimeOffset,
        'registeredDateTime': Edm.DateTimeOffset,
        'managedAt': Edm.String,
        'registeredRoot': Edm.String,
        'originTenantId': Edm.String,
    }
    rels = [
        'parent',
        'roleDefinitions',
        'roleAssignments',
        'roleAssignmentRequests',
        'roleSettings',
        'alerts',
    ]


class PIMgovernanceSubject(object):
    props = {
        'id': Edm.String,
        'type': Edm.String,
        'displayName': Edm.String,
        'principalName': Edm.String,
        'email': Edm.String,
    }
    rels = [

    ]


class PIMgovernanceAlert(object):
    props = {
        'id': Edm.String,
        'resourceId': Edm.String,
        'alertName': Edm.String,
        'alertDescription': Edm.String,
        'numberOfAffectedItems': Edm.Int32,
        'additionalData': Collection,
        'lastModifiedDateTime': Edm.DateTimeOffset,
        'lastScannedDateTime': Edm.DateTimeOffset,
        'severityLevel': Edm.String,
        'alertType': Edm.String,
        'securityImpact': Edm.String,
        'mitigationSteps': Edm.String,
        'howToPrevent': Edm.String,
        'isDisabled': Edm.Boolean,
        'isActive': Edm.Boolean,
        'isResolvable': Edm.Boolean,
        'isConfigurable': Edm.Boolean,
        'status': Edm.String,
        'settings': Collection,
    }
    rels = [

    ]


class PIMgovernanceRoleDefinition(object):
    props = {
        'id': Edm.String,
        'resourceId': Edm.String,
        'externalId': Edm.String,
        'templateId': Edm.String,
        'displayName': Edm.String,
        'type': Edm.String,
    }
    rels = [
        'resource',
        'roleSetting',
    ]


class PIMgovernanceRoleAssignment(object):
    props = {
        'id': Edm.String,
        'resourceId': Edm.String,
        'roleDefinitionId': Edm.String,
        'subjectId': Edm.String,
        'scopedResourceId': Edm.String,
        'linkedEligibleRoleAssignmentId': Edm.String,
        'externalId': Edm.String,
        'isPermanent': Edm.Boolean,
        'startDateTime': Edm.DateTimeOffset,
        'endDateTime': Edm.DateTimeOffset,
        'memberType': Edm.String,
        'assignmentState': Edm.String,
        'status': Edm.String,
        'condition': Edm.String,
        'conditionVersion': Edm.String,
        'conditionDescription': Edm.String,
    }
    rels = [
        'resource',
        'roleDefinition',
        'subject',
        'linkedEligibleRoleAssignment',
        'scopedResource',
    ]


class PIMgovernanceRoleAssignmentRequest(object):
    props = {
        'id': Edm.String,
        'resourceId': Edm.String,
        'roleDefinitionId': Edm.String,
        'subjectId': Edm.String,
        'scopedResourceId': Edm.String,
        'linkedEligibleRoleAssignmentId': Edm.String,
        'type': Edm.String,
        'assignmentState': Edm.String,
        'requestedDateTime': Edm.DateTimeOffset,
        'roleAssignmentStartDateTime': Edm.DateTimeOffset,
        'roleAssignmentEndDateTime': Edm.DateTimeOffset,
        'reason': Edm.String,
        'status': PIMgovernanceRoleAssignmentRequestStatus,
        'schedule': PIMgovernanceSchedule,
        'PIMmetadata': PIMmetadata,
        'ticketNumber': Edm.String,
        'ticketSystem': Edm.String,
        'condition': Edm.String,
        'conditionVersion': Edm.String,
        'conditionDescription': Edm.String,
    }
    rels = [
        'resource',
        'roleDefinition',
        'subject',
        'scopedResource',
    ]


class PIMgovernanceRoleSetting(object):
    props = {
        'id': Edm.String,
        'resourceId': Edm.String,
        'roleDefinitionId': Edm.String,
        'isDefault': Edm.Boolean,
        'lastUpdatedDateTime': Edm.DateTimeOffset,
        'lastUpdatedBy': Edm.String,
        'adminEligibleSettings': Collection,
        'adminMemberSettings': Collection,
        'userEligibleSettings': Collection,
        'userMemberSettings': Collection,
    }
    rels = [
        'roleDefinition',
        'resource',
    ]


class PIMgovernanceRoleSettingV2(object):
    props = {
        'id': Edm.String,
        'resourceId': Edm.String,
        'roleDefinitionId': Edm.String,
        'isDefault': Edm.Boolean,
        'lastUpdatedDateTime': Edm.DateTimeOffset,
        'lastUpdatedBy': Edm.String,
        'lifeCycleManagement': Collection,
    }
    rels = [
        'roleDefinition',
        'resource',
    ]


class PIMgovernanceActivity(object):
    props = {
        'id': Edm.String,
        'correlationId': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
        'expirationDateTime': Edm.DateTimeOffset,
        'operationType': Edm.String,
        'reason': Edm.String,
        'status': Edm.String,
        'ticketNumber': Edm.String,
        'ticketSystem': Edm.String,
        'statusReason': Edm.String,
        'triggeredByTarget': PIMtriggeredByTarget,
    }
    rels = [
        'requestor',
        'originalRequestor',
        'target',
        'subject',
        'resource',
        'scopedResource',
    ]


class PIMgovernanceJob(object):
    props = {
        'id': Edm.String,
        'deliveryTime': Edm.DateTimeOffset,
        'tenantId': Edm.String,
        'providerId': Edm.String,
        'applicationId': Edm.String,
        'metadata': PIMmetadata,
    }
    rels = [
        'requestor',
        'originalRequestor',
    ]


class PIMforkedJob(object):
    props = {
        'id': Edm.String,
        'forkingId': Edm.String,
        'deliveryTime': Edm.DateTimeOffset,
        'tenantId': Edm.String,
        'providerId': Edm.String,
        'applicationId': Edm.String,
        'metadata': Collection,
    }
    rels = [
        'requestor',
        'originalRequestor',
    ]


class PIMtarget(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'uniqueName': Edm.String,
        'objectType': Edm.String,
        'internalType': Edm.String,
    }
    rels = [

    ]

