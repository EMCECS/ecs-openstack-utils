"""
Created on Jul 1, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


# from ECSAdminClient import ECSAdminClient

class DashBoard:
    """
    Class to retrieve monitoring data for requests from the portal monitoring dashboard
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getLocalVDCDetails(self):
        """
        Gets the local VDC details
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        vdcresponse = requests.get(self.ecsAdminClient.url + GET_LOCAL_VDS_DETAILS, headers=headers, verify=False)
        self.commons.checkstatus(vdcresponse)
        return vdcresponse.json()

    def getLocalVDCReplicationGroups(self):
        """
        Gets the local VDC replication groups details
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        vdcresponse = requests.get(self.ecsAdminClient.url + GET_LOCAL_VDC_REPLICATION_GROUPS, headers=headers,
                                   verify=False)
        self.commons.checkstatus(vdcresponse)
        return vdcresponse.json()

    def getReplicationGroupFailedLinks(self):
        """
        Gets the local VDC replication groups failed links details
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        failedLinks = requests.get(self.ecsAdminClient.url + GET_LOCAL_REPLICATION_FAILED_LINKS, headers=headers,
                                   verify=False)
        self.commons.checkstatus(failedLinks)
        return failedLinks.json()

    def getLocalVDCStoragePools(self):
        """
        Gets the local VDC storage pools details
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        storagePools = requests.get(self.ecsAdminClient.url + GET_LOCAL_VDC_STORAGE_DETAILS, headers=headers,
                                    verify=False)
        self.commons.checkstatus(storagePools)
        return storagePools.json()

    def getLocalVDCNodeDetails(self):
        """
        Gets the local VDC nodes details
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        nodeDetails = requests.get(self.ecsAdminClient.url + GET_LOCAL_ZONE_NODES, headers=headers, verify=False)
        self.commons.checkstatus(nodeDetails)
        return nodeDetails.json()

    def getStoragePoolDetails(self, storagePoolId):
        """
        Gets the storage pool details.
        :param storagePoolId:Storage pool identifier
        """
        assert storagePoolId is not None, MESSAGE_STORAGE_POOL_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        storagePools = requests.get(self.ecsAdminClient.url + GET_STORAGE_POOL_DETAILS.format(storagePoolId),
                                    headers=headers, verify=False)
        self.commons.checkstatus(storagePools)
        return storagePools.json()

    def getNodeInstanceDetails(self, nodeInstance):
        """
        Gets the node instance details
        :param nodeInstance:Identity of the Node
        """
        assert nodeInstance is not None, MESSAGE_NODE_INSTANCE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        url = self.ecsAdminClient.url + GET_NODE_INSTANCE_DETAILS.format(nodeInstance)
        print "Url is %s", url
        nodeInstanceDetails = requests.get(self.ecsAdminClient.url + GET_NODE_INSTANCE_DETAILS.format(nodeInstance),
                                           headers=headers, verify=False)
        self.commons.checkstatus(nodeInstanceDetails)
        return nodeInstanceDetails.json()

    def getDiskInstanceDetails(self, diskId):
        """
        Gets the disk instance details.
        :param diskId:Identity of the disk
        """
        assert diskId is not None, MESSAGE_DISK_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        diskInstanceDetails = requests.get(self.ecsAdminClient.url + GET_DISK_INSTANCE_DETAILS.format(diskId),
                                           headers=headers, verify=False)
        self.commons.checkstatus(diskInstanceDetails)
        return diskInstanceDetails.json()

    def getProcessInstanceDetails(self, processInstance):
        """
        Gets the process instance details.
        :param processInstance: Identity of the process
        """
        assert processInstance is not None, MESSAGE_PROCESS_INSTANCE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        processDetails = requests.get(self.ecsAdminClient.url + GET_PROCESS_INSTANCE_DETAILS.format(processInstance),
                                      headers=headers, verify=False)
        self.commons.checkstatus(processDetails)
        return processDetails.json()

    def getNodeInstanceProcessDetails(self, nodeInstance):
        """
        Gets the node instance process details.
        :param nodeInstance:Identity of the Node
        """
        assert nodeInstance is not None, MESSAGE_NODE_INSTANCE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        processDetails = requests.get(self.ecsAdminClient.url + GET_NODE_INSTANCE_PROCESS_DETAILS.format(nodeInstance),
                                      headers=headers, verify=False)
        self.commons.checkstatus(processDetails)
        return processDetails.json()

    def getNodeInstanceDiskDetails(self, nodeInstance):
        """
        Gets node instance disk details
        :param nodeInstance:Identity of the Node
        """
        assert nodeInstance is not None, MESSAGE_NODE_INSTANCE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        storagePoolDetails = requests.get(self.ecsAdminClient.url + GET_NODE_INSTANCE_DISK_DETAILS.format(nodeInstance),
                                          headers=headers, verify=False)
        self.commons.checkstatus(storagePoolDetails)
        return storagePoolDetails.json()

    def getStoragePoolNodeDetails(self, storagePoolId):
        """
        Gets the storage pool node details.
        :param storagePoolId:Identity of the storage pool
        """
        assert storagePoolId is not None, MESSAGE_STORAGE_POOL_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        storagePoolNodeDetails = requests.get(
            self.ecsAdminClient.url + GET_STORAGE_POOL_NODE_DETAILS.format(storagePoolId), headers=headers,
            verify=False)
        self.commons.checkstatus(storagePoolNodeDetails)
        return storagePoolNodeDetails.json()

    def getReplicationGroupBootStrapDetails(self):
        """
        Gets the local VDC replication group bootstrap links details.
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        bootstrapDetails = requests.get(self.ecsAdminClient.url + GET_VDC_REPLICATION_BOOTSTRAP_DETAILS,
                                        headers=headers, verify=False)
        self.commons.checkstatus(bootstrapDetails)
        return bootstrapDetails.json()

    def getReplicationInstanceDetails(self, replicationIdentifier):
        """
        Gets the replication group instance details.
        :param replicationIdentifier:Replication group identifier
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        url = self.ecsAdminClient.url + GET_REPLICATION_GROUPS_INSTANCE_DETAILS.format(replicationIdentifier)
        print url
        replicationInstance = requests.get(
            self.ecsAdminClient.url + GET_REPLICATION_GROUPS_INSTANCE_DETAILS.format(replicationIdentifier),
            headers=headers, verify=False)
        self.commons.checkstatus(replicationInstance)
        return replicationInstance.json()

    def getReplicationGroupLinks(self, replicationIdentifier):
        """
        Gets the replication group link instance details
        :param replicationIdentifier:Replication group identifier
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        url = self.ecsAdminClient.url + GET_REPLICATION_GROUPS_LINK_INSTANCE_DETAILS.format(replicationIdentifier)
        print url
        replicationGroupLinks = requests.get(
            self.ecsAdminClient.url + GET_REPLICATION_GROUPS_LINK_INSTANCE_DETAILS.format(replicationIdentifier),
            headers=headers, verify=False)
        self.commons.checkstatus(replicationGroupLinks)
        return replicationGroupLinks.json()

    def getReplicationGroupAssoLinks(self, replicationIdentifier):
        """
        Gets the replication group instance associated link details.
        :param replicationIdentifier:Replication group identifier
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        replicationGroupAssoLinks = requests.get(
            self.ecsAdminClient.url + GET_REPLICATION_GROUP_INSTANCE_ASSOCIATED_LINK_DETAILS.format(
                replicationIdentifier), headers=headers, verify=False)
        self.commons.checkstatus(replicationGroupAssoLinks)
        return replicationGroupAssoLinks.json()
