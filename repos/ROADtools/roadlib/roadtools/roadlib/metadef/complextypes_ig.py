from roadtools.roadlib.metadef.basetypes import Edm, Collection
import enum

IGexpirationPatternType_data = {
    'notSpecified': 0,
    'noExpiration': 1,
    'afterDateTime': 2,
    'afterDuration': 3,
}
IGexpirationPatternType = enum.Enum('IGexpirationPatternType', IGexpirationPatternType_data)


IGaccessPackageFilterByCurrentUserOptions_data = {
    'allowedRequestor': 1,
    'unknownFutureValue': 99,
}
IGaccessPackageFilterByCurrentUserOptions = enum.Enum('IGaccessPackageFilterByCurrentUserOptions', IGaccessPackageFilterByCurrentUserOptions_data)


IGaccessPackageAssignmentFilterByCurrentUserOptions_data = {
    'target': 1,
    'createdBy': 2,
    'targetApplicationOwner': 3,
    'unknownFutureValue': 99,
    'targetManager': 100,
}
IGaccessPackageAssignmentFilterByCurrentUserOptions = enum.Enum('IGaccessPackageAssignmentFilterByCurrentUserOptions', IGaccessPackageAssignmentFilterByCurrentUserOptions_data)


IGaccessPackageAssignmentRequestFilterByCurrentUserOptions_data = {
    'target': 1,
    'createdBy': 2,
    'approver': 3,
    'targetApplicationOwner': 4,
    'unknownFutureValue': 99,
    'targetOrRequestor': 100,
    'targetManager': 101,
    'requestForOthers': 102,
}
IGaccessPackageAssignmentRequestFilterByCurrentUserOptions = enum.Enum('IGaccessPackageAssignmentRequestFilterByCurrentUserOptions', IGaccessPackageAssignmentRequestFilterByCurrentUserOptions_data)


IGaccessPackageSuggestionFilterByCurrentUserOptions_data = {
    'none': 0,
    'relatedPeopleAssignments': 1,
    'assignmentHistory': 2,
    'unknownFutureValue': 4,
}
IGaccessPackageSuggestionFilterByCurrentUserOptions = enum.Enum('IGaccessPackageSuggestionFilterByCurrentUserOptions', IGaccessPackageSuggestionFilterByCurrentUserOptions_data)


IGallowedTargetScope_data = {
    'notSpecified': 0,
    'specificDirectoryUsers': 1,
    'specificConnectedOrganizationUsers': 2,
    'specificDirectoryServicePrincipals': 3,
    'allMemberUsers': 4,
    'allDirectoryUsers': 5,
    'allDirectoryServicePrincipals': 6,
    'allConfiguredConnectedOrganizationUsers': 7,
    'allExternalUsers': 8,
    'allDirectoryAgentIdentities': 9,
    'unknownFutureValue': 10,
}
IGallowedTargetScope = enum.Enum('IGallowedTargetScope', IGallowedTargetScope_data)


IGaccessReviewExpirationBehavior_data = {
    'keepAccess': 0,
    'removeAccess': 1,
    'acceptAccessRecommendation': 2,
    'unknownFutureValue': 99,
}
IGaccessReviewExpirationBehavior = enum.Enum('IGaccessReviewExpirationBehavior', IGaccessReviewExpirationBehavior_data)


IGrecurrencePatternType_data = {
    'daily': 0,
    'weekly': 1,
    'absoluteMonthly': 2,
    'relativeMonthly': 3,
    'absoluteYearly': 4,
    'relativeYearly': 5,
}
IGrecurrencePatternType = enum.Enum('IGrecurrencePatternType', IGrecurrencePatternType_data)


IGdayOfWeek_data = {
    'sunday': 0,
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
}
IGdayOfWeek = enum.Enum('IGdayOfWeek', IGdayOfWeek_data)


IGweekIndex_data = {
    'first': 0,
    'second': 1,
    'third': 2,
    'fourth': 3,
    'last': 4,
}
IGweekIndex = enum.Enum('IGweekIndex', IGweekIndex_data)


