"""
Created on Jun 24, 2015

@author: joshia7
"""

import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *
from datetime import datetime


class Billing:
    """
    Class for managing billing details
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.commons = Commons()
        self.token = token

    def getBillingDetailsForBucket(self, namespace, bucket, sizeUnit=None):
        """
        Gets billing details for the specified namespace and bucket name
        :param namespace:Namespace containing the bucket
        :param bucket:Bucket name for which billing information needs to be retrieved
        :param sizeUnit:Unit to be used for calculating the size on disk (KB,MB and GB. GB is default value).
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert bucket is not None, MESSAGE_BUCKET_REQUIRED

        if sizeUnit is None:
            sizeUnit = "GB"
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        params = {"sizeunit": sizeUnit}
        billingBucketInfo = requests.get(
            self.ecsAdminClient.url + GET_BILLING_NAMESPACE_BUCKET.format(namespace, bucket), headers=headers,
            params=params, verify=False)
        self.commons.checkstatus(billingBucketInfo)
        return billingBucketInfo.json()

    def getBillingWithInterval(self, start_time, end_time, namespace, bucket, sizeunit=None):
        """
        Gets billing details for the specified namespace, interval and bucket details.
        :param start_time:Starting time for the sample(s) in ISO-8601 minute format.
        :param end_time:Ending time for the sample(s) in ISO-8601 minute format.
        :param namespace:Namespace containing the bucket
        :param bucket:Bucket name
        :param sizeunit:Unit to be used for calculating the size on disk
        """
        assert start_time is not None, MESSAGE_START_TIME_REQUIRED
        assert end_time is not None, MESSAGE_END_TIME_REQUIRED
        start_minutes = datetime.strptime(start_time, '%Y-%m-%dT%H:%M').minute

        assert start_minutes % 5 == 0, MESSAGE_START_TIME_NOT_VALID

        end_minutes = datetime.strptime(end_time, '%Y-%m-%dT%H:%M').minute

        assert end_minutes % 5 == 0, MESSAGE_END_TIME_NOT_VALID
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED
        assert bucket is not None, MESSAGE_BUCKET_REQUIRED

        if sizeunit is None:
            sizeunit = "GB"
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        params = {"sizeunit": sizeunit, "start_time": start_time, "end_time": end_time}
        billingBucketInfo = requests.get(self.ecsAdminClient.url + GET_BILLING_WITH_INTERVAL.format(namespace, bucket),
                                         headers=headers, params=params, verify=False)
        self.commons.checkstatus(billingBucketInfo)
        return billingBucketInfo.json()

    def namespaceBillingInfo(self, namespace, include_bucket_detail=None, marker=None, sizeunit=None):
        """
        Gets billing details for the specified namespace and bucket details
        :param namespace:Namespace to get information about
        :param include_bucket_detail:If true, include information about all the buckets owned by this namespace
        :param marker:Used to continue a truncated response
        :param sizeunit:Unit to be used for calculating the size on disk
        """
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED

        if sizeunit is None:
            sizeunit = "GB"
        if include_bucket_detail is None:
            include_bucket_detail = False

        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        if marker is None:
            params = {"sizeunit": sizeunit, "include_bucket_detail": include_bucket_detail}
        else:
            params = {"sizeunit": sizeunit, "include_bucket_detail": include_bucket_detail, "marker": marker}

        billingInfo = requests.get(self.ecsAdminClient.url + GET_BILLING_FOR_NAMESPACE.format(namespace),
                                   headers=headers, params=params, verify=False)
        self.commons.checkstatus(billingInfo)
        return billingInfo.json()

    def namespaceBillingInfoWithInterval(self, namespace, start_time, end_time, include_bucket_detail=None,
                                         sizeunit=None, marker=None):
        """
        Gets billing details for the specified namespace, interval and, optionally, buckets
        :param namespace:Namespace to get information about
        :param start_time:Starting time (inclusive) for the sample(s) in ISO-8601 minute format
        :param end_time:Ending time (exclusive) for the sample(s) in ISO-8601 minute format.
        :param include_bucket_detail:Optional (default=false). If true, include information about all the buckets
        owned by this namespace.
        :param sizeunit:Unit to be used for calculating the size on disk
        :param marker:Optional, Used to continue a truncated response.
        """
        assert start_time is not None, MESSAGE_START_TIME_REQUIRED
        assert end_time is not None, MESSAGE_END_TIME_REQUIRED

        start_minutes = datetime.strptime(start_time, '%Y-%m-%dT%H:%M').minute

        assert start_minutes % 5 == 0, MESSAGE_START_TIME_NOT_VALID

        end_minutes = datetime.strptime(end_time, '%Y-%m-%dT%H:%M').minute

        assert end_minutes % 5 == 0, MESSAGE_END_TIME_NOT_VALID
        assert namespace is not None, MESSAGE_NAMESPACE_REQUIRED

        if sizeunit is None:
            sizeunit = "GB"
        if include_bucket_detail is None:
            include_bucket_detail = False

        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        if marker is None:
            params = {"sizeunit": sizeunit, "include_bucket_detail": include_bucket_detail, "start_time": start_time,
                      "end_time": end_time}
        else:
            params = {"sizeunit": sizeunit, "include_bucket_detail": include_bucket_detail, "marker": marker,
                      "start_time": start_time, "end_time": end_time}

        billingInfo = requests.get(self.ecsAdminClient.url + GET_BILLING_NAMESPACE_WITH_INTERVAL.format(namespace),
                                   headers=headers, params=params, verify=False)
        self.commons.checkstatus(billingInfo)
        return billingInfo.json()
