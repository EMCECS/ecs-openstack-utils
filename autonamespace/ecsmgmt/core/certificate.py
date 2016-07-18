"""
Created on Jul 1, 2015

@author: joshia7
"""
import requests
import simplejson as json
from ecsmgmt.util.messageconstants import *
from ecsmgmt.util.commons import Commons
from ecsmgmt.util.urlconstants import *


class Certificate:
    """
    Class for managing certificates.
    """

    def __init__(self, client_instance, token):
        self.ecsAdminClient = client_instance
        self.token = token
        self.commons = Commons()

    def getCertificateChain(self):
        """
        Gets certificate chain configured
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        certificateResponse = requests.get(self.ecsAdminClient.url + GET_CERTIFICATE_CHAIN_CONFIGURED,
                                           headers=headers, verify=False)
        self.commons.checkstatus(certificateResponse)
        return certificateResponse.json()

    def setKeyCertificate(self, system_selfsigned, private_key, certificate_chain, ip_addresses=None):
        """
        Sets private key and certificate pair. The new certificate and key will be rotated into all of the nodes
        within 1 hour.
        :param system_selfsigned:Set true if the new certificate is self signed, false otherwise.
        :param private_key:The private key used to sign the certificate in PEM format.
        :param certificate_chain:New certificate for the nodes in PEM format
        :param ip_addresses:Key and certificate parameter IP addresses
        """
        assert system_selfsigned is not None, MESSAGE_SELF_SYSTEM_SIGN_REQUIRED
        assert isinstance(system_selfsigned, bool), MESSAGE_SELF_SYSTEM_SIGN_IS_BOOLEAN
        assert private_key is not None, MESSAGE_PRIVATE_KEY_REQUIRED
        assert certificate_chain is not None, MESSAGE_CERTIFICATE_CHAIN_REQUIRED
        key_and_certificate = {"private_key": private_key, "certificate_chain": certificate_chain}
        body = {"ip_addresses": ip_addresses,
                "system_selfsigned": system_selfsigned,
                "key_and_certificate": key_and_certificate}
        body = json.dumps(body)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json'}
        setResponse = requests.put(self.ecsAdminClient.url + SET_KEY_CERTIFICATE_PAIR, headers=headers,
                                   data=body, verify=False)
        self.commons.checkstatus(setResponse)
        return setResponse.json()