IGrecurrenceRangeType_data = {
    'endDate': 0,
    'noEnd': 1,
    'numbered': 2,
}
IGrecurrenceRangeType = enum.Enum('IGrecurrenceRangeType', IGrecurrenceRangeType_data)


IGserviceTreeOwnershipType_data = {
    'devOwners': 1,
    'pmOwners': 2,
    'admins': 3,
    'owners': 4,
}
IGserviceTreeOwnershipType = enum.Enum('IGserviceTreeOwnershipType', IGserviceTreeOwnershipType_data)


IGserviceTreeLevel_data = {
    'offering': 0,
    'service': 1,
    'teamGroup': 2,
    'serviceGroup': 3,
    'organization': 4,
    'division': 5,
}
IGserviceTreeLevel = enum.Enum('IGserviceTreeLevel', IGserviceTreeLevel_data)


IGaccessPackageCatalogState_data = {
    'unpublished': 1,
    'published': 2,
    'unknownFutureValue': 3,
}
IGaccessPackageCatalogState = enum.Enum('IGaccessPackageCatalogState', IGaccessPackageCatalogState_data)


IGaccessReviewTimeoutBehavior_data = {
    'keepAccess': 0,
    'removeAccess': 1,
    'acceptAccessRecommendation': 2,
    'unKnownFutureValue': 99,
}
IGaccessReviewTimeoutBehavior = enum.Enum('IGaccessReviewTimeoutBehavior', IGaccessReviewTimeoutBehavior_data)


IGaccessPackageCustomExtensionStage_data = {
    'assignmentRequestCreated': 1,
    'assignmentRequestApproved': 2,
    'assignmentRequestGranted': 3,
    'assignmentRequestRemoved': 4,
    'assignmentFourteenDaysBeforeExpiration': 5,
    'assignmentOneDayBeforeExpiration': 6,
    'unknownFutureValue': 7,
    'assignmentRequestDeterminingApprovalRequirements': 8,
}
IGaccessPackageCustomExtensionStage = enum.Enum('IGaccessPackageCustomExtensionStage', IGaccessPackageCustomExtensionStage_data)


IGprivilegeLevel_data = {
    'standard': 0,
    'privileged': 1,
    'unknownFutureValue': 2,
}
IGprivilegeLevel = enum.Enum('IGprivilegeLevel', IGprivilegeLevel_data)


IGaccessPackageRequestState_data = {
    'submitted': 0,
    'pendingApproval': 1,
    'delivering': 2,
    'delivered': 3,
    'deliveryFailed': 4,
    'denied': 5,
    'scheduled': 6,
    'canceled': 7,
    'partiallyDelivered': 8,
    'unknownFutureValue': 9,
}
IGaccessPackageRequestState = enum.Enum('IGaccessPackageRequestState', IGaccessPackageRequestState_data)


IGaccessPackageSubjectType_data = {
    'notSpecified': 0,
    'user': 1,
    'servicePrincipal': 2,
    'unknownFutureValue': 3,
    'group': 4,
    'groupSecurityNotEnabled': 5,
    'agentIdentity': 6,
}
IGaccessPackageSubjectType = enum.Enum('IGaccessPackageSubjectType', IGaccessPackageSubjectType_data)


IGaccessPackageSubjectLifecycle_data = {
    'notDefined': 0,
    'notGoverned': 1,
    'governed': 2,
    'unknownFutureValue': 3,
}
IGaccessPackageSubjectLifecycle = enum.Enum('IGaccessPackageSubjectLifecycle', IGaccessPackageSubjectLifecycle_data)


IGaccessPackageAssignmentState_data = {
    'delivering': 0,
    'partiallyDelivered': 1,
    'delivered': 2,
    'expired': 3,
    'deliveryFailed': 4,
    'unknownFutureValue': 5,
}
IGaccessPackageAssignmentState = enum.Enum('IGaccessPackageAssignmentState', IGaccessPackageAssignmentState_data)


IGaccessPackageCustomExtensionHandlerStatus_data = {
    'requestSent': 1,
    'requestReceived': 2,
    'unknownFutureValue': 3,
}
IGaccessPackageCustomExtensionHandlerStatus = enum.Enum('IGaccessPackageCustomExtensionHandlerStatus', IGaccessPackageCustomExtensionHandlerStatus_data)


