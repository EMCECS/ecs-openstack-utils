"""
Created on Jul 1, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


class BaseURL:
    """
    Class for creating and managing a Base URL
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def createBaseURL(self, baseURLName, baseURL, is_namespace_in_host):
        """
        Creates a Base URL with the given details.
        :param baseURLName:Base URL name
        :param baseURL:Base URL string
        :param is_namespace_in_host:Indicates whether the namespace is included in the URL
        """
        assert baseURLName is not None, MESSAGE_BASE_URL_NAME_REQUIRED
        assert baseURL is not None, MESSAGE_BASE_URL_VALUE_REQUIRED
        assert is_namespace_in_host is not None, MESSAGE_IS_NAMESPACE_IN_HOST_REQUIRED
        assert isinstance(is_namespace_in_host, bool), MESSAGE_IS_NAMESPACE_IN_HOST_NOT_VALID
        body = {"name": baseURLName,
                "base_url": baseURL,
                "is_namespace_in_host": is_namespace_in_host}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createresponse = requests.post(self.ecsAdminClient.url + CREATE_BASE_URL, headers=headers, data=body,
                                       verify=False)
        self.commons.checkstatus(createresponse)
        return createresponse.json()

    def deleteBaseURL(self, baseURLID):
        """
        Deletes the specified Base URL.
        :param baseURLID:Base URL identifier that needs to be deleted
        """
        assert baseURLID is not None, MESSAGE_BASEURL_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteresponse = requests.post(self.ecsAdminClient.url + DELETE_BASE_URL.format(baseURLID), headers=headers,
                                       verify=False)
        if self.commons.checkstatus(deleteresponse):
            return True
        else:
            return False

    def updateBaseURL(self, baseUrlToBeUpdate, baseURLName, baseURL, is_namespace_in_host):
        """

        :param baseUrlToBeUpdate:Base URL identifier that needs to be updated
        :param baseURLName:Base URL name
        :param baseURL:Base URL string
        :param is_namespace_in_host:Indicates whether the namespace is included in the URL
        """
        assert baseUrlToBeUpdate is not None, MESSAGE_BASEURL_IDENTIFIER_REQUIRED
        body = {}
        assert isinstance(is_namespace_in_host, bool), MESSAGE_IS_NAMESPACE_IN_HOST_NOT_VALID
        body['is_namespace_in_host'] = is_namespace_in_host
        body['name'] = baseURLName
        body['base_url'] = baseURL
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createresponse = requests.put(self.ecsAdminClient.url + UPDATE_BASE_URL.format(baseUrlToBeUpdate),
                                      headers=headers, data=body, verify=False)
        if self.commons.checkstatus(createresponse):
            return True
        else:
            return False

    def getSpecificBaseURL(self, baseURLID):
        """
        Gets details for the specified Base URL.
        :param baseURLID:Base URL identifier for the Base URL that needs to be retrieved
        """
        assert baseURLID is not None, MESSAGE_BASEURL_IDENTIFIER_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        baseURLdetails = requests.get(self.ecsAdminClient.url + GET_SPECIFIED_BASE_URL_DETAILS.format(baseURLID),
                                      headers=headers, verify=False)
        self.commons.checkstatus(baseURLdetails)
        return baseURLdetails.json()

    def getAllBaseURL(self):
        """
        Lists all configured Base URLs.
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        baseURLdetails = requests.get(self.ecsAdminClient.url + GET_ALL_BASE_URL, headers=headers, verify=False)
        self.commons.checkstatus(baseURLdetails)
        return baseURLdetails.json()
