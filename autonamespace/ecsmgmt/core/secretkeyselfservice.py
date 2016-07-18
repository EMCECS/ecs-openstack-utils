"""
Created on Jul 7, 2015

@author: joshia7
"""

import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *
# from ECSAdminClient import ECSAdminClient
from array import array


class SecretKeySelfService:
    """
    Class that enables an authenticated user to request a secret key that can be used to access the object store.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getAllSecretKeys(self):
        """
        Gets all configured secret keys for the user account that makes the request
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        keyInfo = requests.get(self.ecsAdminClient.url + GET_ALL_SECRET_KEYS, headers=headers, verify=False)
        self.commons.checkstatus(keyInfo)
        return keyInfo.json()

    def createSecretKey(self, existing_key_expiry_time_mins):
        """
        Creates a secret key for the authenticated user that makes the request
        :param existing_key_expiry_time_mins:Expiry time/date for the secret key in minutes
        """
        assert existing_key_expiry_time_mins is not None, MESSAGE_EXPIRY_TIME_FOR_KEY_REQUIRED
        body = {"existing_key_expiry_time_mins": existing_key_expiry_time_mins}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        keyinfo = requests.post(self.ecsAdminClient.url + CREATE_SECRET_KEY, headers=headers, data=body, verify=False)
        self.commons.checkstatus(keyinfo)
        return keyinfo.json()

    def deleteSecretKey(self, secret_key):
        """
        Deletes the specified secret key for the authenticated user that makes the request
        :param secret_key:Secret key to be deleted
        """
        assert secret_key is not None, MESSAGE_SECRET_KEYS_REQUIRED
        body = {"secret_key": secret_key}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        keyinfo = requests.post(self.ecsAdminClient.url + DELETE_SECRET_KEY, headers=headers, data=body, verify=False)
        self.commons.checkstatus(keyinfo)
        return keyinfo.json()