IGaccessPackageRequestType_data = {
    'notSpecified': 0,
    'userAdd': 1,
    'userUpdate': 2,
    'userRemove': 3,
    'adminAdd': 4,
    'adminUpdate': 5,
    'adminRemove': 6,
    'systemAdd': 7,
    'systemUpdate': 8,
    'systemRemove': 9,
    'onBehalfAdd': 10,
    'unknownFutureValue': 11,
    'userExtend': 99,
}
IGaccessPackageRequestType = enum.Enum('IGaccessPackageRequestType', IGaccessPackageRequestType_data)


IGcustomExtensionCalloutInstanceStatus_data = {
    'calloutSent': 1,
    'callbackReceived': 2,
    'calloutFailed': 3,
    'callbackTimedOut': 4,
    'waitingForCallback': 5,
    'unknownFutureValue': 6,
}
IGcustomExtensionCalloutInstanceStatus = enum.Enum('IGcustomExtensionCalloutInstanceStatus', IGcustomExtensionCalloutInstanceStatus_data)


IGoptInPreviewFeatureSelection_data = {
    'keepDefault': 0,
    'optIn': 1,
    'optOut': 2,
}
IGoptInPreviewFeatureSelection = enum.Enum('IGoptInPreviewFeatureSelection', IGoptInPreviewFeatureSelection_data)


IGaccessPackageRelatedPeopleSuggestionInsightLevel_data = {
    'disabled': 0,
    'count': 1,
    'countAndNames': 2,
    'unknownFutureValue': 3,
}
IGaccessPackageRelatedPeopleSuggestionInsightLevel = enum.Enum('IGaccessPackageRelatedPeopleSuggestionInsightLevel', IGaccessPackageRelatedPeopleSuggestionInsightLevel_data)


IGresourceVisibilityScope_data = {
    'allDirectoryUsers': 0,
    'allMemberUsers': 1,
    'none': 2,
    'unknownFutureValue': 3,
}
IGresourceVisibilityScope = enum.Enum('IGresourceVisibilityScope', IGresourceVisibilityScope_data)


IGRiskLevel_data = {
    'low': 0,
    'medium': 1,
    'high': 2,
    'hidden': 3,
    'none': 4,
    'unknownFutureValue': 5,
}
IGRiskLevel = enum.Enum('IGRiskLevel', IGRiskLevel_data)


IGenforcementScope_data = {
    'newGuestOnboarding': 0,
    'anyGuestRequest': 1,
    'unknownFutureValue': 2,
}
IGenforcementScope = enum.Enum('IGenforcementScope', IGenforcementScope_data)


IGPurviewInsiderRiskManagementLevel_data = {
    'none': 0,
    'minor': 1,
    'moderate': 2,
    'elevated': 3,
    'unknownFutureValue': 4,
}
IGPurviewInsiderRiskManagementLevel = enum.Enum('IGPurviewInsiderRiskManagementLevel', IGPurviewInsiderRiskManagementLevel_data)


IGApproverInformationVisibility_data = {
    'Default': 0,
    'NotVisible': 1,
    'Visible': 2,
}
IGApproverInformationVisibility = enum.Enum('IGApproverInformationVisibility', IGApproverInformationVisibility_data)


IGVerifiableCredentialPresentationStatusCode_data = {
    'request_retrieved': 0,
    'presentation_verified': 1,
    'unknownFutureValue': 9,
}
IGVerifiableCredentialPresentationStatusCode = enum.Enum('IGVerifiableCredentialPresentationStatusCode', IGVerifiableCredentialPresentationStatusCode_data)


IGConnectorType_data = {
    'sapIag': 0,
}
IGConnectorType = enum.Enum('IGConnectorType', IGConnectorType_data)


class IGsubjectSet(object):
    props = {
        'isBackup': Edm.Boolean,
    }


class IGsingleUser(object):
    props = {
        'objectId': Edm.String,
        'id': Edm.String,
        'userId': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
    }


