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

class Capacity:
    """
    Class for for retrieving the current managed capacity.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getCapacity(self):
        """
        Gets the provisioned and available capacity of the cluster in GBs
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        capacityresponse = requests.get(self.ecsAdminClient.url + GET_CAPACITY, headers=headers, verify=False)
        self.commons.checkstatus(capacityresponse)
        return capacityresponse.json()

    def getClusterCapacity(self, vArrayId):
        """
        Gets the cluster capacity of the specified storage pool. The details includes the provisioned capacity in GB
        and available capacity in GB.
        :param vArrayId:Storage pool identifier for which to retrieve capacity
        """
        assert vArrayId is not None, MESSAGE_STORAGE_POOL_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        clustercapacityresponse = requests.get(self.ecsAdminClient.url + GET_CLUSTER_CAPACITY.format(vArrayId),
                                               headers=headers, verify=False)
        self.commons.checkstatus(clustercapacityresponse)
        return clustercapacityresponse.json()
