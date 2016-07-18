"""
Created on Jul 6, 2015

@author: joshia7
"""
import simplejson as json


class AuthProvider:
    """
    DTO for AuthProvider data
    """

    def __init__(self, mode, server_urls, managerdn, manager_password, domains, search_base, search_filter,
                 group_attribute, group_whitelist_values=None, name=None,
                 description=None, disable=None, search_scope=None, max_page_size=None, validate_certificates=None):
        self.mode = mode
        self.server_urls = server_urls
        self.managerdn = managerdn
        self.manager_password = manager_password
        self.domains = domains
        self.search_base = search_base
        self.search_filter = search_filter
        self.group_whitelist_values = group_whitelist_values
        self.name = name
        self.description = description
        self.disable = disable
        self.search_scope = search_scope
        self.max_page_size = max_page_size
        self.validate_certificates = validate_certificates
        self.group_attribute = group_attribute

    def getJSON(self):
        """
        Convert AuthProvider Object to JSON
        """
        params = dict()
        params['server_urls'] = self.server_urls
        params['domains'] = self.domains
        params['group_whitelist_values'] = self.group_whitelist_values
        params['mode'] = self.mode
        params['name'] = self.name
        params['description'] = self.description
        params['disable'] = self.disable
        params['manager_dn'] = self.managerdn
        params['manager_password'] = self.manager_password
        params['search_base'] = self.search_base
        params['search_filter'] = self.search_filter
        params['search_scope'] = self.search_filter
        params['group_attribute'] = self.group_attribute
        params['max_page_size'] = self.max_page_size
        params['validate_certificates'] = self.validate_certificates

        return json.dumps(params)

# def getUpdateJSON
