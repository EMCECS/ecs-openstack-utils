"""
Created on Jul 6, 2015

@author: joshia7
"""

import simplejson as json


class ACL:
    """
    DTO for ACL
    """

    def __init__(self, bucket_id, namespace, owner, user, userperm, group,
                 groupperm, customgroup, cgperm, permission):
        self.bucket_id = bucket_id
        self.namespace = namespace
        self.owner = owner
        self.user = user
        self.userperm = userperm
        self.group = group
        self.groupperm = groupperm
        self.customgroup = customgroup
        self.cgperm = cgperm
        self.permission = permission

    def getJSON(self):
        """
        Convert ACL object to JSON
        """
        params = dict()
        acl = dict()
        user_acl = dict()
        group_acl = dict()
        customgroup_acl = dict()
        user_acl['user'] = self.user
        user_acl['pemission'] = self.userperm.split(',')

        group_acl['group'] = self.group
        group_acl['pemission'] = self.groupperm.split(',')

        customgroup_acl['customgroup'] = self.customgroup
        customgroup_acl['pemission'] = self.cgperm.split(',')

        acl['user_acl'] = user_acl
        acl['group_acl'] = group_acl
        acl['customgroup_acl'] = customgroup_acl
        acl['owner'] = self.owner
        params['bucket'] = self.bucket_id
        params['namespace'] = self.namespace
        params['acl'] = acl

        return json.dumps(params)
