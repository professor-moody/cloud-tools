from roadtools.roadlib.metadef.basetypes import Edm, Collection
from roadtools.roadlib.metadef.complextypes_ig import *

class IGidentityGovernance(object):
    props = {
        'id': Edm.String,
    }
    rels = [
        'entitlementManagement',
    ]


class IGentitlementManagement(object):
    props = {
        'id': Edm.String,
        'currentUserApproverDelegate': IGapproverDelegate,
    }
    rels = [
        'accessPackageCatalogs',
        'catalogs',
        'accessPackageResources',
        'resources',
        'accessPackageResourceRequests',
        'resourceRequests',
        'accessPackageResourceRoleScopes',
        'resourceRoleScopes',
        'accessPackages',
        'accessPackageAssignmentPolicies',
        'assignmentPolicies',
        'accessPackageAssignments',
        'assignments',
        'accessPackageAssignmentRequests',
        'assignmentRequests',
        'accessPackageAssignmentResourceRoles',
        'settings',
        'connectedOrganizations',
        'accessPackageResourceEnvironments',
        'resourceEnvironments',
        'subjects',
        'controlConfigurations',
    ]


class IGentitlementManagementSettings(object):
    props = {
        'id': Edm.String,
        'externalUserLifecycleAction': Edm.String,
        'daysUntilExternalUserDeletedAfterBlocked': Edm.Int32,
        'durationUntilExternalUserDeletedAfterBlocked': Edm.Duration,
        'optInPreviewFeatures': IGoptInPreviewFeatures,
        'sharePointCentralAdminSite': Edm.String,
    }
    rels = [

    ]


class IGaccessPackageSuggestion(object):
    props = {
        'accessPackageId': Edm.String,
        'id': Edm.String,
        'accessPackageSuggestionReasons': Collection,
        'reasons': Collection,
        'tag': Edm.Int32,
    }
    rels = [
        'accessPackage',
        'availableAccessPackage',
    ]


class IGaccessPackageCatalog(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'uniqueName': Edm.String,
        'description': Edm.String,
        'catalogType': Edm.String,
        'catalogStatus': Edm.String,
        'state': IGaccessPackageCatalogState,
        'isExternallyVisible': Edm.Boolean,
        'createdBy': Edm.String,
        'createdByString': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedBy': Edm.String,
        'lastModifiedByString': Edm.String,
        'modifiedDateTime': Edm.DateTimeOffset,
        'lastModifiedDateTime': Edm.DateTimeOffset,
        'serviceManagementReference': IGserviceManagementReference,
        'privilegeLevel': IGprivilegeLevel,
    }
    rels = [
        'accessPackageResources',
        'resources',
        'accessPackageResourceRoles',
        'resourceRoles',
        'accessPackageResourceScopes',
        'resourceScopes',
        'accessPackages',
        'additionalInfo',
        'customExtensions',
        'customAccessPackageWorkflowExtensions',
        'accessPackageCustomWorkflowExtensions',
        'customWorkflowExtensions',
    ]


class IGbillingConfiguration(object):
    props = {
        'name': Edm.String,
        'resourceId': Edm.String,
        'subscriptionId': Edm.String,
        'resourceGroupName': Edm.String,
        'resourceLocation': Edm.String,
    }
    rels = [
        'subscriptions',
    ]


class IGSubscriptions(object):
    props = {
        'subscriptionId': Edm.String,
    }
    rels = [
        'resourceGroups',
    ]


class IGResourceGroups(object):
    props = {
        'name': Edm.String,
    }
    rels = [
        'providers',
    ]


class IGProviders(object):
    props = {
        'name': Edm.String,
    }
    rels = [
        'guestGovernanceUsage',
    ]


class IGGuestGovernanceUsageResource(object):
    props = {
        'id': Edm.String,
    }
    rels = [

    ]


class IGaccessPackageResource(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'url': Edm.String,
        'resourceType': Edm.String,
        'originId': Edm.String,
        'originSystem': Edm.String,
        'isPendingOnboarding': Edm.Boolean,
        'addedBy': Edm.String,
        'addedOn': Edm.DateTimeOffset,
        'attributes': Collection,
        'createdBy': Edm.String,
        'createdByString': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
    }
    rels = [
        'accessPackageResourceEnvironment',
        'accessPackageResourceScopes',
        'accessPackageResourceRoles',
        'roles',
        'scopes',
        'environment',
        'externalOriginResourceConnector',
    ]


class IGaccessPackageResourceEnvironment(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'originSystem': Edm.String,
        'originId': Edm.String,
        'isDefaultEnvironment': Edm.Boolean,
        'connectionInfo': IGconnectionInfo,
    }
    rels = [
        'accessPackageResources',
    ]


