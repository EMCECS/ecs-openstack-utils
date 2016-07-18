"""
Created on Jun 24, 2015

@author: joshia7
"""

import requests
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *
from requests.auth import HTTPBasicAuth


class Authentication(object):
    """
    The Class used for Authentication Purpose,used for generation of token and to logout of the ECS Management API
    """
    headers = {'Accept': 'application/json'}

    def __init__(self, client_instance):
        """
         Constructor for the Authentication Class
        :param client_instance:Object Instance of ECSAdminClient
        """
        self.ecsAdminClient = client_instance

    def login(self, user_name, password):
        """
        Used for the Generation of token
        :param user_name:UserName
        :param password:Password
        """
        assert user_name is not None, MESSAGE_USERNAME_REQUIRED
        assert password is not None, MESSAGE_PASSWORD_REQUIRED
        login_response = requests.get(self.ecsAdminClient.url + LOGIN, headers=self.headers, verify=False,
                                      auth=HTTPBasicAuth(user_name, password))
        common = Commons()
        common.checkstatus(login_response)
        token = login_response.headers["x-sds-auth-token"]
        return token

    def logout(self, token):
        """
        Used to logout
        :param token:Authentication Token
        """
        assert token is not None, MESSAGE_TOKEN_REQUIRED
        self.headers['x-sds-auth-token'] = token
        logout_response = requests.get(self.ecsAdminClient.url + LOGOUT, headers=self.headers,
                                       verify=False)
        return logout_response
