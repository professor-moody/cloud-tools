import { Injectable } from '@angular/core';
import { PIMRoleDefinition, AccessPackagePolicy, AccessPackageDetails, AzureScopeInfo, AzureRoleAssignment } from './aadobjects.service';

@Injectable({
  providedIn: 'root'
})
export class UtilitiesService {

  constructor() { }

  /**
   * Determines if a role requires approval for activation
   * @param roleDefinition The role definition object
   * @returns true if approval is required, false if not, null if unable to determine
   */
  requiresApproval(roleDefinition: PIMRoleDefinition): boolean | null {
    try {
      // Check if roleSettingsv2 exists
      if (!roleDefinition.roleSettingsv2 || !Array.isArray(roleDefinition.roleSettingsv2) || roleDefinition.roleSettingsv2.length === 0) {
        return null;
      }
      const roleSettings = roleDefinition.roleSettingsv2[0];
      if (!roleSettings.lifeCycleManagement || !Array.isArray(roleSettings.lifeCycleManagement)) {
        return null;
      }

      // Find the EndUser activation rule (caller: 'EndUser', level: 'Member')
      const endUserMemberRule = roleSettings.lifeCycleManagement.find(
        (rule: any) => rule.caller === 'EndUser' && rule.level === 'Member'
      );

      if (!endUserMemberRule || !endUserMemberRule.value) {
        return null;
      }

      // Find the ApprovalRule in the value array
      const approvalRule = endUserMemberRule.value.find(
        (rule: any) => rule.ruleIdentifier === 'ApprovalRule'
      );

      if (!approvalRule || !approvalRule.setting) {
        return null;
      }

      // Parse the approval rule setting (JSON string)
      const approvalSetting = JSON.parse(approvalRule.setting);

      // Return whether approval is enabled, can use either casing weirdly enough
      return approvalSetting.enabled === true || approvalSetting.Enabled === true;
    } catch (error) {
      console.error('Error parsing role settings for approval:', error);
      return null;
    }
  }

  /**
   * Checks if an access package requires approval
   * @param accessPackage The access package policy
   * @returns true if approval is required, false otherwise
   */
    requiresAccessPackageApproval(accessPackage: AccessPackagePolicy): boolean {
    // Check both possible locations for approval settings
    const approvalSettings = accessPackage.approvalSettings || accessPackage.requestApprovalSettings;

    if (!approvalSettings) {
      return false;
    }

    // Check both possible property names
    return approvalSettings.isApprovalRequiredForAdd === true ||
           approvalSettings.isApprovalRequired === true;
  }

  /**
   * Gets a human-readable duration string
   * @param durationInDays Number of days
   * @returns Formatted duration string
   */
  formatDuration(durationInDays: number): string {
    if (durationInDays == 0){
      return "No expiry"
    } else if (durationInDays >= 365) {
      const years = Math.floor(durationInDays / 365);
      return years === 1 ? '1 year' : `${years} years`;
    } else if (durationInDays >= 30) {
      const months = Math.floor(durationInDays / 30);
      return months === 1 ? '1 month' : `${months} months`;
    } else {
      return durationInDays === 1 ? '1 day' : `${durationInDays} days`;
    }
  }

  /**
   * Gets formatted approver information for an access package
   * @param accessPackage The access package policy
   * @returns Array of approver descriptions
   */
  getApprovers(accessPackage: AccessPackagePolicy): string[] {
    // Check both possible locations for approval settings
    const approvalSettings = accessPackage.approvalSettings || accessPackage.requestApprovalSettings;

    if (!approvalSettings || (!approvalSettings.isApprovalRequiredForAdd && !approvalSettings.isApprovalRequired)) {
      return [];
    }

    const approvers: string[] = [];

    // Check both possible stage array names
    const stages = approvalSettings.stages || approvalSettings.approvalStages || [];

    stages.forEach((stage, index) => {
      const stageLabel = stages.length > 1 ? `Stage ${index + 1}: ` : '';

      // Process primary approvers
      if (stage.primaryApprovers && stage.primaryApprovers.length > 0) {
        const primaryApproverNames = stage.primaryApprovers
          .filter(approver => !approver.isBackup)
          .map(approver => this.formatApprover(approver));

        if (primaryApproverNames.length > 0) {
          approvers.push(`${stageLabel}${primaryApproverNames.join(', ')}`);
        }
      }

      // Process fallback approvers
      const fallbackApprovers = stage.fallbackPrimaryApprovers ||
                               stage.primaryApprovers?.filter(a => a.isBackup);

      if (fallbackApprovers && fallbackApprovers.length > 0) {
        const fallbackNames = fallbackApprovers.map(approver => this.formatApprover(approver));
        if (fallbackNames.length > 0) {
          approvers.push(`${stageLabel}Fallback: ${fallbackNames.join(', ')}`);
        }
      }
    });

    return approvers;
  }