class IGcontrolConfiguration(object):
    props = {
        'id': Edm.String,
        'isEnabled': Edm.Boolean,
        'createdBy': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedBy': Edm.String,
        'modifiedDateTime': Edm.DateTimeOffset,
    }
    rels = [

    ]


class IGaccessPackageResourceRequest(object):
    props = {
        'id': Edm.String,
        'requestType': Edm.String,
        'requestState': Edm.String,
        'state': IGaccessPackageRequestState,
        'requestStatus': Edm.String,
        'createdBy': Edm.String,
        'createdByString': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
        'catalogId': Edm.String,
        'executeImmediately': Edm.Boolean,
        'justification': Edm.String,
        'expirationDateTime': Edm.DateTimeOffset,
        'history': Collection,
        'answers': Collection,
        'parameters': Collection,
    }
    rels = [
        'accessPackageResource',
        'resource',
        'catalog',
        'requestor',
    ]


class IGaccessPackageResourceRoleScope(object):
    props = {
        'id': Edm.String,
        'createdBy': Edm.String,
        'createdByString': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedBy': Edm.String,
        'modifiedDateTime': Edm.DateTimeOffset,
    }
    rels = [
        'accessPackageResourceRole',
        'accessPackageResourceScope',
        'role',
        'scope',
    ]


class IGaccessPackage(object):
    props = {
        'id': Edm.String,
        'catalogId': Edm.String,
        'displayName': Edm.String,
        'uniqueName': Edm.String,
        'description': Edm.String,
        'isHidden': Edm.Boolean,
        'isRoleScopesVisible': Edm.Boolean,
        'createdBy': Edm.String,
        'createdByString': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedBy': Edm.String,
        'lastModifiedByString': Edm.String,
        'modifiedDateTime': Edm.DateTimeOffset,
        'lastModifiedDateTime': Edm.DateTimeOffset,
        'lastCriticalModificationDateTime': Edm.DateTimeOffset,
        'lastSuccessfulChangeEvaluationDateTime': Edm.DateTimeOffset,
    }
    rels = [
        'accessPackageCatalog',
        'catalog',
        'accessPackageResourceRoleScopes',
        'accessPackageAssignmentPolicies',
        'additionalInfo',
        'resourceRoleScopes',
        'assignmentPolicies',
        'incompatibleAccessPackages',
        'accessPackagesIncompatibleWith',
        'incompatibleGroups',
    ]


class IGaccessPackageAssignmentPolicy(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'allowedTargetScope': IGallowedTargetScope,
        'specificAllowedTargets': Collection,
        'expiration': IGexpirationPattern,
        'countOfUsersIncludedInPolicy': Edm.Int32,
        'activeAssignmentCount': Edm.Int32,
        'createdDateTime': Edm.DateTimeOffset,
        'createdByString': Edm.String,
        'accessPackageAssignmentRequestorSettings': IGaccessPackageAssignmentRequestorSettings,
        'automaticRequestSettings': IGaccessPackageAutomaticRequestSettings,
        'lastModifiedByString': Edm.String,
        'approvalSettings': IGaccessPackageAssignmentApprovalSettings,
        'lastModifiedDateTime': Edm.DateTimeOffset,
        'reviewSettings': IGaccessPackageAssignmentReviewSettings,
        'questions': Collection,
        'notificationSettings': IGAccessPackageNotificationSettings,
        'accessPackageNotificationSettings': IGAccessPackageNotificationSettings,
        'verifiableCredentialSettings': IGverifiableCredentialSettings,
        'createdBy': Edm.String,
        'modifiedBy': Edm.String,
        'isDenyPolicy': Edm.Boolean,
        'canExtend': Edm.Boolean,
        'durationInDays': Edm.Int32,
        'expirationDateTime': Edm.DateTimeOffset,
        'isCustomAssignmentScheduleAllowed': Edm.Boolean,
        'policyAssignmentType': Edm.String,
        'requestorSettings': IGrequestorSettings,
        'accessReviewSettings': IGassignmentReviewSettings,
        'assignmentReviewSettings': IGassignmentReviewSettings,
        'requestApprovalSettings': IGapprovalSettings,
        'accessPackageId': Edm.String,
        'modifiedDateTime': Edm.DateTimeOffset,
    }
    rels = [
        'accessPackage',
        'accessPackageCatalog',
        'catalog',
        'customExtensionHandlers',
        'customExtensionStageSettings',
        'additionalInfo',
    ]


