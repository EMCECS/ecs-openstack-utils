"""
Created on Jun 24, 2015

@author: joshia7
"""

import requests
from httplib import HTTPException
from ecsmgmt.exception.ecsexception import ECSException


class Commons:
    """
    Utility class to validate responses
    """

    def checkstatus(self, response):
        """
        Check the HTTP status code of the response
        :param response:JSON response
        """
        if 299 < response.status_code < 500:
            response_description = response.json()
            detailed_description = str(response_description['code']) + ":" + response_description['description']
            print "Description of error is " + detailed_description
            raise ECSException(detailed_description)

        elif response.status_code > 499:
            raise HTTPException

        return True
