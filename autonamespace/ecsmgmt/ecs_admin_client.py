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
Created on Jun 25, 2015

@author: joshia7
"""

from util.urlconstants import *
from core.authentication import Authentication
from util.commons import Commons
from core.namespace import Namespace
from core.billing import Billing
from core.cas import CAS
from core.certificate import Certificate
# from symbol import parameters
# from uuid import NAMESPACE_URL
from core.configureproperties import ConfigureProperties
from core.licensing import Licensing
from core.capacity import Capacity
from core.dashboard import DashBoard
from core.events import Events
from core.replicationgroup import ReplicationGroup
from core.tempfailedzone import TempFailedZone
from core.baseurl import BaseURL
from core.bucket import Bucket
from core.datastore import DataStore
from core.node import Node
from core.storagePool import StoragePool
from core.vdc import VDC
from core.callhome import CallHome
from core.authenticationprovider import AuthenticationProvider
from core.passwordgroup import PasswordGroup
from core.secretKey import SecretKey
from core.secretkeyselfservice import SecretKeySelfService
from core.userObject import UserObject
from core.userManagement import UserManagement
from util.messageconstants import *
import os
import logging

"""
# Logging
"""

# logging.basicConfig(filename='api.log', level=logging.DEBUG)
# logging.captureWarnings(True)
# logging.debug('-' * 40 + os.path.abspath(__file__) + '-' * 40)

"""
# Client
"""


class ECSAdminClient:
    """
    Serves as the First point of interaction with the SDK and also provides ECS Management API instances.
    """

    def __init__(self, url, username=None, password=None, token=None):
        """

        :param url:The ECS URL
        :param username:Username
        :param password:Password
        :param token:Authentication Token
        """
        self.url = url
        assert url is not None, MESSAGE_URL_REQUIRED

        if password is not None and username is not None and token is None:
            self.userName = username
            self.password = password
            self.token = None

        if token is not None and username is not None and password is None:
            self.token = token

            self.check_scope = True
        else:

            self.check_scope = False

    def __del__(self):
        """
        This method is automatically called when the Object goes out of Scope and if no token is passed to the
        constructor then it logouts the user from ECSAPI
        """
        if not self.check_scope:
            self.logout()

            #     Login Method
            #     parameters:
            #        self:ECSAdminClient Object

    def login(self):
        """
        Login with userName and password
        """
        if self.token is None:
            auth = Authentication(self)
            self.token = auth.login(self.userName, self.password)
            return self.token

    @staticmethod
    def static_login(self, username, password):
        """

        :param self:
        :type self:
        :param username:
        :type username:
        :param password:
        :type password:
        """
        auth = Authentication(self)
        self.token = auth.login(self.userName, self.password)

    #     Logout Method
    #     parameters:
    #        self:ECSAdminClient Object
    def logout(self):
        """
        To logout the user from the ECS Management API
        """

        #
        # print "In logout "
        auth = Authentication(self)
        try:
            logout_response = auth.logout(self.token)
            common = Commons()
            if common.checkstatus(logout_response):
                self.token = None
        except AssertionError:
            if self.token is None:
                # We must not have had a token to begin with, don't spam.
                pass
            else:
                # Something else happened.
                raise

                #     NameSpace Method
                #     parameters:
                #        self:ECSAdminClient Object

    def namespaces(self):
        """
        Returns a Namespace instance object to the user
        """
        namespace = Namespace(self, self.token)
        return namespace

    #     Billing Method
    #     parameters:
    #        self:ECSAdminClient Object

    def billing(self):
        """
        Returns a Billing instance object to the user
        """
        billing = Billing(self, self.token)
        return billing

    #     CAS Method
    #     parameters:
    #        self:ECSAdminClient Object

    def cas(self):
        """
        Returns a CAS instance object to the user
        """

        cas = CAS(self, self.token)
        return cas

    #     Certificate Method
    #     parameters:
    #        self:ECSAdminClient Object

    def certificate(self):
        """
        Returns a Certificate instance object to the user
        """
        certificate = Certificate(self, self.token)
        return certificate

    #     ConfigureProperties Method
    #     parameters:
    #        self:ECSAdminClient Object

    def configuration_properties(self):
        """
        Returns a Configuration Properties  instance object to the user
        """
        configuration_properties = ConfigureProperties(self, self.token)
        return configuration_properties

    #     Licensing Method
    #     parameters:
    #        self:ECSAdminClient Object

    def license(self):
        """
        Returns a License instance object to the user
        """
        license_instance = Licensing(self, self.token)
        return license_instance

    #     Capacity Method
    #     parameters:
    #        self:ECSAdminClient Object
    def capacity(self):
        """
        Returns a Capacity instance object to the user
        """
        capacity = Capacity(self, self.token)
        return capacity

    #     DashBoard Method
    #     parameters:
    #        self:ECSAdminClient Object

    def dashboard(self):
        """
        Returns a DashBoard instance object to the user
        """
        dashboard = DashBoard(self, self.token)
        return dashboard

    #     Events Method
    #     parameters:
    #        self:ECSAdminClient Object
    def events(self):
        """
        Returns a Events instance object to the user
        """
        events = Events(self, self.token)
        return events

    #     ReplicationGroup Method
    #     parameters:
    #        self:ECSAdminClient Object

    def replication_group(self):
        """
        Returns a Replication group instance object to the user
        """
        replication_group = ReplicationGroup(self, self.token)
        return replication_group

    #     TempFailedZone Method
    #     parameters:
    #        self:ECSAdminClient Object

    def temp_failed_zone(self):
        """
        Returns a Temp Failed Zone instance object to the user
        """
        temp_failed_zone = TempFailedZone(self, self.token)
        return temp_failed_zone

    #     BaseURL Method
    #     parameters:
    #        self:ECSAdminClient Object
    def base_url(self):
        """
        Returns a BaseURL instance object to the user
        """
        base_url = BaseURL(self, self.token)
        return base_url

    #     Bucket Method
    #     parameters:
    #        self:ECSAdminClient Object

    def bucket(self):
        """
        Returns a Bucket instance object to the user
        """

        bucket = Bucket(self, self.token)
        return bucket

    #     DataStore Method
    #     parameters:
    #        self:ECSAdminClient Object

    def data_store(self):
        """
        Returns a DataStore instance object to the user
        """
        data_store = DataStore(self, self.token)
        return data_store

    #     Node Method
    #     parameters:
    #        self:ECSAdminClient Object

    def node(self):
        """
        Returns a Node instance object to the user
        """
        node = Node(self, self.token)
        return node

    #     StoragePool Method
    #     parameters:
    #        self:ECSAdminClient Object

    def storage_pool(self):
        """
        Returns a Storage instance object to the user
        """
        storage_pool = StoragePool(self, self.token)
        return storage_pool

    #     VDC Method
    #     parameters:
    #        self:ECSAdminClient Object

    def vdc(self):
        """
        Returns a VDC instance object to the user
        """
        vdc = VDC(self, self.token)
        return vdc

    #     CallHome Method
    #     parameters:
    #        self:ECSAdminClient Object

    def call_home(self):
        """
        Returns a CallHome instance object to the user
        """
        call_home = CallHome(self, self.token)
        return call_home

    #     AuthenticationProvider Method
    #     parameters:
    #        self:ECSAdminClient Object
    def authentication_provider(self):
        """
        Returns a AuthenticationProvider instance object to the user
        """

        authentication_provider = AuthenticationProvider(self, self.token)
        return authentication_provider

    #     PasswordGroup Method
    #     parameters:
    #        self:ECSAdminClient Object

    def password_group(self):
        """
        Returns a Password Group object to the user
        """
        password_group = PasswordGroup(self, self.token)
        return password_group

    #     SecretKey Method
    #     parameters:
    #        self:ECSAdminClient Object

    def secret_key(self):
        """
        Returns a Secret Key object to the user
        """

        secret_key = SecretKey(self, self.token)
        return secret_key

    #     SecretKeySelfService Method
    #     parameters:
    #        self:ECSAdminClient Object
    def secret_key_self_service(self):
        """
        Returns a secretKey instance object to the user
        """
        secret_key_self_service = SecretKeySelfService(self, self.token)
        return secret_key_self_service

    #     UserObject Method
    #     parameters:
    #        self:ECSAdminClient Object
    def object_user(self):
        """
        Returns a ObjectUser instance object to the user
        """
        object_user = UserObject(self, self.token)
        return object_user

    #     UserManagement Method
    #     parameters:
    #        self:ECSAdminClient Object

    def management_user(self):
        """
        Returns a ManagementUser instance object to the user
        """
        management_user = UserManagement(self, self.token)
        return management_user