class IGgroupMembers(object):
    props = {
        'objectId': Edm.String,
        'id': Edm.String,
        'groupId': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
    }


class IGrequestorManager(object):
    props = {
        'managerLevel': Edm.Int32,
    }


class IGconnectedOrganizationMembers(object):
    props = {
        'objectId': Edm.String,
        'id': Edm.String,
        'connectedOrganizationId': Edm.String,
        'displayName': Edm.String,
        'description': Edm.String,
    }


class IGinternalSponsors(object):
    props = {

    }


class IGexternalSponsors(object):
    props = {

    }


class IGidentity(object):
    props = {
        'id': Edm.String,
        'displayName': Edm.String,
    }


class IGanswerString(object):
    props = {
        'value': Edm.String,
    }


class IGresourceAttributeSource(object):
    props = {

    }


class IGresourceAttributeDestination(object):
    props = {

    }


class IGuserDirectoryAttributeStore(object):
    props = {

    }


class IGresourceAttributeStore(object):
    props = {

    }


class IGmultipleChoiceQuestion(object):
    props = {
        'choices': Collection,
        'allowsMultipleSelection': Edm.Boolean,
        'isMultipleSelectionAllowed': Edm.Boolean,
    }


class IGtextInputQuestion(object):
    props = {
        'isSingleLineQuestion': Edm.Boolean,
        'regexPattern': Edm.String,
    }


class IGaccessPackageAssignmentRequestorSettings(object):
    props = {
        'enableTargetsToSelfAddAccess': Edm.Boolean,
        'enableTargetsToSelfUpdateAccess': Edm.Boolean,
        'enableTargetsToSelfRemoveAccess': Edm.Boolean,
        'allowCustomAssignmentSchedule': Edm.Boolean,
        'onBehalfRequestors': Collection,
        'enableOnBehalfRequestorsToAddAccess': Edm.Boolean,
        'enableOnBehalfRequestorsToUpdateAccess': Edm.Boolean,
        'enableOnBehalfRequestorsToRemoveAccess': Edm.Boolean,
    }


class IGtargetAgentIdentitySponsors(object):
    props = {

    }


class IGtargetManager(object):
    props = {
        'managerLevel': Edm.Int32,
    }


class IGtargetApplicationOwners(object):
    props = {

    }


class IGsingleServicePrincipal(object):
    props = {
        'servicePrincipalId': Edm.String,
        'description': Edm.String,
    }


class IGcustomExtensionData(object):
    props = {

    }


class IGaccessPackageAssignmentCallbackData(object):
    props = {
        'stage': IGaccessPackageCustomExtensionStage,
        'customExtensionStageInstanceId': Edm.String,
    }


class IGcustomExtensionCalloutResponse(object):
    props = {
        'source': Edm.String,
        'type': Edm.String,
        'data': IGcustomExtensionData,
    }


class IGserviceManagementReference(object):
    props = {
        'id': Edm.String,
        'type': Edm.String,
    }


class IGexpirationPattern(object):
    props = {
        'endDateTime': Edm.DateTimeOffset,
        'duration': Edm.Duration,
        'type': Edm.String,
    }


class IGrecurrencePattern(object):
    props = {
        'type': IGrecurrencePatternType,
        'interval': Edm.Int32,
        'month': Edm.Int32,
        'dayOfMonth': Edm.Int32,
        'daysOfWeek': Collection,
        'firstDayOfWeek': IGdayOfWeek,
        'index': IGweekIndex,
    }


class IGrecurrenceRange(object):
    props = {
        'type': IGrecurrenceRangeType,
        'numberOfOccurrences': Edm.Int32,
        'recurrenceTimeZone': Edm.String,
        'startDate': Edm.DateTimeOffset,
        'endDate': Edm.DateTimeOffset,
    }


class IGattributeRuleMembers(object):
    props = {
        'description': Edm.String,
        'membershipRule': Edm.String,
    }


class IGcatalogRoleAssignment(object):
    props = {
        'roleDefinitionId': Edm.String,
        'description': Edm.String,
    }


class IGchainUpToManager(object):
    props = {
        'objectId': Edm.String,
        'displayName': Edm.String,
    }


