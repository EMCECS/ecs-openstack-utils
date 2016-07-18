"""
Created on Jul 6, 2015

@author: joshia7
"""

from ecsmgmt.util.messageconstants import *
import simplejson as json
import requests

from ecsmgmt.util.urlconstants import *
from ecsmgmt.util.commons import Commons


class AuthenticationProvider:
    """
    Class for provisioning and managing authentication providers.
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def get_authentication_provider(self, authenticationProviderId):
        """
        Gets the details for the specified authentication provider
        :param authenticationProviderId:Authentication provider identifier URN
        """
        assert authenticationProviderId is not None, MESSAGE_AUTH_PROVIDER_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getDetails = requests.get(self.ecsAdminClient.url + GET_SPECIFIED_AUTHENTICATION_PROVIDER.format(
            authenticationProviderId), headers=headers, verify=False)
        self.commons.checkstatus(getDetails)
        return getDetails.json()

    def authenticationProviderList(self):
        """
        Lists the configured authentication providers
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getList = requests.get(self.ecsAdminClient.url + GET_AUTHENTICATION_PROVIDER_LIST, headers=headers,
                               verify=False)
        self.commons.checkstatus(getList)
        return getList.json()

    def createAuthProvider(self, AuthProvider):
        """
        Creates an authentication provider using the specified attributes
        :param AuthProvider:AuthProvider provider object
        """
        assert AuthProvider is not None, MESSAGE_AUTH_PROVIDER_REQUIRED
        body = AuthenticationProvider.getJSON()
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        createResponse = requests.post(self.ecsAdminClient.url + CREATE_AUTHENTICATION_PROVIDER, data=body,
                                       headers=headers, verify=False)
        self.commons.checkstatus(createResponse)
        return createResponse.json()

    def deleteAuthProvider(self, authenticationProviderId):
        """
        Deletes an authentication provider
        :param authenticationProviderId:URN of the authentication provider to be deleted
        """
        assert authenticationProviderId is not None, MESSAGE_AUTH_PROVIDER_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteResponse = requests.delete(self.ecsAdminClient.url + DELET_AUTHENTICATION_PROVIDER,
                                         headers=headers, verify=False)
        if self.commons.checkstatus(deleteResponse):
            return True
        else:
            return False

    def update_authentication_provider(self, authenticationProviderId, mode, add_urls, remove_urls,
                                       managerdn, managerpwd,
                                       searchbase, searchfilter,
                                       groupattr, name, add_domains,
                                       remove_domains, add_whitelist,
                                       remove_whitelist, searchscope,
                                       description, disable,
                                       validatecertificate, maxpagesize):
        """
        Updates an authentication provider with the specified attribute values
        :param authenticationProviderId:URN of the authentication provider to be updated
        :param mode:Type of provider. Active Directory(AD) or generic LDAPv3 (LDAP)
        :param add_urls:List of Server URLs to add. You cannot mix ldap and ldaps URLs
        :param remove_urls:List of Server URLs to remove

        :param managerdn:Distinguished Name for the bind user.
        :param managerpwd:Password for the manager DN "bind" user.
        :param searchbase:Search base from which the LDAP search will start when authenticating users.
        :param searchfilter:Key value pair representing the search filter criteria.

        :param groupattr:Attribute for group search. This is the attribute name that will be used to represent group
        membership. Once set during creation of the provider, the value for this parameter cannot be changed.
        :param name:Name of the provider
        :param add_domains:List of domains to add
        :param remove_domains:List of domains to remove
        :param add_whitelist:List of white list values to add
        :param remove_whitelist:List of white list values to remove
        :param searchscope:In conjunction with the search_base, the search_scope indicates how many levels below the
        base the search can continue
        :param description:Description of the provider
        :param disable:Specifies if a provider is disabled or enabled.
        :param validatecertificate:Whether or not to validate certificates when LDAPS is used
        :param maxpagesize:Maximum number of results that the LDAP server will return on a single page
        """
        server_assignments = dict()
        domain_assignments = dict()
        whitelist_assignments = dict()
        urls = dict()
        domains = dict()
        whitelist = dict()
        urls['add'] = []
        for iter in add_urls:
            if iter is not "":
                urls['add'].append(iter)

        urls['remove'] = []
        for iter in remove_urls:
            if iter is not "":
                urls['remove'].append(iter)

        domains['add'] = []
        for iter in add_domains:
            if iter is not "":
                domains['add'].append(iter)

        domains['remove'] = []
        for iter in remove_domains:
            if iter is not "":
                domains['remove'].append(iter)

        whitelist['remove'] = []
        for iter in remove_whitelist:
            if iter is not "":
                whitelist['remove'].append(iter)

        whitelist['add'] = []
        for iter in add_whitelist:
            if iter is not "":
                whitelist['add'].append(iter)

        parms = {'mode': mode,
                 'manager_dn': managerdn,
                 'manager_password': managerpwd,
                 'search_base': searchbase,
                 'search_filter': searchfilter,
                 'search_scope': searchscope,
                 'group_attribute': groupattr,
                 'name': name,
                 'description': description,
                 'disable': disable,
                 'max_page_size': maxpagesize}
        if (len(urls['add']) > 0) or (len(urls['remove']) > 0):
            #             urls = self.cleanup_dict(urls)
            parms['server_url_changes'] = urls

        if (len(domains['remove']) > 0) or (len(domains['add']) > 0):
            #             domains = self.cleanup_dict(domains)
            parms['domain_changes'] = domains

        if (len(whitelist['add']) > 0) or (len(whitelist['remove']) > 0):
            #             whitelist = self.cleanup_dict(whitelist)
            parms['group_whitelist_value_changes'] = whitelist

        body = json.dumps(parms)
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        updateResponse = requests.put(
            self.ecsAdminClient.url + UPDATE_AUTHENTICATION_PROVIDER.format(authenticationProviderId),
            headers=headers, data=body, verify=False)
        self.commons.checkstatus(updateResponse)
        return updateResponse.json()