class IGaccessPackageAssignment(object):
    props = {
        'id': Edm.String,
        'catalogId': Edm.String,
        'accessPackageId': Edm.String,
        'assignmentPolicyId': Edm.String,
        'targetId': Edm.String,
        'schedule': IGentitlementManagementSchedule,
        'assignmentStatus': Edm.String,
        'assignmentState': Edm.String,
        'state': IGaccessPackageAssignmentState,
        'status': Edm.String,
        'isExtended': Edm.Boolean,
        'expiredDateTime': Edm.DateTimeOffset,
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedDateTime': Edm.DateTimeOffset,
        'history': Collection,
        'customExtensionHandlerInstances': Collection,
        'customExtensionCalloutInstances': Collection,
    }
    rels = [
        'accessPackage',
        'accessPackageAssignmentPolicy',
        'assignmentPolicy',
        'target',
        'accessPackageAssignmentRequests',
        'accessPackageAssignmentResourceRoles',
    ]


class IGaccessPackageAssignmentRequest(object):
    props = {
        'id': Edm.String,
        'requestType': Edm.String,
        'schedule': IGentitlementManagementSchedule,
        'answers': Collection,
        'requestState': Edm.String,
        'state': IGaccessPackageRequestState,
        'requestStatus': Edm.String,
        'status': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedDateTime': Edm.DateTimeOffset,
        'completedDate': Edm.DateTimeOffset,
        'justification': Edm.String,
        'isValidationOnly': Edm.Boolean,
        'history': Collection,
        'parameters': Collection,
        'customProperties': Collection,
        'referenceId': Edm.String,
        'verifiedCredentialsData': Collection,
        'customExtensionHandlerInstances': Collection,
        'customExtensionCalloutInstances': Collection,
    }
    rels = [
        'accessPackage',
        'accessPackageAssignment',
        'requestor',
        'assignment',
        'fulfillmentErrors',
        'approval',
    ]


class IGaccessPackageAssignmentResourceRole(object):
    props = {
        'id': Edm.String,
        'originId': Edm.String,
        'originSystem': Edm.String,
        'status': Edm.String,
    }
    rels = [
        'accessPackageResourceScope',
        'accessPackageResourceRole',
        'accessPackageSubject',
        'accessPackageAssignments',
    ]


class IGentitlementManagementRoleDefinition(object):
    props = {
        'id': Edm.String,
        'name': Edm.String,
        'actions': Collection,
        'scopes': Collection,
    }
    rels = [

    ]


class IGentitlementManagementRoleAssignment(object):
    props = {
        'id': Edm.String,
        'principalType': Edm.String,
        'scope': Edm.String,
        'roleDefinitionId': Edm.String,
        'isInherited': Edm.Boolean,
        'createdBy': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
    }
    rels = [
        'roleDefinition',
        'accessPackageSubject',
    ]


class IGfeature(object):
    props = {
        'isEnabled': Edm.Boolean,
        'id': Edm.String,
        'isEndUserFeature': Edm.Boolean,
    }
    rels = [

    ]


class IGauditEvent(object):
    props = {
        'id': Edm.String,
        'createTime': Edm.DateTimeOffset,
        'expirationTime': Edm.DateTimeOffset,
        'auditCategory': Edm.String,
        'auditType': Edm.String,
        'correlationId': Edm.String,
        'tenantId': Edm.String,
        'operationName': Edm.String,
        'resultType': Edm.String,
        'error': Edm.String,
        'additionalInformation': Edm.String,
    }
    rels = [
        'requestor',
        'targets',
        'primaryTarget',
        'auditableObjectChangeDetails',
    ]


class IGtenant(object):
    props = {
        'id': Edm.String,
        'initialDomainName': Edm.String,
        'displayName': Edm.String,
        'isTestTenant': Edm.Boolean,
        'premiumSku': Edm.String,
        'privacyUrl': Edm.String,
        'brandingLocale': Edm.String,
        'bannerLogoUrl': Edm.String,
        'nextSubjectSync': Edm.DateTimeOffset,
    }
    rels = [

    ]


class IGcheckAccess(object):
    props = {
        'resourceScope': Edm.String,
        'action': Edm.String,
    }
    rels = [

    ]


class IGaccessPackageSubject(object):
    props = {
        'connectedOrganizationId': Edm.String,
        'id': Edm.String,
        'objectId': Edm.String,
        'altSecId': Edm.String,
        'displayName': Edm.String,
        'principalName': Edm.String,
        'email': Edm.String,
        'onPremisesSecurityIdentifier': Edm.String,
        'type': Edm.String,
        'subjectType': IGaccessPackageSubjectType,
        'subjectLifecycle': IGaccessPackageSubjectLifecycle,
        'cleanupScheduledDateTime': Edm.DateTimeOffset,
        'createdDateTime': Edm.DateTimeOffset,
    }
    rels = [
        'tenant',
        'connectedOrganization',
    ]