class IGaccessPackageAssignees(object):
    props = {
        'description': Edm.String,
        'id': Edm.String,
    }


class IGleverageCatalogServiceTree(object):
    props = {
        'serviceTreeOwnershipType': IGserviceTreeOwnershipType,
    }


class IGorgHierarchyUsers(object):
    props = {
        'orgLeaderObjectId': Edm.String,
        'orgLeaderDisplayName': Edm.String,
    }


class IGserviceTreeHierarchicalLookup(object):
    props = {
        'serviceTreeLevel': IGserviceTreeLevel,
        'serviceTreeOwnershipType': IGserviceTreeOwnershipType,
    }


class IGtargetAgentIdentitySponsorsOrOwners(object):
    props = {

    }


class IGtargetUserSponsors(object):
    props = {

    }


class IGconnectionInfo(object):
    props = {
        'url': Edm.String,
    }


class IGexternalTokenBasedSapIagConnectionInfo(object):
    props = {
        'subscriptionId': Edm.String,
        'resourceGroup': Edm.String,
        'domain': Edm.String,
        'accessTokenUrl': Edm.String,
        'clientId': Edm.String,
        'keyVaultName': Edm.String,
        'secretKey': Edm.String,
    }


class IGentitlementManagementLocalizedContent(object):
    props = {
        'defaultText': Edm.String,
        'localizedTexts': Collection,
    }


class IGlocalizedText(object):
    props = {
        'text': Edm.String,
        'languageCode': Edm.String,
    }


class IGanswerChoice(object):
    props = {
        'text': Edm.String,
        'localizations': Collection,
        'actualValue': Edm.String,
        'displayValue': IGentitlementManagementLocalizedContent,
    }


class IGcustomExtensionEndpointConfiguration(object):
    props = {

    }


class IGlogicAppTriggerEndpointConfiguration(object):
    props = {
        'subscriptionId': Edm.String,
        'resourceGroupName': Edm.String,
        'logicAppWorkflowName': Edm.String,
        'url': Edm.String,
    }


class IGaccessPackageAutomaticRequestSettings(object):
    props = {
        'requestAccessForAllowedTargets': Edm.Boolean,
        'removeAccessWhenTargetLeavesAllowedTargets': Edm.Boolean,
        'gracePeriodBeforeAccessRemoval': Edm.Duration,
    }


class IGaccessPackageAssignmentApprovalSettings(object):
    props = {
        'isApprovalRequiredForAdd': Edm.Boolean,
        'isApprovalRequiredForUpdate': Edm.Boolean,
        'isRequestorJustificationRequired': Edm.Boolean,
        'skipManagerApprovalForManagerAsRequestor': Edm.Boolean,
        'stages': Collection,
    }


class IGaccessPackageApprovalStage(object):
    props = {
        'durationBeforeAutomaticDenial': Edm.Duration,
        'isApproverJustificationRequired': Edm.Boolean,
        'isApproverAllowedToModifyRequest': Edm.Boolean,
        'isApproverInformationVisibleToRequestor': Edm.Boolean,
        'approverInformationVisibility': IGApproverInformationVisibility,
        'isEscalationEnabled': Edm.Boolean,
        'durationBeforeEscalation': Edm.Duration,
        'primaryApprovers': Collection,
        'fallbackPrimaryApprovers': Collection,
        'escalationApprovers': Collection,
        'fallbackEscalationApprovers': Collection,
    }


class IGaccessPackageDynamicApprovalStage(object):
    props = {

    }


class IGcustomExtensionClientConfiguration(object):
    props = {
        'timeoutInMilliseconds': Edm.Int32,
        'maximumRetries': Edm.Int32,
    }


class IGcustomExtensionAuthenticationConfiguration(object):
    props = {

    }


class IGazureAdTokenAuthentication(object):
    props = {
        'resourceId': Edm.String,
    }


class IGazureAdPopTokenAuthentication(object):
    props = {

    }


class IGcustomExtensionCallbackConfiguration(object):
    props = {
        'durationBeforeTimeout': Edm.Duration,
        'timeoutDuration': Edm.Duration,
    }


