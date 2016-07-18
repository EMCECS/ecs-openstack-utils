"""
Created on Jun 24, 2015

@author: joshia7
"""
import exceptions


class ECSException(exceptions.Exception):
    """

    """

    def __init__(self, args):
        super(ECSException, self).__init__(args)
        self.args = args
