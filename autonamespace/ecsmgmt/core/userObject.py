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


class UserObject:
    """
    Class for for creating and managing users associated with a namespace.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def createUserForNamespace(self, user, namespace, tags):
        """
        Creates a user for a specified namespace
        :param user:User to be created
        :param namespace:Namespace identifier to associate with the user
        :param tags:A list of arbitrary tags to assign to the new user.
        """
        assert user is not None, MESSAGE_USERNAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert tags is not None, MESSAGE_TAGS_REQUIRED
        assert isinstance(tags, array), MESSAGE_TAGS_SHOULD_BE_ARRAY
        body = {"user": user, "namespace": namespace, "tags": tags}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createresponse = requests.post(self.ecsAdminClient.url + CREATE_USER_FOR_NAMESPACE, data=body, headers=headers,
                                       verify=False)
        self.commons.checkstatus(createresponse)
        return createresponse.json()

    def deleteUser(self, user, namespace):
        """
        Deletes the specified user and its secret keys
        :param user:User to be deleted
        :param namespace:Namespace identifier to associate with the user
        """
        assert user is not None, MESSAGE_USERNAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        body = {"user": user, "namespace": namespace}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteresponse = requests.post(self.ecsAdminClient.url + DELETE_SPECIFIED_USER, data=body, headers=headers,
                                       verify=False)
        if self.commons.checkstatus(deleteresponse):
            return True
        else:
            return False

    def userDetails(self, uid, namespace=None):
        """
        Gets user details for the specified user.
        :param uid:Valid user identifier
        :param namespace:Optional when userscope is GLOBAL. Required when userscope is NAMESPACE. The namespace to
        which user belong
        """
        assert uid is not None, MESSAGE_USER_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userDetails = ""
        if namespace is not None:
            params = {"namespace": namespace}
            userDetails = requests.get(self.ecsAdminClient.url + GET_USER_DETAILS.format(uid), headers=headers,
                                       params=params, verify=False)
        else:
            userDetails = requests.get(self.ecsAdminClient.url + GET_USER_DETAILS.format(uid), headers=headers,
                                       verify=False)

        self.commons.checkstatus(userDetails)
        return userDetails.json()

    def getAllUsers(self):
        """
        Gets identifiers for all configured users
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userDetails = requests.get(self.ecsAdminClient.url + GET_USER_IDENTIFIERS, headers=headers, verify=False)
        self.commons.checkstatus(userDetails)
        return userDetails.json()

    def getUsersForNamespace(self, namespace):
        """
        Gets all users for the specified namespace.
        :param namespace:Namespace for which users should be returned
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userDetails = requests.get(self.ecsAdminClient.url + GET_USER_INDENTIFIERS_FOR_NAMESPACE.format(namespace),
                                   headers=headers, verify=False)
        self.commons.checkstatus(userDetails)
        return userDetails.json()

    def setUserLock(self, user, namespace, isLocked):
        """
        Locks or unlocks the specified user
        :param user:User name to be locked/unlocked
        :param namespace:Namespace for this user
        :param isLocked:Set true if user needs to be is to be locked, false otherwise
        """
        assert user is not None, MESSAGE_USERNAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert isLocked is not None, MESSAGE_IS_LOCK_REQUIRED
        assert isinstance(isLocked, bool), MESSAGE_IS_LOCK_NOT_VALID
        body = {"user": user, "namespace": namespace, "isLocked": isLocked}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        lockResponse = requests.put(self.ecsAdminClient.url + LOCK_SPECIFIED_USER, data=body, headers=headers,
                                    verify=False)
        if self.commons.checkstatus(lockResponse):
            return True
        else:
            return False

    def getUserLockDetails(self, userName, namespace):
        """
        Gets the user lock state for the specified user belonging to the specified namespace.
        :param userName:User name for which user lock status should be returned
        :param namespace:Namespace to which user belongs
        """
        assert userName is not None, MESSAGE_USERNAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        lockDetails = requests.get(
            self.ecsAdminClient.url + GET_LOCK_DETAILS_FOR_USER_NAMESPACE.format(userName, namespace), headers=headers,
            verify=False)

        self.commons.checkstatus(lockDetails)
        return lockDetails.json()

    def getLockStateForUser(self, userName):
        """
        Gets the user lock state for the specified user
        :param userName:User name for which user lock details should be returned
        """
        assert userName is not None, MESSAGE_USERNAME_REQUIRED

        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        lockDetails = requests.get(self.ecsAdminClient.url + GET_LOCK_FOR_USER.format(userName), headers=headers,
                                   verify=False)

        self.commons.checkstatus(lockDetails)
        return lockDetails.json()