class IGcustomCalloutExtension(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'endpointConfiguration': IGcustomExtensionEndpointConfiguration,
        'clientConfiguration': IGcustomExtensionClientConfiguration,
        'authenticationConfiguration': IGcustomExtensionAuthenticationConfiguration,
        'callbackConfiguration': IGcustomExtensionCallbackConfiguration,
    }
    rels = [

    ]


class IGcustomAccessPackageWorkflowExtension(IGcustomCalloutExtension):
    props = {
        'responseConfiguration': IGcustomExtensionResponseConfiguration,
        'createdDateTime': Edm.DateTimeOffset,
        'lastModifiedDateTime': Edm.DateTimeOffset,
        'type': Edm.String,
        'isConvertible': Edm.Boolean,
        'convertibleType': Edm.String,
    }
    rels = [
        'accessPackageCatalog',
        'createdBy',
        'lastModifiedBy',
    ]


class IGavailableAccessPackageSummary(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
    }
    rels = [

    ]


class IGavailableAccessPackageDetails(IGavailableAccessPackageSummary):
    props = {

    }
    rels = [
        'accessPackageResourceRoleScopes',
    ]


class IGavailableAccessPackage(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
    }
    rels = [
        'resourceRoleScopes',
        'accessPackageResourceRoleScopes',
    ]


class IGapprovalStep(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'status': Edm.String,
        'assignedToMe': Edm.Boolean,
        'reviewedDateTime': Edm.DateTimeOffset,
        'reviewResult': Edm.String,
        'justification': Edm.String,
    }
    rels = [
        'reviewedBy',
    ]


class IGaccessPackageAssignmentRequestApprovalStep(IGapprovalStep):
    props = {
        'answers': Collection,
    }
    rels = [

    ]


class IGapproval(object):
    props = {
        'id': Edm.String,
        'requestApprovalSettings': IGapprovalSettings,
        'settings': IGaccessPackageAssignmentApprovalSettings,
    }
    rels = [
        'steps',
    ]


class IGexternalOriginResourceConnector(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'connectorType': IGConnectorType,
        'connectionInfo': IGconnectionInfo,
        'createdBy': Edm.String,
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedBy': Edm.String,
        'modifiedDateTime': Edm.DateTimeOffset,
    }
    rels = [

    ]


class IGguestApproval(IGcontrolConfiguration):
    props = {
        'enforcementScope': IGenforcementScope,
        'approvalStage': IGguestApprovalStage,
    }
    rels = [

    ]


class IGinsiderRiskyUserApproval(IGcontrolConfiguration):
    props = {
        'isApprovalRequired': Edm.Boolean,
        'minimumRiskLevel': IGPurviewInsiderRiskManagementLevel,
    }
    rels = [

    ]


class IGentraIdProtectionRiskyUserApproval(IGcontrolConfiguration):
    props = {
        'isApprovalRequired': Edm.Boolean,
        'minimumRiskLevel': IGRiskLevel,
    }
    rels = [

    ]


class IGaccessPackageResourceScope(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'originId': Edm.String,
        'originSystem': Edm.String,
        'roleOriginId': Edm.String,
        'isRootScope': Edm.Boolean,
        'url': Edm.String,
    }
    rels = [
        'accessPackageResource',
        'resource',
    ]


class IGaccessPackageResourceRole(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'roleType': Edm.String,
        'originSystem': Edm.String,
        'originId': Edm.String,
    }
    rels = [
        'accessPackageResource',
        'resource',
    ]


class IGcustomDataProvidedResource(IGaccessPackageResource):
    props = {
        'notificationEndpointConfiguration': IGcustomExtensionEndpointConfiguration,
    }
    rels = [

    ]


class IGaccessPackageCustomManagedResource(IGaccessPackageResource):
    props = {

    }
    rels = [
        'targetResource',
    ]


class IGaccessPackageAssignmentRequestWorkflowExtension(IGcustomCalloutExtension):
    props = {
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedBy': Edm.String,
        'lastModifiedDateTime': Edm.DateTimeOffset,
    }
    rels = [
        'accessPackageCatalog',
        'createdBy',
        'lastModifiedBy',
    ]


class IGaccessPackageAssignmentWorkflowExtension(IGcustomCalloutExtension):
    props = {
        'createdDateTime': Edm.DateTimeOffset,
        'modifiedBy': Edm.String,
        'lastModifiedDateTime': Edm.DateTimeOffset,
    }
    rels = [
        'accessPackageCatalog',
        'createdBy',
        'lastModifiedBy',
    ]


