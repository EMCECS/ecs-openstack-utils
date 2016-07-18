"""
Created on Jul 6, 2015

@author: joshia7
"""

import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


class Node:
    """
    Class for fetching data nodes in the cluster.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getDataNodes(self):
        """
        Gets the data nodes that are currently configured in the cluster
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        nodeList = requests.get(self.ecsAdminClient.url + GET_DATA_NODES, headers=headers, verify=False)
        self.commons.checkstatus(nodeList)
        return nodeList.json()