class IGaccessPackageRequestApprovalStageCallbackConfiguration(object):
    props = {

    }


class IGcustomExtensionResponseConfiguration(object):
    props = {
        'isCallbackSupported': Edm.Boolean,
        'callbackMaxDuration': Edm.Duration,
    }


class IGAccessPackageNotificationSettings(object):
    props = {
        'isAssignmentNotificationDisabled': Edm.Boolean,
    }


class IGrequestorSettings(object):
    props = {
        'allowCustomAssignmentSchedule': Edm.Boolean,
        'scopeType': Edm.String,
        'isOnBehalfAllowed': Edm.Boolean,
        'acceptRequests': Edm.Boolean,
        'allowedRequestors': Collection,
        'requestorScope': Collection,
        'onBehalfRequestors': Collection,
    }


class IGassignmentReviewSettings(object):
    props = {
        'isEnabled': Edm.Boolean,
        'recurrenceType': Edm.String,
        'reviewerType': Edm.String,
        'startDateTime': Edm.DateTimeOffset,
        'durationInDays': Edm.Int32,
        'businessFlowId': Edm.String,
        'reviewers': Collection,
        'accessReviewTimeoutBehavior': IGaccessReviewTimeoutBehavior,
        'isAccessRecommendationEnabled': Edm.Boolean,
        'isAgenticExperienceEnabled': Edm.Boolean,
        'isApprovalJustificationRequired': Edm.Boolean,
        'isReminderNotificationsDisabled': Edm.Boolean,
    }


class IGapprovalSettings(object):
    props = {
        'isApprovalRequired': Edm.Boolean,
        'isApprovalRequiredForUpdate': Edm.Boolean,
        'isApprovalRequiredForExtension': Edm.Boolean,
        'skipManagerApprovalForManagerAsRequestor': Edm.Boolean,
        'isRequestorJustificationRequired': Edm.Boolean,
        'approvalMode': Edm.String,
        'approvalStages': Collection,
    }


class IGapprovalStage(object):
    props = {
        'approvalStageTimeOutInDays': Edm.Int32,
        'isApproverJustificationRequired': Edm.Boolean,
        'isApproverAllowedToModifyRequest': Edm.Boolean,
        'isApproverInformationVisibleToRequestor': Edm.Boolean,
        'approverInformationVisibility': IGApproverInformationVisibility,
        'isEscalationEnabled': Edm.Boolean,
        'escalationTimeInMinutes': Edm.Int32,
        'primaryApprovers': Collection,
        'escalationApprovers': Collection,
    }


class IGguestApprovalStage(object):
    props = {

    }


class IGdynamicApprovalStage(object):
    props = {

    }


class IGrequestActivity(object):
    props = {
        'action': Edm.String,
        'actorDisplayName': Edm.String,
        'actorPrincipalName': Edm.String,
        'userDisplayName': Edm.String,
        'userPrincipalName': Edm.String,
        'actionDateTime': Edm.DateTimeOffset,
        'scheduledDateTime': Edm.DateTimeOffset,
        'detail': Edm.String,
    }


class IGrequestParameter(object):
    props = {
        'name': Edm.String,
        'value': Edm.String,
    }


class IGaccessPackageAssignmentCalloutData(object):
    props = {
        'accessPackageAssignmentRequestId': Edm.String,
        'customExtensionStageInstanceId': Edm.String,
        'stage': Edm.String,
        'callbackConfiguration': IGcustomExtensionCallbackConfiguration,
    }


class IGassignmentRequestApprovalStageCallbackData(object):
    props = {
        'approvalStage': IGaccessPackageApprovalStage,
    }


class IGaccessPackageAssignmentRequestCalloutData(object):
    props = {
        'accessPackageAssignmentRequestId': Edm.String,
        'callbackUriPath': Edm.String,
        'customExtensionStageInstanceId': Edm.String,
        'stage': Edm.String,
        'requestType': IGaccessPackageRequestType,
        'answers': Collection,
        'state': IGaccessPackageRequestState,
        'status': Edm.String,
        'callbackConfiguration': IGcustomExtensionCallbackConfiguration,
        'verifiedCredentialsData': Collection,
    }