class IGCustomExtensionHandler(object):
    props = {
        'id': Edm.String,
        'stage': IGaccessPackageCustomExtensionStage,
    }
    rels = [
        'customExtension',
    ]


class IGCustomExtensionStageSetting(object):
    props = {
        'id': Edm.String,
        'stage': IGaccessPackageCustomExtensionStage,
    }
    rels = [
        'customExtension',
    ]


class IGassignmentPolicyAdditionalInfo(object):
    props = {
        'assignmentPolicyId': Edm.String,
        'activeAssignmentCount': Edm.Int32,
    }
    rels = [

    ]


class IGaccessPackageAdditionalInfo(object):
    props = {
        'accessPackageId': Edm.String,
        'activeAssignmentCount': Edm.Int32,
        'pendingRequestCount': Edm.Int32,
        'assignmentPolicyCount': Edm.Int32,
        'roleScopeCount': Edm.Int32,
    }
    rels = [

    ]


class IGDirectoryObject(object):
    props = {
        'id': Edm.String,
    }
    rels = [

    ]


class IGgroup(IGDirectoryObject):
    props = {
        'displayName': Edm.String,
        'mail': Edm.String,
    }
    rels = [

    ]


class IGcatalogAdditionalInfo(object):
    props = {
        'catalogId': Edm.String,
        'accessPackageCount': Edm.Int32,
        'resourceCount': Edm.Int32,
    }
    rels = [

    ]


class IGconnectedOrganization(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
    }
    rels = [

    ]


class IGfulfillmentError(object):
    props = {
        'roleName': Edm.String,
        'resourceType': Edm.String,
        'resourceId': Edm.String,
        'resourceName': Edm.String,
        'errorMessage': Edm.String,
        'errorDateTime': Edm.DateTimeOffset,
    }
    rels = [

    ]


class IGendUserSettings(IGcontrolConfiguration):
    props = {
        'isRelatedPeopleSuggestionEnabled': Edm.Boolean,
        'relatedPeopleInsightLevel': IGaccessPackageRelatedPeopleSuggestionInsightLevel,
        'isViewDirectReportsAccessPackageAssignmentsEnabled': Edm.Boolean,
        'showApproverDetailsToMembers': Edm.Boolean,
        'resourcesVisibleTo': IGresourceVisibilityScope,
    }
    rels = [

    ]


class IGapplication(IGDirectoryObject):
    props = {
        'displayName': Edm.String,
    }
    rels = [

    ]


class IGservicePrincipal(IGDirectoryObject):
    props = {
        'displayName': Edm.String,
    }
    rels = [

    ]


class IGuser(IGDirectoryObject):
    props = {
        'displayName': Edm.String,
        'mail': Edm.String,
        'userPrincipalName': Edm.String,
    }
    rels = [

    ]


class IGauditTarget(object):
    props = {
        'id': Edm.String,
        'tenantId': Edm.String,
        'displayName': Edm.String,
        'uniqueName': Edm.String,
        'internalType': Edm.String,
        'objectType': Edm.String,
        'category': Edm.String,
    }
    rels = [
        'changeDetails',
    ]


class IGauditChangeDetail(object):
    props = {
        'propertyName': Edm.String,
        'value': Edm.String,
    }
    rels = [

    ]


class IGauditableObjectChangedDetails(object):
    props = {
        'propertyName': Edm.String,
        'oldValue': Edm.String,
        'newValue': Edm.String,
    }
    rels = [

    ]


class IGroleManagement(object):
    props = {
        'id': Edm.String,
        'entitlementManagement': IGrbacApplication,
    }
    rels = [

    ]


class IGunifiedRoleDefinition(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
        'isBuiltIn': Edm.Boolean,
        'isEnabled': Edm.Boolean,
        'templateId': Edm.String,
        'version': Edm.String,
        'rolePermissions': Collection,
    }
    rels = [

    ]


class IGunifiedRoleAssignment(object):
    props = {
        'id': Edm.String,
        'principalId': Edm.String,
        'roleDefinitionId': Edm.String,
        'directoryScopeId': Edm.String,
        'appScopeId': Edm.String,
    }
    rels = [
        'roleDefinition',
        'principal',
        'directoryScope',
        'appScope',
    ]


class IGappScope(object):
    props = {
        'id': Edm.String,
        'type': Edm.String,
        'displayName': Edm.String,
    }
    rels = [

    ]


class IGIdentity(object):
    props = {
        'displayName': Edm.String,
        'id': Edm.String,
        'oDataType': Edm.String,
    }
    rels = [

    ]

