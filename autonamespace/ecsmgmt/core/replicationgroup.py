"""
Created on Jul 1, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *

from array import array
from __builtin__ import True


class ReplicationGroup:
    """
    Class for provisioning and managing replication groups (previously called virtual pools or vpools).
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getReplicationGroups(self):
        """
        Lists all configured replication groups
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        replicationgroups = requests.get(self.ecsAdminClient.url + GET_REPLICATION_GROUPS, headers=headers,
                                         verify=False)
        self.commons.checkstatus(replicationgroups)
        return replicationgroups.json()

    def getSpecificReplicationGroup(self, replicationIdentifier):
        """
        Gets the details for the specified replication group.
        :param replicationIdentifier:Replication group identifier for which details needs to be retrieved
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        replicationgroupdetails = requests.get(
            self.ecsAdminClient.url + GET_SPECIFIED_REPLICATION_GROUP.format(replicationIdentifier), headers=headers,
            verify=False)
        self.commons.checkstatus(replicationgroupdetails)
        return replicationgroupdetails.json()

    def updateReplicationGroup(self, replicationIdentifier, name, description, allowAllNamespaces):
        """
        Updates the name and description for a replication group
        :param name:Name
        :param replicationIdentifier:Replication group identifier for which details needs to be updated
        :param description:Description
        :param allowAllNamespaces:Indicates whether all namesapces can access the replication group
        """
        assert name is not None, MESSAGE_REPLICATION_GROUP_NAME_REQUIRED
        assert description is not None, MESSAGE_REPLICATION_GROUP_DESCRIPTION_REQUIRED
        assert allowAllNamespaces is not None, MESSAGE_ALLOW_ALL_NAMESPACE_REQUIRED
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        body = {"name": name,
                "description": description,
                "allowAllNamespaces": allowAllNamespaces}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        replicationgroups = requests.put(
            self.ecsAdminClient.url + UPDATE_REPLICATION_GROUP.format(replicationIdentifier), data=body,
            headers=headers, verify=False)
        if self.commons.checkstatus(replicationgroups):
            return True
        else:
            return False

    def removeFromReplicationGroup(self, replicationIdentifier, varrays):
        """
        Deletes a storage pool (VDC:storage pool tuple) from a specified replication group.
        :param replicationIdentifier:Replication group identifier for which storage pool needs to be removed
        :param varrays:array of dict with key as "names" and values as "values"
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        assert isinstance(varrays, dict), MESSAGE_VARRAYS_SHOULD_BE_DICT
        params = dict()
        listOfVarrays = []
        for key, value in varrays.items():
            params = {"names": key, "value": value}
            listOfVarrays.append(params)

        body = {"mappings": listOfVarrays}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteresponse = requests.put(
            self.ecsAdminClient.url + REMOVE_FROM_REPLICATION_GROUP.format(replicationIdentifier), data=body,
            headers=headers, verify=False)
        if self.commons.checkstatus(deleteresponse):
            return True
        else:
            return False

    def removeReplicationGroup(self, replicationIdentifier):
        """
        Deletes a specified replication group
        :param replicationIdentifier:Replication group to be deleted
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED

        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteresponse = requests.post(self.ecsAdminClient.url + REMOVE_REPLICATION_GROUP.format(replicationIdentifier),
                                       headers=headers, verify=False)
        if self.commons.checkstatus(deleteresponse):
            return True
        else:
            return False

    def addToReplicationGroup(self, replicationIdentifier, varrays):
        """
        Adds one or more storage pools (as VDC:storage pool tuples) to the specified replication group.
        :param replicationIdentifier:Replication group identifier for which storage pool needs to be added
        :param varrays:array of dict with key as "names" and values as "values"
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        assert isinstance(varrays, dict), MESSAGE_VARRAYS_SHOULD_BE_DICT
        params = dict()
        listOfVarrays = []
        for key, value in varrays.items():
            params = {"names": key, "value": value}
            listOfVarrays.append(params)

        body = {"mappings": listOfVarrays}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        addResponse = requests.put(self.ecsAdminClient.url + ADD_STORAGE_POOL.format(replicationIdentifier),
                                   headers=headers, data=body, verify=False)
        if self.commons.checkstatus(addResponse):
            return True
        else:
            return False

    def createReplicationGroups(self, replicationIdentifier, name, description, isAllowAllNamespaces,
                                zone_mappings=None, ):
        """
        Creates a replication group that includes the specified storage pools (VDC:storage pool tuple).
        :param replicationIdentifier:Identifier for this replication group
        :param name:Unique name identifying the replication group
        :param description:Description of this replication group
        :param isAllowAllNamespaces:Indicates whether all namespaces can access the replication group
        :param zone_mappings:Array of dict with key:"name" ,value:"value"
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        assert name is not None, MESSAGE_REPLICATION_GROUP_NAME_REQUIRED
        assert description is not None, MESSAGE_REPLICATION_GROUP_DESCRIPTION_REQUIRED
        assert isAllowAllNamespaces is not None, MESSAGE_ALLOW_ALL_NAMESPACE_REQUIRED
        body = {}
        if zone_mappings is not None:
            assert isinstance(zone_mappings, dict), MESSAGE_ZONE_MAPPINGS_SHOULD_BE_DICT
            params = dict()
            listOfVarrays = []
            for key, value in zone_mappings.items():
                params = {"names": key, "value": value}
                listOfVarrays.append(params)

            body['zone_mappings'] = listOfVarrays

        body = {"id": replicationIdentifier,
                "name": name,
                "description": description,
                "isAllowAllNamespaces": isAllowAllNamespaces}
        body = json.dumps(body)

        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createResponse = requests.post(self.ecsAdminClient.url + CREATE_REPLICATION_GROUP, headers=headers, data=body,
                                       verify=False)
        self.commons.checkstatus(createResponse)
        return createResponse.json()
