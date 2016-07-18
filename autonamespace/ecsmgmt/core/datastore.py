"""
Created on Jul 6, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *
from array import array


class DataStore:
    """
    Class for provisioning object data stores
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getVDCDataStoreList(self):
        """
        Gets list of data stores configured in the system
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        datastorelist = requests.get(self.ecsAdminClient.url + GET_VDC_DATA_STORES, headers=headers,
                                     verify=False)
        self.commons.checkstatus(datastorelist)
        return datastorelist.json()

    def createDataStoreOnCommodity(self, nodeList):
        """
        Creates data store(s) on commodity nodes
        :param nodeList:An JSON array with
                       nodeId:IP address for the commodity node.
                       name:User provided name
                       virtual_array:Desired storage pool Id for creating the data store
                       description:User provided description

        """
        assert isinstance(nodeList, array), MESSAGE_NODELIST_SHOULD_BE_ARRAY
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        params = dict()
        params['nodes'] = nodeList
        body = json.dumps(params)
        createresponse = requests.post(self.ecsAdminClient.url + CREATE_DATA_STORE, headers=headers,
                                       data=body, verify=False)
        if self.commons.checkstatus(createresponse):
            return True
        else:
            return False


            #         assert nodeId!=None,MESSAGE_NODE_ID_REQUIRED
            #         assert name!=None,MESSAGE_NODE_NAME_REQUIRED
            #         assert virtual_array!=None,MESSAGE_VIRTUAL_ARRAY_REQUIRED
            #         assert description!=None,MESSAGE_NODE_DESCRIPTION_REQUIRED

    def get_DataStoreAssociatedWithStoragePool(self, datastoreId):
        """
        User provided description
        :param datastoreId:Identifier of the data store
        """
        assert datastoreId is not None, MESSAGE_DATA_STORE_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        datastorelist = requests.get(
            self.ecsAdminClient.url + GET_COMMODITY_DATA_STORE_WITH_STORAGE_POOL.format(datastoreId),
            headers=headers, verify=False)
        self.commons.checkstatus(datastorelist)
        return datastorelist.json()

    def getDataStoreWithVArray(self, storagePoolIdentifier):
        """
        Gets the list of details of commodity data stores associated with a storage pool
        :param storagePoolIdentifier:Identifier of the storage pool
        """
        assert storagePoolIdentifier is not None, MESSAGE_STORAGE_POOL_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        datastorelist = requests.get(
            self.ecsAdminClient.url + GET_COMMODITY_DATA_STORE_WITH_VARRAY.format(storagePoolIdentifier),
            headers=headers, verify=False)
        self.commons.checkstatus(datastorelist)
        return datastorelist.json()

    def deactivateDataStore(self, datastoreId):
        """
        Deactivates the commodity node and data store
        :param datastoreId:Identifier of data store to delete
        """
        assert datastoreId is not None, MESSAGE_DATA_STORE_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deletionResponse = requests.post(
            self.ecsAdminClient.url + DEACTIVATE_DATA_STORE.format(datastoreId), headers=headers,
            verify=False)
        self.commons.checkstatus(deletionResponse)
        return deletionResponse.json()

    def getRecentTask(self, datastoreId, taskOperationId):
        """
        Get all recent tasks for a specific data store.
        :param datastoreId:Identifier for the data store to query
        :param taskOperationId:Identifier for the task operation of the data store
        """
        assert datastoreId is not None, MESSAGE_DATA_STORE_IDENTIFIER_REQUIRED
        assert taskOperationId is not None, MESSAGE_TASK_OPERATION_ID
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        taskresponse = requests.get(
            self.ecsAdminClient.url + LIST_SPECIFIC_TASK.format(datastoreId, taskOperationId),
            headers=headers, verify=False)
        self.commons.checkstatus(taskresponse)
        return taskresponse.json()

    def getBulkStore(self, datastoreIdList):
        """
        Retrieves list of resource (data store) representations based on input Ids
        :param datastoreIdList:Data store identifier List
        """
        assert isinstance(datastoreIdList, list), MESSAGE_DATA_STORE_ID_ARRAY_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        body = {"id": datastoreIdList}
        body = json.dumps(body)
        bulkResources = requests.post(self.ecsAdminClient.url + GET_BULK_RESOURCES, data=body,
                                      headers=headers, verify=False)
        self.commons.checkstatus(bulkResources)
        return bulkResources.json()
