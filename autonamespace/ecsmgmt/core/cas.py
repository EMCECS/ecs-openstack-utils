"""
Created on Jun 30, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


class CAS:
    """
    Class  for creating and manipulating CAS specific data for a user
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getCASSecret(self, UID):
        """
        Gets CAS secret for the specified user.
        :param UID:Valid user identifier to get the key from
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        casSecretInfo = requests.get(self.ecsAdminClient.url + GET_CAS_SECRET_KEY.format(UID), headers=headers,
                                     verify=False)
        self.commons.checkstatus(casSecretInfo)
        return casSecretInfo.json()

    def getCASSecretWithNamespace(self, namespace, UID):
        """
        Gets cas secret for the specified namespace and user identifier.
        :param namespace:Namespace for which to get CAS secret
        :param UID:Valid user identifier to get the key from
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        casSecretInfo = requests.get(self.ecsAdminClient.url + GET_CAS_SECRET_WITH_NAMESPACE.format(namespace, UID),
                                     headers=headers, verify=False)
        self.commons.checkstatus(casSecretInfo)
        return casSecretInfo.json()

    def updateCASSecret(self, namespace, UID, secret):
        """
        Creates or updates CAS secret for a specified user.
        :param namespace:Namespace identifier to associate with the CAS secret
        :param UID:Valid user identifier to update a secret for
        :param secret:Secret for the user
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert secret is not None, MESSAGE_SECRET_REQUIRED
        body = {"namespace": namespace, "secret": secret}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        cassecretresponse = requests.post(self.ecsAdminClient.url + UPDATE_CAS_SECRET.format(UID), headers=headers,
                                          data=body, verify=False)
        if self.commons.checkstatus(cassecretresponse):
            return True
        else:
            return False

    def getProfilePEA(self, namespace, UID):
        """
        Generates Pool Entry Authorization (PEA) file for specified user.
        :param namespace:Namespace id with CAS cluster
        :param UID:Valid user identifier to create PEA file
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        peaInfo = requests.get(self.ecsAdminClient.url + GET_PROFILE_PEA.format(namespace, UID), headers=headers,
                               verify=False)
        self.commons.checkstatus(peaInfo)
        return peaInfo.content

    def deactivateCASsecret(self, namespace, UID, secret):
        """
        Deletes CAS secret for a specified user identifier.
        :param namespace:Namespace identifier to associate with the CAS secret
        :param secret:Secret for the user
        :param UID:Valid user identifier to delete the key from
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert secret is not None, MESSAGE_SECRET_REQUIRED
        body = {"namespace": namespace, "secret": secret}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        cassecretresponse = requests.post(self.ecsAdminClient.url + DELETE_CAS_SECRET.format(UID), headers=headers,
                                          data=body, verify=False)
        if self.commons.checkstatus(cassecretresponse):
            return True
        else:
            return False

    def getDefaultBucket(self, namespace, UID):
        """
        Gets default bucket for the specified namespace and user identifier.
        :param namespace:Namespace from which to get bucket
        :param UID:Valid user identifier from which to get bucket
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        bucketResponse = requests.get(
            self.ecsAdminClient.url + GET_DEFAULT_BUCKET_WITH_NAMESPACE.format(namespace, UID), headers=headers,
            verify=False)
        self.commons.checkstatus(bucketResponse)
        return bucketResponse.json()

    def getDefaultBucketForUID(self, UID):
        """
        Gets default bucket for a specified user identifier.
        :param UID:Valid user identifier to get Bucket
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        bucketResponse = requests.get(self.ecsAdminClient.url + GET_DEFAULT_BUCKET_FOR_UID.format(UID), headers=headers,
                                      verify=False)
        self.commons.checkstatus(bucketResponse)
        return bucketResponse.json()

    def updateDefaultBucketWithNamespace(self, UID, namespace, bucket):
        """
        Updates default bucket the specified namespace and user identifier.
        :param UID:Valid user identifier to update default bucket
        :param namespace:Namespace required to update default bucket
        :param bucket:Name of the default bucket to be set
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        assert bucket is not None, MESSAGE_BUCKET_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        body = {"name": bucket}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        bucketresponse = requests.post(
            self.ecsAdminClient.url + UPDATE_DEFAULT_BUCKET_WITH_NAMESPACE.format(namespace, UID), headers=headers,
            data=body, verify=False)
        if self.commons.checkstatus(bucketresponse):
            return True
        else:
            return False

    def registerCAS(self, namespace):
        """
        Gets the CAS registered applications for a specified namespace.
        :param namespace:Namespace required to get CAS registered applications
        """

        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        resgitrationResponse = requests.get(self.ecsAdminClient.url + REGISTER_CAS_FOR_NAMESPACE.format(namespace),
                                            headers=headers, verify=False)
        self.commons.checkstatus(resgitrationResponse)
        return resgitrationResponse.json()

    def updateCASRegistration(self, namespace, UID, metadata):
        """
        Updates the CAS registered applications for a specified namespace and user identifier.
        :param namespace:Namespace for which to get metadata
        :param UID:User identifier for which to get metadata
        :param metadata:CAS metadata to be set for the user
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert metadata is not None, MESSAGE_METADATA_REQUIRED
        assert isinstance(metadata, dict), MESSAGE_METADATA_INVALID
        body = {"metadata": metadata}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        updateResponse = requests.post(
            self.ecsAdminClient.url + UPDATE_CAS_RESGISTERED_APPLICATION.format(namespace, UID), headers=headers,
            data=body, verify=False)
        if self.commons.checkstatus(updateResponse):
            return True
        else:
            return False

    def getCASUserMetadata(self, namespace, UID):
        """
        Gets the CAS user metadata for the specified namespace and user identifier.
        :param namespace:Namespace required to get metadata
        :param UID:User identifier for which to get metadata
        """

        assert UID is not None, MESSAGE_UID_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getMetadata = requests.get(self.ecsAdminClient.url + GET_CAS_USER_METADATA.format(namespace, UID),
                                   headers=headers, verify=False)
        self.commons.checkstatus(getMetadata)
        return getMetadata.json()
