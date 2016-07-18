"""
Created on Jul 7, 2015

@author: joshia7
"""

import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *

from array import array


class SecretKey:
    """
    API for assigning a secret key to a user so that they can use the object store. Assigning a secret key to a user
    creates an object user record.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getKeysForUser(self, uid):
        """
        Gets all secret keys for the specified user.
        :param uid:Valid user identifier for which to retrieve keys
        """
        assert uid is not None, MESSAGE_UID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        keyInfo = requests.get(self.ecsAdminClient.url + GET_KEYS_FOR_USER.format(uid), headers=headers, verify=False)
        self.commons.checkstatus(keyInfo)
        return keyInfo.json()

    def getAllKeys(self, uid, namespace):
        """
        Gets all secret keys for the specified user and namespace.
        :param uid:Valid user identifier for which to retrieve the keys
        :param namespace:Namespace to which user belongs
        """
        assert uid is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        keyInfo = requests.get(self.ecsAdminClient.url + GET_ALL_KEY_FOR_USER.format(uid, namespace), headers=headers,
                               verify=False)
        self.commons.checkstatus(keyInfo)
        return keyInfo.json()

    def createKeyForUser(self, uid, existing_key_expiry_time_mins, namespace, secretkey):
        """
        Creates a secret key for the specified user.
        :param uid:Valid user identifier to create a key for
        :param existing_key_expiry_time_mins:Expiry time in minutes for the secret key
        :param namespace:Namespace for User qualifier
        :param secretkey:Secret key associated with this user
        """
        assert uid is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert secretkey is not None, MESSAGE_SECRET_KEYS_REQUIRED
        assert existing_key_expiry_time_mins is not None, MESSAGE_EXPIRY_TIME_FOR_KEY_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        body = {"existing_key_expiry_time_mins": existing_key_expiry_time_mins,
                "namespace": namespace,
                "secretkey": secretkey}
        body = json.dumps(body)
        createKeyResponse = requests.post(self.ecsAdminClient.url + CREATE_NEW_KEY.format(uid), data=body,
                                          headers=headers, verify=False)
        self.commons.checkstatus(createKeyResponse)
        return createKeyResponse.json()

    def deleteKeyForUser(self, uid, secretkey, namespace):
        """
        Deletes all secret keys for the specific user.
        :param uid:Valid user identifier for which to delete the keys
        :param secretkey:Expiry time/date for the secret key
        :param namespace:User qualifier if the User Scope is NAMESPACE
        """
        assert uid is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert secretkey is not None, MESSAGE_SECRET_KEYS_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        body = {"namespace": namespace,
                "secretkey": secretkey}
        body = json.dumps(body)
        deleteResponse = requests.post(self.ecsAdminClient.url + DELETE_USER_KEY.format(uid), data=body,
                                       headers=headers, verify=False)
        if self.commons.checkstatus(deleteResponse):
            return True
        else:
            return False
