"""
Created on Jul 2, 2015

@author: joshia7
"""

import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


# from ECSAdminClient import ECSAdminClient

# from

class Bucket:
    """
    Class for provisioning and managing buckets
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def createBucket(self, name, namespace, filesystem_enabled, is_stale_allowed, head_type=None, vpool=None):
        """
        Creates a bucket in which users can create objects.
        :param name:Bucket name
        :param namespace:Namespace associated with the user/tenant that is allowed to access the bucket
        :param filesystem_enabled:Flag indicating whether file-system is enabled for this bucket
        :param is_stale_allowed:tag to allow stale data in bucket
        :param head_type:Indicates the object head type that is allowed to access the bucket
        :param vpool:Replication group identifier
        """
        assert name is not None, MESSAGE_BUCKET_NAME_REQUIRED

        assert filesystem_enabled is not None, MESSAGE_FILESYSTEM_ENABLED_REQUIRED
        assert isinstance(filesystem_enabled, bool), MESSAGE_FILESYSTEM_NOT_VALID

        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert is_stale_allowed is not None, MESSAGE_IS_STALE_ALLOWED_REQUIRED
        assert isinstance(is_stale_allowed, bool), MESSAGE_IS_STALE_NOT_VALID
        body = {"name": name,
                "filesystem_enabled": filesystem_enabled,
                "namespace": namespace,
                "is_stale_allowed": is_stale_allowed}
        if head_type is not None:
            body['head_type'] = head_type
        if vpool is not None:
            body['vpool'] = vpool
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createbucket = requests.post(self.ecsAdminClient.url + CREATE_BUCKET, headers=headers, data=body, verify=False)
        self.commons.checkstatus(createbucket)
        return createbucket.json()

    def deleteBucket(self, namespace, bucketName):
        """
        Deletes the specified bucket.
        :param namespace:Namespace associated. If it is null, then current user's namespace is used.
        :param bucketName:Bucket name to be deleted
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        body = {"namespace": namespace}
        #         body=json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deletebucket = requests.post(self.ecsAdminClient.url + DELETE_BUCKET.format(bucketName), headers=headers,
                                     params=body, verify=False)
        if self.commons.checkstatus(deletebucket):
            return True
        else:
            return False

    def getBuckets(self, namespace=None, marker=None, limit=None):
        """
        Gets the list of buckets for the specified namespace
        :param namespace:Namespace for which buckets should be listed
        :param marker:Reference to last object returned.
        :param limit:Number of objects requested in current fetch.
        """

        body = {}

        if marker is not None:
            body['marker'] = marker
        if namespace is not None:
            body['namespace'] = namespace
        if limit is not None:
            body['limit'] = limit

        #         body=json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        bucketinformartion = requests.get(self.ecsAdminClient.url + GET_BUCKET, headers=headers, params=body,
                                          verify=False)
        self.commons.checkstatus(bucketinformartion)
        return bucketinformartion.json()

    def updateRetentionForBucket(self, bucketName, period, namespace):
        """
        Updates the default retention period setting for the specified bucket.
        :param bucketName:Bucket name for which retention period will be updated
        :param period:Default retention period in seconds
        :param namespace:Namespace to which this bucket belongs
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert period is not None, MESSAGE_PERIOD_REQUIRED
        body = {"period": period, "namespace": namespace}
        #         body=json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        updateretenion = requests.put(self.ecsAdminClient.url + UPDATE_RETENTION_PERIOD_FOR_BUCKET.format(bucketName),
                                      headers=headers, data=body, verify=False)
        if self.commons.checkstatus(updateretenion):
            return True
        else:
            return False

    def getRetentionForBucket(self, bucketName, namespace):
        """
        Gets the retention period setting for the specified bucket
        :param bucketName:Bucket name for which the retention period setting will be retrieved
        :param namespace:Namespace associated. If it is null, then current user's namespace is used.
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        body = {"namespace": namespace}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        retentionresponse = requests.get(self.ecsAdminClient.url + GET_RETENTION_PERIOD_FOR_BUCKET.format(bucketName),
                                         headers=headers, params=body, verify=False)
        self.commons.checkstatus(retentionresponse)
        return retentionresponse.json()

    def getBucketInformationForSpecifiedBucket(self, namespace, bucketName):
        """
        Gets bucket information for the specified bucket
        :param namespace:Namespace associated. If it is null, then current user's namespace is used.
        :param bucketName:Bucket name for which information will be retrieved
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        body = {"namespace": namespace}

        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        bucketresponse = requests.get(self.ecsAdminClient.url + GET_BUCKET_INFORMATION_FOR_BUCKET.format(bucketName),
                                      headers=headers, params=body, verify=False)
        self.commons.checkstatus(bucketresponse)
        return bucketresponse.json()

    def updateBucketOwner(self, bucketName, namespace, new_owner):
        """
        Updates the owner for the specified bucket.
        :param bucketName:Name of the bucket for which owner will be updated
        :param namespace:Namespace that is allowed to access this bucket
        :param new_owner:New owner of the bucket
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert new_owner is not None, MESSAGE_OWNER_REQUIRED
        body = {"namespace": namespace, "new_owner": new_owner}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        updateownerresponse = requests.post(self.ecsAdminClient.url + UPDATE_BUCKET_OWNER.format(bucketName),
                                            headers=headers, data=body, verify=False)
        if self.commons.checkstatus(updateownerresponse):
            return True
        else:
            return False

    def updateBucketIsStaleState(self, bucketName, is_stale_allowed, namespace):
        """
        Updates isStaleAllowed details for the specified bucket in order to enable access to the bucket during a
        temporary site outage.
        :param bucketName:Name of the bucket for which isStaleAllowed is to be updated
        :param is_stale_allowed:isStaleAllowed flag of the bucket
        :param namespace:Namespace associated with the user/tenant that is allowed to access the bucket
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert is_stale_allowed is not None, MESSAGE_IS_STALE_ALLOWED_REQUIRED
        assert isinstance(is_stale_allowed, bool), MESSAGE_IS_STALE_NOT_VALID
        body = {"is_stale_allowed": is_stale_allowed, "namespace": namespace}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        updateownerresponse = requests.post(self.ecsAdminClient.url + UPDATE_IS_STALE_ALLOWED.format(bucketName),
                                            headers=headers, data=body, verify=False)
        if self.commons.checkstatus(updateownerresponse):
            return True
        else:
            return False

    def getBucketLock(self, bucketName, namespace):
        """
        Gets lock information for the specified bucket
        :param bucketName:Name of the bucket for which lock information is to be retrieved
        """
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        body = {"namespace": namespace}
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        lockresponse = requests.get(self.ecsAdminClient.url + GET_BUCKET_LOCK.format(bucketName), headers=headers,
                                    params=body, verify=False)
        self.commons.checkstatus(lockresponse)
        return lockresponse.json()

    def updateLock(self, bucketName, isLocked, namespace):
        """
        Locks or unlocks the specified bucket.
        :param bucketName:Name of the bucket which is to be locked/unlocked.
        :param isLocked:Set to "true" for lock bucket and "false" for unlock bucket
        :param namespace:Namespace that is allowed to access this bucket
        """
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert isLocked is not None, MESSAGE_IS_LOCK_REQUIRED
        assert isinstance(isLocked, bool), MESSAGE_IS_LOCK_NOT_VALID
        body = {"namespace": namespace}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        updateresponse = requests.put(self.ecsAdminClient.url + UP_DATE_BUCKET_LOCK.format(bucketName, isLocked),
                                      data=body, headers=headers, verify=False)
        if self.commons.checkstatus(updateresponse):
            return True
        else:
            return False

    def updateBucketQuota(self, bucketName, blockSize, notificationSize, namespace):
        """
        Updates the quota for the specified bucket
        :param bucketName:Name of the bucket for which the quota is to be updated
        :param blockSize:Block size in GB
        :param notificationSize:Notification size in GB
        :param namespace:Namespace to which this bucket belongs
        """

        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert blockSize is not None, MESSAGE_BLOCKSIZE_REQUIRED
        assert notificationSize is not None, MESSAGE_NOTIFICATION_SIZE_REQUIRED
        body = {"namespace": namespace, "blockSize": blockSize, "notificationSize": notificationSize}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        updateResponse = requests.put(self.ecsAdminClient.url + UPDATE_BUCKET_QUOTA.format(bucketName), headers=headers,
                                      data=body, verify=False)
        if self.commons.checkstatus(updateResponse):
            return True
        else:
            return False

    def getBucketQuota(self, bucketName, namespace):
        """
        Gets the quota for the given bucket and namespace.
        :param bucketName:Name of the bucket which for which quota is to be retrieved
        :param namespace:Namespace with which bucket is associated
        """
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        body = {"namespace": namespace}
        #         body=json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        quotaResponse = requests.get(self.ecsAdminClient.url + GET_BUCKET_QUOTA, headers=headers, params=body,
                                     verify=False)
        self.commons.checkstatus(quotaResponse)
        return quotaResponse.json()

    def deleteBucketQuota(self, bucketName, namespace):
        """
        Deletes the quota setting for the given bucket and namespace
        :param bucketName:Name of the bucket for which the quota is to be deleted
        :param namespace:Namespace with which bucket is associated
        """
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        body = {"namespace": namespace}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteresponse = requests.delete(self.ecsAdminClient.url + DELETE_QUOTA.format(bucketName), headers=headers,
                                         data=body, verify=False)
        if self.commons.checkstatus(deleteresponse):
            return True
        else:
            return False

    def updateACL(self, bucketName, acl):
        """
        Updates the ACL for the given bucket.
        :param bucketName:Name of the bucket for which the ACL is to be updated.

        :param acl:ACL Object Instance
        """

        assert acl is not None, MESSAGE_ACL_REQUIRED
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        updateResponse = requests.put(self.ecsAdminClient.url + UPDATE_ACL.format(bucketName), headers=headers,
                                      data=acl, verify=False)
        if self.commons.checkstatus(updateResponse):
            return True
        else:
            return False

    def getBucketACL(self, bucketName, namespace):
        """
        Gets the ACL for the given bucket. Current user's namespace is used.
        :param bucketName:Name of the bucket for which ACL is to be updated.
        :param namespace:Namespace with which bucket is associated
        """
        assert bucketName is not None, MESSAGE_BUCKET_NAME_REQUIRED
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        body = {"namespace": namespace}
        #         body=json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        acl = requests.get(self.ecsAdminClient.url + GET_ACL.format(bucketName), headers=headers, params=body,
                           verify=False)
        self.commons.checkstatus(acl)
        return acl.json()

    def getACLPermission(self):
        """
        Gets all ACL permissions.
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        aclPersmission = requests.get(self.ecsAdminClient.url + GET_ACL_PERMISSION, headers=headers, verify=False)
        self.commons.checkstatus(aclPersmission)
        return aclPersmission.json()

    def getACLGroups(self):
        """
        Gets all ACL groups.
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        aclGroup = requests.get(self.ecsAdminClient.url + GET_ACL_GROUPS, headers=headers, verify=False)
        self.commons.checkstatus(aclGroup)
        return aclGroup.json()
