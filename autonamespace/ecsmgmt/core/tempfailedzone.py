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

class TempFailedZone:
    """
    Class for managing temp failed zones.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getAllFailedZones(self):
        """
        Gets all the configured temp failed zones
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        failedZones = requests.get(self.ecsAdminClient.url + GET_ALL_TEMP_FALIED_ZONE, headers=headers, verify=False)
        self.commons.checkstatus(failedZones)
        return failedZones.json()

    def getFailedZoneForReplicationGroup(self, replicationIdentifier):
        """
        Gets all the temp failed zones for the specified replication group identifier.
        :param replicationIdentifier:Replication group id to retrieve details
        """
        assert replicationIdentifier is not None, MESSAGE_REPLICATION_GROUP_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        failedZone = requests.get(
            self.ecsAdminClient.url + GET_FAILED_ZONE_FOR_REPLICATION_GROUPS.format(replicationIdentifier),
            headers=headers, verify=False)
        self.commons.checkstatus(failedZone)
        return failedZone.json()
