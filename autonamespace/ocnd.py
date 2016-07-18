#!/usr/bin/env python
# coding=utf-8

# Copyright (c) 2015 EMC Corporation
# All Rights Reserved
#
# This software contains the intellectual property of EMC Corporation
# or is licensed to EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of EMC.


"""
ocnd.py - OpenStack Create Namespace Daemon

Travis Wichert <travis.wichert@emc.com>, EMC ECS Customer Advisory Team

Listens on OpenStack Oslo message bus for project/tenant create messages
from Keystone and creates an ECS namespace by the same name with defaults
provided in the Constants section of this script.
"""

from pprint import pprint
import signal
import sys
from oslo_config import cfg
import oslo_messaging
from oslo_messaging import NotificationFilter
from ecsmgmt.ecs_admin_client import ECSAdminClient


"""
Constants
"""


DEFAULT_ECS_RG_NAME = 'default'
DEFAULT_ECS_API_URL = 'https://127.0.0.1:4443'
DEFAULT_ECS_ADMIN_USER = 'root'
DEFAULT_ECS_ADMIN_PASS = 'ChangeMe'


"""
Config classes
"""


class NamespaceConfig(object):
    """
    Represents a namespace configuration
    """
    conf = {
        'namespace': None,
        'namespace_admins': None,
        'default_data_services_vpool': None,
        'default_object_project': None,
        'allowed_vpools_list': None,
        'disallowed_vpools_list': None,
        'user_mapping': None
    }

    def __init__(self, confdict=None):
        if confdict is not None:
            self.conf.update(confdict)

    def set(self, key, value):
        self.conf[key] = value


"""
Client Classes
"""


class ECSClientWrapper(ECSAdminClient):

    url = DEFAULT_ECS_API_URL
    username = DEFAULT_ECS_ADMIN_USER
    password = DEFAULT_ECS_ADMIN_PASS

    def __init__(self):

        ECSAdminClient.__init__(self,
                                url=self.url,
                                username=self.username,
                                password=self.password)

        self.login()

    def get_rgid_by_name(self, rgname):
        client = self.replication_group()
        rgs = client.getReplicationGroups()['data_service_vpool']
        return [x['id'] for x in rgs if x['name'] == rgname][0]

    def create_namespace(self, conf):
        namespace_client = self.namespaces()
        namespace_client.createNameSpace(**conf)


"""
Oslo listener classes
"""


class KeystoneListener(object):
    """
    Keystone notification listener
    """
    filter_rule = NotificationFilter(publisher_id='^keystone.*',
                                     event_type='identity.project.created')

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        handle_project(metadata, payload)


class IdentityListener(object):
    """
    Keystone notification listener
    """
    filter_rule = NotificationFilter(publisher_id='^identity.*',
                                     event_type='identity.project.created')

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        handle_project(metadata, payload)


"""
Handlers
"""


def handle_project(payload, metadata):

    project_id = payload['resource_info']

    ecsclient = ECSClientWrapper()

    nsconfobj = NamespaceConfig()
    nsconfobj.set('namespace', project_id)
    nsconfobj.set('namespace_admins', None)
    nsconfobj.set('default_data_services_vpool', ecsclient.get_rgid_by_name(DEFAULT_ECS_RG_NAME))

    ecsclient.create_namespace(conf=nsconfobj.conf)

    ecsclient.logout()


def handle_signals(signum, frame):
    daemon.stop()
    sys.exit(0)


"""
Main
"""


pool = "emc-ecs-ocnd"

transport = oslo_messaging.get_notification_transport(cfg.CONF)

d = cfg.CONF.__dict__

pprint(d['_groups']['oslo_messaging_rabbit'].__dict__['_opts'])

endpoints = [
    KeystoneListener(),
    IdentityListener()
]

targets = [
    oslo_messaging.Target(topic='notifications'),
    oslo_messaging.Target(topic='notifications_bis')
]

daemon = oslo_messaging.get_notification_listener(transport=transport,
                                                  targets=targets,
                                                  endpoints=endpoints,
                                                  pool=pool)
daemon.start()
signal.signal(signal.SIGINT, handle_signals)
daemon.wait()
