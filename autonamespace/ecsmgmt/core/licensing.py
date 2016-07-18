"""
Created on Jul 1, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


class Licensing:
    """
    Class for managing ECS licenses.
    """

    def __init__(self, client, token):
        self.ecsAdminClient = client
        self.token = token
        self.commons = Commons()

    def get_license_information(self):
        """
        Gets license information
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        license_response = requests.get(
            self.ecsAdminClient.url + GET_LICENSE_INFORMATION, headers=headers, verify=False)
        self.commons.checkstatus(license_response)
        return license_response.json()

    def add_license(self, license_content):
        """
        Adds specified license.
        :param license_content:License Information
        :returns: True if successful
        """
        assert license_content is not None, MESSAGE_LIMIT_REQUIRED
        #         body={"license_feature":license_content}
        body = json.dumps(license_content)
        headers = {'x-sds-auth-token': self.token,
                   'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        add_response = requests.post(
            self.ecsAdminClient.url + ADD_LICENSE, data=body, headers=headers, verify=False)
        return self.commons.checkstatus(add_response)
