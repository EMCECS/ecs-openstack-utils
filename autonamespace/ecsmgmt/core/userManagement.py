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


class UserManagement:
    """
    Class for creating and managing local management users.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def createLocalUserInfo(self, userId, password, isSystemAdmin, isSystemMonitor):
        """
        Creates local users for the VDC
        :param userId:Management user id
        :param password:Password for the management user
        :param isSystemAdmin:If set to true, assigns the management user to the System Admin role
        :param isSystemMonitor:If set to true, assigns the management user to the System Monitor role
        """
        assert userId is not None, MESSAGE_USER_ID_REQUIRED
        assert password is not None, MESSAGE_PASSWORD_REQUIRED
        assert isSystemAdmin is not None, MESSAGE_IS_SYSTEM_ADMIN_REQUIRED
        assert isSystemMonitor is not None, MESSAGE_IS_SYSTEM_MONITOR_REQUIRED
        assert isinstance(isSystemAdmin, bool), MESSAGE_IS_SYSTEM_ADMIN_SHOULD_BE_BOOLEAN
        assert isinstance(isSystemMonitor, bool), MESSAGE_IS_SYSTEM_MONITOR_SHOULD_BE_BOOLEAN
        body = {"userId": userId,
                "password": password,
                "isSystemAdmin": isSystemAdmin,
                "isSystemMonitor": isSystemMonitor}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userInfoResponse = requests.post(self.ecsAdminClient.url + CREATE_LOCAL_VDC_USER_INFO, headers=headers,
                                         data=body, verify=False)
        self.commons.checkstatus(userInfoResponse)
        return userInfoResponse.json()

    def deleteLocalUserInfo(self, userId):
        """
        Deletes local management user information for the specified user identifier.
        :param userId:User identifier for which local user information needs to be deleted.
        """
        assert userId is not None, MESSAGE_USER_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteresponse = requests.post(self.ecsAdminClient.url + DELETE_LOCAL_VDC_USER_INFO.format(userId),
                                       headers=headers, verify=False)
        if self.commons.checkstatus(deleteresponse):
            return True
        else:
            return False

    def updateLocalUserInfo(self, userId, password, isSystemAdmin, isSystemMonitor):
        """
        Updates user details for the specified local management user.
        :param userId:User identifier for which local user information needs to be updated.
        :param password:Password for the management user
        :param isSystemAdmin:Assigns or removes management user to /from System Admin role
        :param isSystemMonitor:Assigns or removes management user to /from System Monitor role.
        """
        assert userId is not None, MESSAGE_USER_ID_REQUIRED
        assert password is not None, MESSAGE_PASSWORD_REQUIRED
        assert isSystemAdmin is not None, MESSAGE_IS_SYSTEM_ADMIN_REQUIRED
        assert isSystemMonitor is not None, MESSAGE_IS_SYSTEM_MONITOR_REQUIRED
        assert isinstance(isSystemAdmin, bool), MESSAGE_IS_SYSTEM_ADMIN_SHOULD_BE_BOOLEAN
        assert isinstance(isSystemMonitor, bool), MESSAGE_IS_SYSTEM_MONITOR_SHOULD_BE_BOOLEAN
        body = {"userId": userId,
                "password": password,
                "isSystemAdmin": isSystemAdmin,
                "isSystemMonitor": isSystemMonitor}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userInfoResponse = requests.put(self.ecsAdminClient.url + UPDATE_LOCAL_VDC_USER_INFO, headers=headers,
                                        data=body, verify=False)
        if self.commons.checkstatus(userInfoResponse):
            return True
        else:
            return False

    def getLocalUserInfo(self, userId):
        """
        Gets details for the specified local management user.
        :param userId:User identifier for which local user information needs to be retrieved
        """
        assert userId is not None, MESSAGE_USER_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userInfoResponse = requests.post(self.ecsAdminClient.url + GET_LOCAL_VDC_USER_INFO.format(userId),
                                         headers=headers, verify=False)
        self.commons.checkstatus(userInfoResponse)
        return userInfoResponse.json()

    def getAllUserInfo(self):
        """
        Lists all local management users
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        userInfoResponse = requests.post(self.ecsAdminClient.url + LIST_LOCAL_VDC_USERS, headers=headers, verify=False)
        self.commons.checkstatus(userInfoResponse)
        return userInfoResponse.json()
