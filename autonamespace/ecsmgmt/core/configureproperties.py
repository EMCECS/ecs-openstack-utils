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

class ConfigureProperties:
    """
    for managing system configuration settings
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getProperties(self):
        """
        Gets the configuration properties for a specified category
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        propertyresponse = requests.get(self.ecsAdminClient.url + GET_PROPERTIES, headers=headers, verify=False)
        self.commons.checkstatus(propertyresponse)
        return propertyresponse.json()

    def getPropertiesMetadata(self):
        """
        Gets the meta data configuration properties for the system
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        propertyMetadataResponse = requests.get(self.ecsAdminClient.url + GET_PROPERTY_METADATA, headers=headers,
                                                verify=False)
        self.commons.checkstatus(propertyMetadataResponse)
        return propertyMetadataResponse.json()

    def setConfigProperties(self, properties):
        """
        Sets the configuration properties for the system
        :param properties:Configuration properties for the given category
        """
        assert properties is not None, MESSAGE_PROPERTIES_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        body = {"properties": properties}
        body = json.dumps(body)
        updateResponse = requests.put(self.ecsAdminClient.url + SET_PROPERTIES, data=body, headers=headers,
                                      verify=False)
        if self.commons.checkstatus(updateResponse):
            return True
        else:
            return False