class IGoptInPreviewFeatures(object):
    props = {
        'enforcePolicyApprovalSettingForAdmins': IGoptInPreviewFeatureSelection,
        'enforcePolicyScopeSettingForAdmins': IGoptInPreviewFeatureSelection,
        'enableMyAccessOverviewForEndUser': IGoptInPreviewFeatureSelection,
        'enableApproverRevoke': IGoptInPreviewFeatureSelection,
        'enableRecommendationForEndUser': IGoptInPreviewFeatureSelection,
        'enableApproverDelegate': IGoptInPreviewFeatureSelection,
    }


class IGAccessPackageSuggestionReason(object):
    props = {
        'score': Edm.Int32,
    }


class IGAccessPackageSuggestionSelfAssignmentHistoryBased(object):
    props = {
        'pastAssigmentCount': Edm.Int32,
        'lastAssignmentDateTime': Edm.DateTimeOffset,
    }


class IGAccessPackageSuggestionRelatedPeopleBased(object):
    props = {
        'relatedPeopleAssignmentCount': Edm.Int32,
        'relatedPeople': Collection,
    }


class IGrbacApplication(object):
    props = {

    }


class IGunifiedRolePermission(object):
    props = {
        'allowedResourceActions': Collection,
        'condition': Edm.String,
    }


class IGApprovalEvent(object):
    props = {
        'isMultiStage': Edm.String,
        'childId': Edm.String,
        'stage': Edm.String,
        'eventTypeId': Edm.Guid,
        'id': Edm.Guid,
        'partnerId': Edm.String,
        'deduplicationId': Edm.String,
        'property1': Edm.String,
        'name': Edm.String,
        'tenantId': Edm.Guid,
        'description': Edm.String,
        'dateTime': Edm.DateTimeOffset,
        'payload': Edm.String,
        'payloadType': Edm.String,
        'properties': Collection,
    }


class IGverifiableCredentialSettings(object):
    props = {
        'credentialTypes': Collection,
    }


class IGverifiableCredentialType(object):
    props = {
        'issuers': Collection,
        'credentialType': Edm.String,
        'claims': Collection,
        'faceCheckPhotoClaimName': Edm.String,
    }


class IGverifiableCredentialIssuerInfo(object):
    props = {
        'linkedDomains': Collection,
        'decentralizedId': Edm.String,
        'issuerId': Edm.Guid,
    }


class IGVerifiedCredentialClaims(object):
    props = {

    }


class IGCredentialState(object):
    props = {
        'revocationStatus': Edm.String,
    }


class IGDomainValidation(object):
    props = {
        'url': Edm.String,
    }


class IGFaceCheck(object):
    props = {
        'matchConfidenceScore': Edm.Int64,
        'sourcePhotoQuality': Edm.String,
    }


class IGVerifiableCredentialRequirementStatus(object):
    props = {

    }


class IGVerifiableCredentialVerified(object):
    props = {

    }


class IGVerifiableCredentialRetrieved(object):
    props = {
        'expiryDateTime': Edm.DateTimeOffset,
    }


class IGVerifiableCredentialRequired(object):
    props = {
        'expiryDateTime': Edm.DateTimeOffset,
        'url': Edm.String,
    }


class IGKeyValuePair_2OfString_String(object):
    props = {

    }


class IGresourceAttribute(object):
    props = {
        'id': Edm.String,
        'attributeName': Edm.String,
        'name': Edm.String,
        'attributeDefaultValue': Edm.String,
        'isEditable': Edm.Boolean,
        'isPersistedOnAssignmentRemoval': Edm.Boolean,
        'attributeSource': IGresourceAttributeSource,
        'source': IGresourceAttributeSource,
        'attributeDestination': IGresourceAttributeDestination,
        'destination': IGresourceAttributeDestination,
    }


class IGquestion(object):
    props = {
        'id': Edm.String,
        'isRequired': Edm.Boolean,
        'isAnswerEditable': Edm.Boolean,
        'text': IGentitlementManagementLocalizedContent,
        'textString': Edm.String,
        'localizations': Collection,
        'sequence': Edm.Int32,
        'attribute': IGresourceAttribute,
    }


