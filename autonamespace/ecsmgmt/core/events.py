"""
Created on Jul 1, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


class Events:
    """
    Class for fetching audit alerts.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def getAuditEvents(self, start_time=None, end_time=None, namespace=None, marker=None, limit=None):
        """
        Gets audit events for the specified namespace identifier and interval.
        :param start_time:Start time for the interval to retrieve audit events
        :param end_time:End time for the interval to retrieve audit events
        :param namespace:Namespace identifier for which audit events needs to be retrieved
        :param marker:Reference of last audit event returned
        :param limit:Number of audit events requested in current fetch
        """

        body = {}
        if start_time is not None:
            body['start_time'] = start_time
        if end_time is not None:
            body['end_time'] = end_time
        if namespace is not None:
            body['namespace'] = namespace
        if marker is not None:
            body['marker'] = marker
        if limit is not None:
            body['limit'] = limit

        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        auditeventsresponse = requests.get(self.ecsAdminClient.url + GET_AUDIT_EVENTS, headers=headers, params=body,
                                           verify=False)
        self.commons.checkstatus(auditeventsresponse)
        return auditeventsresponse.json()
