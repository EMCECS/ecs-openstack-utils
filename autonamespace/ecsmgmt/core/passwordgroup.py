"""
Created on Jul 7, 2015

@author: joshia7
"""

import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *
import array


class PasswordGroup:
    """
    Class for for for creating and managing Swift passwords and assigning Swift users to groups
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getUserGroupForUser(self, uid):
        """
        Gets all user groups for a specified user identifier.
        :param uid:User identifier required to get all user groups
        """
        assert uid is not None, MESSAGE_UID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userGroupInfo = requests.get(self.ecsAdminClient.url + GET_USER_GROUPS.format(uid), headers=headers,
                                     verify=False)
        self.commons.checkstatus(userGroupInfo)
        return userGroupInfo.json()

    def getAlluserGroups(self, uid, namespace):
        """
        Gets all user groups for a specified user identifier and namespace
        :param uid:User identifier from which to get all user groups
        :param namespace:Namespace to which user belongs
        """
        assert uid is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userGroupInfo = requests.get(self.ecsAdminClient.url + GET_ALL_USER_GROUPS.format(uid, namespace),
                                     headers=headers, verify=False)
        self.commons.checkstatus(userGroupInfo)
        return userGroupInfo.json()

    def createPassword(self, groupList, namespace, uid, password):
        """
        Creates user, password and group for a specific user.
        :param groupList:List of ADMIN groups for the user
        :param namespace:Namespace of the object stores
        :param uid:Valid user identifier to create a password for
        :param password:Password for the user
        """
        assert password is not None, MESSAGE_PASSWORD_REQUIRED
        assert uid is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert groupList is not None, MESSAGE_GROUPS_LIST_REQUIRED
        assert isinstance(groupList, array), MESSAGE_GROUPS_LIST_SHOULD_BE_ARRAY
        body = {"password": password,
                "group_list": groupList,
                "namespace": namespace}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createPasswordResponse = requests.put(self.ecsAdminClient.url + CREATE_PASSWORD.format(uid), headers=headers,
                                              data=body, verify=False)
        if self.commons.checkstatus(createPasswordResponse):
            return True
        else:
            return False

    def updatePassword(self, uid, namespace, groupList, password):
        """
        Updates user, password and group info for a specific user identifier.
        :param uid:Valid user identifier for which to update password group
        :param namespace:Namespace associated with the user user as userId qualifier if the User Scope is NAMESPACE
        :param groupList:List of groups for the user
        :param password:Password for the user
        """
        assert password is not None, MESSAGE_PASSWORD_REQUIRED
        assert uid is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert groupList is not None, MESSAGE_GROUPS_LIST_REQUIRED
        assert isinstance(groupList, array), MESSAGE_GROUPS_LIST_SHOULD_BE_ARRAY
        body = {"password": password,
                "group_list": groupList,
                "namespace": namespace}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createPasswordResponse = requests.post(self.ecsAdminClient.url + UPDATE_PASSWORD.format(uid), headers=headers,
                                               data=body, verify=False)
        if self.commons.checkstatus(createPasswordResponse):
            return True
        else:
            return False

    def removePassword(self, uid, namespace):
        """
        Deletes password group for a specified user.
        :param uid:Valid user identifier to delete password group
        :param namespace:Namespace identifier to associate with the user
        """
        assert uid is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        body = {"namespace": namespace}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteResponse = requests.post(self.ecsAdminClient.url + DELETE_PASSWORD_GROUP, headers=headers, data=body,
                                       verify=False)
        if self.commons.checkstatus(deleteResponse):
            return True
        else:
            return False
