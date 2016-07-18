"""
Created on Jul 6, 2015

@author: joshia7
"""
from ecsmgmt.util.messageconstants import *
import simplejson as json
import requests
from ecsmgmt.util.urlconstants import *
from ecsmgmt.util.commons import Commons


class StoragePool:
    """
    Class for provisioning and managing storage pools (previously called a virtual array or varray).
    """

    def __init__(self, client_instance, token):
        self.ecsAdminClient = client_instance
        self.token = token
        self.commons = Commons()

    def create_storage_pool(self, virtual_array_name=None, protected=False, cold_storage_enabled=False,
                            description=None):
        """
        Creates a storage pool with the specified details.
        :param virtual_array_name:Virtual array name
        :param protected: Set to true if varray is protected, false otherwise
        :param cold_storage_enabled: Set to true of varray has cold storage enabled, false otherwise
        :param description:Description
        """
        assert virtual_array_name is not None, MESSAGE_VIRTUAL_ARRAY_NAME_REQUIRED
        assert protected is not None, MESSAGE_IS_PROTECTED_REQUIRED
        assert isinstance(protected, bool), MESSAGE_IS_PROTECTED_SHOULD_BE_BOOLEAN
        assert isinstance(cold_storage_enabled, bool), MESSAGE_IS_PROTECTED_SHOULD_BE_BOOLEAN

        if description is None:
            description = "Storage Pool"
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        body = {"name": virtual_array_name,
                "isProtected": protected,
                "isColdStorageEnabled": cold_storage_enabled,
                "description": description}
        body = json.dumps(body)
        create_response = requests.post(
            self.ecsAdminClient.url + CREATE_STORAGE_POOL, headers=headers, data=body, verify=False)
        self.commons.checkstatus(create_response)
        return create_response.json()

    def deleteVirtualArray(self, storagePoolId):
        """
        Deletes the storage pool for the specified identifier.
        :param storagePoolId:Storage pool identifier to be deleted
        """
        assert storagePoolId is not None, MESSAGE_STORAGE_POOL_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteResponse = requests.delete(self.ecsAdminClient.url + DELETE_VARRAY.format(storagePoolId),
                                         headers=headers, verify=False)

        if self.commons.checkstatus(deleteResponse):
            return True
        else:
            return False

    def updateStoragePool(self, storagePoolId, virtualArrayName, isProtected, description=None):
        """
        Updates storage pool (previously called a virtual array or varray) for the specified identifier.
        :param storagePoolId:Storage pool identifier to be updated
        :param virtualArrayName:Name of storage pool to be updated
        :param isProtected:Set true if storage pool is protected, false otherwise
        :param description:Description. If no description found, then "Virtual Array" is used by default
        """
        assert virtualArrayName is not None, MESSAGE_VIRTUAL_ARRAY_NAME_REQUIRED
        assert isProtected is not None, MESSAGE_IS_PROTECTED_REQUIRED
        assert isinstance(isProtected, bool), MESSAGE_IS_PROTECTED_SHOULD_BE_BOOLEAN
        assert storagePoolId is not None, MESSAGE_STORAGE_POOL_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        if description is None:
            description = "Virtual Array"

        body = {"name": virtualArrayName,
                "isProtected": isProtected,
                "description": description}
        body = json.dumps(body)

        updateResponse = requests.put(self.ecsAdminClient.url + UPDATE_VARRAY.format(storagePoolId),
                                      headers=headers, data=body, verify=False)
        self.commons.checkstatus(updateResponse)
        return updateResponse.json()

    def getDetailsOfSpecifiedStoragePool(self, storagePoolId):
        """
        Gets the details for the specified storage pool.
        :param storagePoolId:Storage pool identifier to be retrieved
        """
        assert storagePoolId is not None, MESSAGE_STORAGE_POOL_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getDetailsResponse = requests.get(
            self.ecsAdminClient.url + GET_DETAILS_STORAGE_POOL.format(storagePoolId), headers=headers,
            verify=False)
        self.commons.checkstatus(getDetailsResponse)
        return getDetailsResponse.json()

    def getListOfStoragePools(self, vdc_id=None):
        """
        Gets a list of storage pools from the local VDC.
        :param vdc_id:virtual data center identifier for which list of storage poold is to be retrieved
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        body = {}
        if vdc_id is not None:
            body['vdc-id'] = vdc_id

        getListResponse = requests.get(self.ecsAdminClient.url + GET_LIST_OF_STORAGE_POOLS,
                                       headers=headers, params=body, verify=False)
        self.commons.checkstatus(getListResponse)
        return getListResponse.json()
