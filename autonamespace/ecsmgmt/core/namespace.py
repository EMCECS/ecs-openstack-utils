"""
Created on Jun 24, 2015

@author: joshia7
"""

import requests
import simplejson as json
import ecsmgmt.core.namespace
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


# from ECSAdminClient import ECSAdminClient

class Namespace:
    """
    Class for provisioning and managing namespaces
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getNamespaces(self):
        """
        Gets the identifiers for all configured namespaces
        """
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        namespaceresponse = requests.get(self.ecsAdminClient.url + NAMESPACES, headers=headers, verify=False)

        self.commons.checkstatus(namespaceresponse)
        return namespaceresponse.json()

    def getDetailedNameSpace(self, id):
        """
        Gets the details for the given namespace
        :param id:Namespace identifier for which details needs to be retrieved.
        """
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        assert id is not None, MESSAGE_NAMESPACE_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        namespaceresponse = requests.get(self.ecsAdminClient.url + NAMESPACES_DETAILED.format(id), headers=headers,
                                         verify=False)

        self.commons.checkstatus(namespaceresponse)
        return namespaceresponse.json()

    def getRetentionClassPeriod(self, namespace, className):
        """
        Gets the retention period for the given namespace and retention class.
        :param namespace:Namespace for which retention period needs to retrieved
        :param className:Class name for which retention period needs to retrieved
        """
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert className is not None, MESSAGE_CLASSNAME_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        retentionresponse = requests.get(self.ecsAdminClient.url + GET_RETENTION_CLASS.format(namespace, className),
                                         headers=headers, verify=False)
        self.commons.checkstatus(retentionresponse)
        return retentionresponse.json()

    def getRetentionList(self, namespace):
        """
        Gets the list of retention classes for the specified namespace
        :param namespace:Namespace identifier for which retention classes needs to retrieved
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        retentionListresponse = requests.get(self.ecsAdminClient.url + GET_RETENTION_LIST.format(namespace),
                                             headers=headers, verify=False)
        self.commons.checkstatus(retentionListresponse)
        return retentionListresponse.json()

    def getNamespaceQuota(self, namespace):
        """
        Gets the namespace hard and soft quotas that have been set for a specified namespace.
        :param namespace:Namespace identifier for which namespace quota details needs to retrieved
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        getQuotaResponse = requests.get(self.ecsAdminClient.url + GET_NAMESPACE_QUOTA.format(namespace),
                                        headers=headers, verify=False)
        self.commons.checkstatus(getQuotaResponse)
        return getQuotaResponse.json()

    def removeNamespaceQuota(self, namespace):
        """
        Deletes the namespace quota for the specified namespace.
        :param namespace:Namespace identifier for which namespace quota details needs to deleted
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Content-Type': 'application/json'}
        removeresponse = requests.delete(self.ecsAdminClient.url + GET_NAMESPACE_QUOTA.format(namespace),
                                         headers=headers, verify=False)
        if self.commons.checkstatus(removeresponse):
            return True
        else:
            return False

    def createNameSpace(self, namespace, namespace_admins, default_data_services_vpool=None,
                        default_object_project=None, allowed_vpools_list=None, disallowed_vpools_list=None,
                        user_mapping=None):
        """
        Creates a namespace with the given details
        :param namespace:User provided namespace
        :param namespace_admins:Comma separated list of namespace admins
        :param default_data_services_vpool:Default replication group identifier for this namespace when creating buckets
        :param default_object_project:Default project id for this tenant when creating buckets
        :param allowed_vpools_list:List of replication groups that are allowed to create buckets in the corresponding
        namespace
        :param disallowed_vpools_list:List of replication groups that are not allowed to create buckets in the
        corresponding namespace
        :param user_mapping:User Mapping Details
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        # assert namespace_admins is not None, MESSAGE_NAMESPACE_ADMIN_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        body = {"namespace": namespace,
                "default_data_services_vpool": default_data_services_vpool,
                "default_object_project": default_object_project,
                "allowed_vpools_list": allowed_vpools_list,
                "disallowed_vpools_list": disallowed_vpools_list,
                "namespace_admins": namespace_admins,
                "user_mapping": user_mapping
                }

        body = json.dumps(body)

        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = self.ecsAdminClient.url + CREATE_NAMESPACE
        namespacecreationresponse = requests.post(self.ecsAdminClient.url + CREATE_NAMESPACE, headers=headers,
                                                  data=body, verify=False)
        if self.commons.checkstatus(namespacecreationresponse):
            return True
        else:
            return False

    def removeNameSpace(self, namespace):
        """
        Deactivates and deletes the given namespace and all associated user mappings.
        :param namespace:An active namespace identifier which needs to be deactivated/deleted
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        removeNameSpaceResponse = requests.post(self.ecsAdminClient.url + REMOVE_NAMESPACE.format(namespace),
                                                headers=headers, verify=False)
        if self.commons.checkstatus(removeNameSpaceResponse):
            return True
        else:
            return False

    def createRetention(self, namespace, name, period):
        """
        Creates a retention class for the specified namespace. The method payload specifies the retention class
        details which define a name for the class and a retention period.
        :param namespace:Namespace identifier for which retention class needs to created
        :param name:Name of the retention class
        :param period:Period of the retention class in seconds
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        assert name is not None, MESSAGE_CLASSNAME_REQUIRED
        assert period is not None, MESSAGE_PERIOD_REQUIRED
        body = {"name": name,
                "period": period}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        retentionCreationResponse = requests.post(self.ecsAdminClient.url + CREATE_RETENTION.format(namespace),
                                                  headers=headers, data=body, verify=False)
        if self.commons.checkstatus(retentionCreationResponse):
            return True
        else:
            return False

    def updateRetention(self, namespace, retention, period):
        """
        Updates the retention class details for a specified retention class for a namespace
        :param namespace:Namespace identifier for which retention class needs to retrieved
        :param retention:Retention class for which details needs to updated.
        :param period:A new period value for class in seconds
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        assert retention is not None, MESSAGE_CLASSNAME_REQUIRED
        assert period is not None, MESSAGE_PERIOD_REQUIRED
        body = {"period": period}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        retentionUpdateResponse = requests.put(self.ecsAdminClient.url + UPDATE_RENTENTION.format(namespace, retention),
                                               headers=headers, data=body, verify=False)
        if self.commons.checkstatus(retentionUpdateResponse):
            return True
        else:
            return False

    def updateNamespaceQuota(self, namespace, blockSize=None, notificationSize=None):
        """
        Updates the namespace quota for a specified namespace
        :param namespace:Namespace identifier for which namespace quota details need to be updated
        :param blockSize:Block size in GB.
        :param notificationSize:Notification size in GB
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        #         assert blockSize!=None,MESSAGE_BLOCKSIZE_REQUIRED
        #         assert notificationSize!=None,MESSAGE_NOTIFICATION_SIZE_REQUIRED
        body = {"blockSize": blockSize,
                "notificationSize": notificationSize}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Content-Type': 'application/json'}
        namespaceQuotaUpdateResponse = requests.put(self.ecsAdminClient.url + UPDATE_NAMESPACE_QUOTA.format(namespace),
                                                    headers=headers, data=body, verify=False)
        if self.commons.checkstatus(namespaceQuotaUpdateResponse):
            return True
        else:
            return False

    def updateNameSpace(self, namespace, namespace_admins, default_data_services_vpool=None,
                        vpools_added_to_allowed_vpools_list=None,
                        vpools_added_to_disallowed_vpools_list=None, vpools_removed_from_allowed_vpools_list=None,
                        vpools_removed_from_disallowed_vpools_list=None, user_mapping=None):
        """
        Updates namespace details such as replication group list, namespace administrators and user mappings
        :param namespace:Namespace identifier whose details needs to be updated
        :param namespace_admins:Comma separated list of namespace admins
        :param default_data_services_vpool:Default replication group identifier when creating buckets
        :param vpools_added_to_allowed_vpools_list:List of replication group identifier which will be added in the
        namespace access allowed list for allowing namespace access
        :param vpools_added_to_disallowed_vpools_list:List of replication group identifiers which will be added in
        the namespace access disallowed list
        :param vpools_removed_from_allowed_vpools_list:List of replication group identifier which will be removed
        from allowed list
        :param vpools_removed_from_disallowed_vpools_list:List of replication group identifier which will be removed
        from the namespace access disallowed list
        :param user_mapping:User Mapping
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert namespace_admins is not None, MESSAGE_NAMESPACE_ADMIN_REQUIRED
        #         assert default_data_services_vpool!=None,MESSAGE_DEFAULT_DATA_SERVICE_REQUIRED
        #         assert token!=None,MESSAGE_TOKEN_REQUIRED
        body = {
            "default_data_services_vpool": default_data_services_vpool,
            "vpools_added_to_allowed_vpools_list": vpools_added_to_allowed_vpools_list,
            "vpools_added_to_disallowed_vpools_list": vpools_added_to_disallowed_vpools_list,
            "vpools_removed_from_allowed_vpools_list": vpools_removed_from_allowed_vpools_list,
            "vpools_removed_from_disallowed_vpools_list": vpools_removed_from_disallowed_vpools_list,
            "namespace_admins": namespace_admins,
            "user_mapping": user_mapping
        }

        body = json.dumps(body)
        print body
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        namespacecreationresponse = requests.put(self.ecsAdminClient.url + UPDATE_NAMESPACE.format(namespace),
                                                 headers=headers, data=body, verify=False)
        if self.commons.checkstatus(namespacecreationresponse):
            return True
        else:
            return False
