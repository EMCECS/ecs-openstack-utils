"""
Created on Jul 1, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


# from ECSAdminClient import ECSAdminClient

class CallHome:
    """
    Class for managing alerts and sending alerts to ConnectEMC for troubleshooting and debugging purposes
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def createAlert(self, user_str, contact, event_id=None):
        """
        Creates and sends an alert event with error logs attached as an aid to troubleshooting customer issues.
        :param event_id:Event id for these alerts,Allowed values: 999, 599,Default: 999
        :param user_str:User written string
        :param contact:Contact details
        """

        assert user_str is not None, MESSAGE_USER_STRING_REQUIRED
        assert contact is not None, MESSAGE_CONTACT_REQUIRED
        assert event_id == 999 or event_id == 599 or event_id is None, MESSAGE_EVENT_ID_NOT_VALID
        if event_id is None:
            event_id = 999
        body = {"user_str": user_str, "contact": contact}
        body = json.dumps(body)
        params = {"event_id": event_id}
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createalertresponse = requests.post(self.ecsAdminClient.url + CREATE_ALERT, data=body, params=params,
                                            headers=headers, verify=False)
        self.commons.checkstatus(createalertresponse)
        return createalertresponse.json()

    def configureFTPSProperties(self, host_name=None, email_server=None, notify_email_address=None, email_sender=None,
                                bsafe_encryption_ind=None):
        """
        Configures ConnectEMC FTPD transport properties.
        :param host_name:ConnectEMC FTPS Hostname
        :param email_server:SMTP server or relay for sending email
        :param notify_email_address:Email address for the ConnectEMC Service notifications
        :param email_sender:From email address for sending email messages
        :param bsafe_encryption_ind:Encrypt ConnectEMC Service data using RSA BSAFE
        """
        body = {"host_name": host_name,
                "email_server": email_server,
                "notify_email_address": notify_email_address,
                "email_sender": email_sender,
                "bsafe_encryption_ind": bsafe_encryption_ind}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        configureresponse = requests.post(self.ecsAdminClient.url + CONFIGURE_FTPS_PROPERTIES, headers=headers,
                                          data=body, verify=False)
        if self.commons.checkstatus(configureresponse):
            return True
        else:
            return False

    def configSMTP(self, email_server=None, port=None, primary_email_address=None, notify_email_address=None,
                   email_sender=None, smtp_auth_type=None, username=None, password=None, start_tls_ind=None,
                   enable_tls_cert=None, bsafe_encryption_ind=None):
        """
        Configures ConnectEMC SMTP transport properties
        :param email_server:SMTP server or relay for sending email
        :param port:SMTP server port. If set to 0, the default SMTP port is used (25, or 465 if TLS/SSL is enabled)
        :param primary_email_address:Email address where you can be contacted
        :param notify_email_address:Email address for the ConnectEMC Service notifications
        :param email_sender:From email address for sending email messages
        :param smtp_auth_type:Authentication type for connecting to the SMTP server
        :param username:Username for authenticating with the SMTP server
        :param password:Password for authenticating with the SMTP server
        :param start_tls_ind:Use TLS/SSL for the SMTP server connections
        :param enable_tls_cert:Enable TLS Certificate
        :param bsafe_encryption_ind:Encrypt ConnectEMC Service data using RSA BSAFE
        """
        body = {"email_server": email_server,
                "port": port,
                "primary_email_address": primary_email_address,
                "notify_email_address": notify_email_address,
                "email_sender": email_sender,
                "smtp_auth_type": smtp_auth_type,
                "username": username,
                "password": password,
                "start_tls_ind": start_tls_ind,
                "enable_tls_cert": enable_tls_cert,
                "bsafe_encryption_ind": bsafe_encryption_ind}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        configureresponse = requests.post(self.ecsAdminClient.url + CONFIGURE_SMTP, headers=headers, data=body,
                                          verify=False)
        if self.commons.checkstatus(configureresponse):
            return True
        else:
            return False

    def disableConnectEMC(self):
        """
        Disables ConnectEMC configurations.
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        disbaleresponse = requests.post(self.ecsAdminClient.url + DISABLE_CONNECTEMC, headers=headers, verify=False)
        if self.commons.checkstatus(disbaleresponse):
            return True
        else:
            return False

    def getConfigDetails(self):
        """
        Gets ConnectEMC configuration details.
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        configdetails = requests.get(self.ecsAdminClient.url + GET_CONNECTEMC_CONFIG_DETAILS, headers=headers,
                                     verify=False)
        self.commons.checkstatus(configdetails)
        return configdetails.json()