class IGcustomExtensionHandlerInstance(object):
    props = {
        'id': Edm.String,
        'customExtensionHandlerId': Edm.String,
        'status': IGaccessPackageCustomExtensionHandlerStatus,
        'externalCorrelationId': Edm.String,
        'customExtensionId': Edm.String,
        'stage': IGaccessPackageCustomExtensionStage,
        'error': Edm.String,
        'callbackData': IGcustomExtensionData,
    }


class IGcustomExtensionCalloutInstance(object):
    props = {
        'id': Edm.String,
        'status': IGcustomExtensionCalloutInstanceStatus,
        'externalCorrelationId': Edm.String,
        'customExtensionId': Edm.String,
        'error': Edm.String,
        'detail': Edm.String,
        'callbackData': IGcustomExtensionData,
    }


class IGpatternedRecurrence(object):
    props = {
        'pattern': IGrecurrencePattern,
        'range': IGrecurrenceRange,
    }


class IGVerifiedCredentialData(object):
    props = {
        'issuer': Edm.String,
        'type': Collection,
        'claims': IGVerifiedCredentialClaims,
        'credentialState': IGCredentialState,
        'domainValidation': IGDomainValidation,
        'issuanceDate': Edm.String,
        'expirationDate': Edm.String,
        'faceCheck': IGFaceCheck,
    }


class IGanswer(object):
    props = {
        'displayValue': Edm.String,
        'answeredQuestion': IGquestion,
    }


class IGresourceAttributeQuestion(object):
    props = {
        'question': IGquestion,
    }


class IGentitlementManagementSchedule(object):
    props = {
        'startDateTime': Edm.DateTimeOffset,
        'duration': Edm.Duration,
        'stopDateTime': Edm.DateTimeOffset,
        'expiration': IGexpirationPattern,
        'recurrence': IGpatternedRecurrence,
    }


class IGaccessPackageAssignmentRequestRequirements(object):
    props = {
        'policyId': Edm.String,
        'policyDisplayName': Edm.String,
        'policyDescription': Edm.String,
        'isApprovalRequiredForAdd': Edm.Boolean,
        'isApprovalRequiredForUpdate': Edm.Boolean,
        'isApprovalRequired': Edm.Boolean,
        'isApprovalRequiredForExtension': Edm.Boolean,
        'isCustomAssignmentScheduleAllowed': Edm.Boolean,
        'allowCustomAssignmentSchedule': Edm.Boolean,
        'isRequestorJustificationRequired': Edm.Boolean,
        'schedule': IGentitlementManagementSchedule,
        'questions': Collection,
        'existingAnswers': Collection,
        'verifiableCredentialRequirementStatus': IGVerifiableCredentialRequirementStatus,
        'requestorSettings': IGaccessPackageAssignmentRequestorSettings,
    }


class IGaccessPackageAssignmentReviewSettings(object):
    props = {
        'isEnabled': Edm.Boolean,
        'schedule': IGentitlementManagementSchedule,
        'expirationBehavior': IGaccessReviewExpirationBehavior,
        'businessFlowId': Edm.String,
        'isRecommendationEnabled': Edm.Boolean,
        'isReminderNotificationsDisabled': Edm.Boolean,
        'isReviewerJustificationRequired': Edm.Boolean,
        'isAgenticExperienceEnabled': Edm.Boolean,
        'isSelfReview': Edm.Boolean,
        'primaryReviewers': Collection,
        'fallbackReviewers': Collection,
    }


class IGaccessPackageAssignmentRequestCallbackData(object):
    props = {
        'stage': IGaccessPackageCustomExtensionStage,
        'customExtensionStageInstanceId': Edm.String,
        'state': IGaccessPackageRequestState,
        'answers': Collection,
        'schedule': IGentitlementManagementSchedule,
        'customExtensionStageInstanceDetail': Edm.String,
    }


class IGapproverDelegate(object):
    props = {
        'schedule': IGentitlementManagementSchedule,
        'delegate': IGsubjectSet,
    }