  /**
   * Formats an individual approver based on their type
   * @param approver The approver object
   * @returns Formatted approver string
   */
  formatApprover(approver: any): string {
    if (!approver || !approver['@odata.type']) {
      return 'Unknown approver';
    }

    switch (approver['@odata.type']) {
      case '#Microsoft.IGAELM.EC.FrontEnd.ExternalModel.requestorManager':
        const level = approver.managerLevel || 1;
        return level === 1 ? 'Manager' : `Manager (level ${level})`;

      case '#Microsoft.IGAELM.EC.FrontEnd.ExternalModel.singleUser':
        return approver.displayName || 'User';

      case '#Microsoft.IGAELM.EC.FrontEnd.ExternalModel.groupMembers':
        return `Group: ${approver.displayName || 'Unknown'}`;

      default:
        return approver.displayName || 'Unknown approver';
    }
  }

  parseAzureScope(scope: string): AzureScopeInfo {
    if (!scope || scope === '/') {
      return {
        type: 'Root',
        displayName: 'Root (Tenant)'
      };
    }

    const parts = scope.split('/').filter(p => p);

    // Check if it starts with "providers" (management group)
    if (parts[0] === 'providers' && parts[1] === 'Microsoft.Management') {
      return {
        type: 'ManagementGroup',
        displayName: `Management Group: ${parts[3] || 'Unknown'}`
      };
    }

    // Subscription level
    if (parts.length === 2 && parts[0] === 'subscriptions') {
      return {
        type: 'Subscription',
        displayName: 'Subscription',
        subscriptionId: parts[1]
      };
    }

    // Resource Group level
    if (parts.length === 4 && parts[0] === 'subscriptions' && parts[2] === 'resourceGroups') {
      return {
        type: 'ResourceGroup',
        displayName: `Resource Group: ${parts[3]}`,
        subscriptionId: parts[1],
        resourceGroup: parts[3]
      };
    }

    // Individual Resource level
    if (parts.length >= 6 && parts[0] === 'subscriptions' && parts[4] === 'providers') {
      const resourceProvider = parts[5];
      const resourceType = parts[6];
      const resourceName = parts[7];

      return {
        type: 'Resource',
        displayName: `${this.formatResourceType(resourceType)}: ${resourceName || 'Unknown'}`,
        subscriptionId: parts[1],
        resourceGroup: parts[3],
        resourceProvider: resourceProvider,
        resourceType: resourceType,
        resourceName: resourceName
      };
    }

    // Unknown/other scope
    return {
      type: 'Resource',
      displayName: scope
    };
  }

  /**
   * Formats Azure resource type for display
   * @param resourceType The resource type from the scope
   * @returns Human-readable resource type
   */
  formatResourceType(resourceType: string): string {
    if (!resourceType) {
      return 'Resource';
    }

    // Convert camelCase to Title Case
    const formatted = resourceType
      .replace(/([A-Z])/g, ' $1')
      .trim()
      .replace(/^./, str => str.toUpperCase());

    return formatted;
  }

  /**
   * Gets an icon name for the scope type
   * @param scopeInfo The parsed scope information
   * @returns Material icon name
   */
  getScopeIcon(scopeInfo: AzureScopeInfo): string {
    switch (scopeInfo.type) {
      case 'Root':
        return 'domain';
      case 'ManagementGroup':
        return 'account_tree';
      case 'Subscription':
        return 'credit_card';
      case 'ResourceGroup':
        return 'folder';
      case 'Resource':
        return 'dashboard_customize';
      default:
        return 'help_outline';
    }
  }

  /**
   * Gets a CSS class for the scope type
   * @param scopeInfo The parsed scope information
   * @returns CSS class name
   */
  getScopeClass(scopeInfo: AzureScopeInfo): string {
    return `scope-${scopeInfo.type.toLowerCase()}`;
  }

  /**
   * Formats a date string to the user's locale
   * @param dateString ISO date string
   * @returns Formatted date string or null if invalid
   */
  formatDateTime(dateString: string | null | undefined): string | null {
    if (!dateString) {
      return null;
    }

    try {
      const date = new Date(dateString);

      // Check if date is valid
      if (isNaN(date.getTime())) {
        return dateString;
      }

      // Format to user's locale with date and time
      return date.toLocaleString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (error) {
      console.error('Error formatting date:', error);
      return dateString;
    }
  }

  /**
   * Formats a date string to the user's locale (date only, no time)
   * @param dateString ISO date string
   * @returns Formatted date string or null if invalid
   */
  formatDate(dateString: string | null | undefined): string | null {
    if (!dateString) {
      return null;
    }

    try {
      const date = new Date(dateString);

      // Check if date is valid
      if (isNaN(date.getTime())) {
        return dateString;
      }

      // Format to user's locale with date only
      return date.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch (error) {
      console.error('Error formatting date:', error);
      return dateString;
    }
  }

  public translateAuthStrength(guid: string): string {
    const builtIn: { [key: string]: string } = {
      '00000000-0000-0000-0000-000000000002': 'Multi-factor authentication',
      '00000000-0000-0000-0000-000000000003': 'Passwordless MFA',
      '00000000-0000-0000-0000-000000000004': 'Phishing-resistant MFA'
    };
    return builtIn[guid] ?? `Unknown auth strength policy: ${guid} (probably custom)`;
  }
}
