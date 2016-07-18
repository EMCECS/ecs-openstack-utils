"""
Created on Jul 6, 2015

@author: joshia7
"""
from ecsmgmt.util.messageconstants import *
import simplejson as json
import requests
from ecsmgmt.util.urlconstants import *
from ecsmgmt.util.commons import Commons


class VDC:
    """
    Class for managing the attributes of a virtual data center (VDC).
    """

    def __init__(self, ECSAdminClient, token):
        self.ecsAdminClient = ECSAdminClient
        self.token = token
        self.commons = Commons()

    def insertVDCAttributes(self, vdcName, vdcNewName, interVdcEndPoints, secretKeys):
        """
        Inserts the attributes for the current VDC or a VDC which you want the current VDC to connect
        :param vdcName:VDC name for which mapping needs to be inserted
        :param vdcNewName:Name of VDC to be inserted
        :param interVdcEndPoints:End points for the VDC
        :param secretKeys:Secret key to encrypt communication between VDC
        """
        assert vdcName is not None, MESSAGE_VDC_NAME_REQUIRED
        assert vdcNewName is not None, MESSAGE_VDC_NEW_NAME_REQUIRED
        assert interVdcEndPoints is not None, MESSAGE_INTERVDC_END_POINTS_REQUIRED
        assert secretKeys is not None, MESSAGE_SECRET_KEYS_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        body = {"vdcName": vdcName,
                "interVdcEndPoints": interVdcEndPoints,
                "secretKeys": secretKeys}
        body = json.dumps(body)
        insertResponse = requests.put(self.ecsAdminClient.url + INSERT_VDC_ATTRIBUTES.format(vdcName), data=body,
                                      headers=headers, verify=False)
        if self.commons.checkstatus(insertResponse):
            return True
        else:
            return False

    def deactivateVDC(self, vdcId):
        """
        Deactivates and deletes a VDC
        :param vdcId:VDC identifier for which VDC Information needs to be deleted.
        """
        assert vdcId is not None, MESSAGE_VDC_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        deleteResponse = requests.post(self.ecsAdminClient.url + DEACTIVATE_AND_DELETE_VDC.format(vdcId),
                                       headers=headers, verify=False)
        if self.commons.checkstatus(deleteResponse):
            return True
        else:
            return False

    def getVDCDetailsByName(self, vdcName):
        """
        Gets the details for a VDC, the identity of which is specified by its name
        :param vdcName:Name of the VDC for which details are to be retrieved
        """
        assert vdcName is not None, MESSAGE_VDC_NAME_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getDetails = requests.get(self.ecsAdminClient.url + GET_VDC_BY_NAME.format(vdcName), headers=headers,
                                  verify=False)
        self.commons.checkstatus(getDetails)
        return getDetails.json()

    def getVDCByID(self, vdcId):
        """
        Gets the details for a VDC the identity of which is specified by its VDC identifier.
        :param vdcId:Identifier of VDC for which details are is to be retrieved
        """
        assert vdcId is not None, MESSAGE_VDC_ID_REQUIRED
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getDetails = requests.get(self.ecsAdminClient.url + GET_VDC_BY_ID.format(vdcId), headers=headers, verify=False)
        self.commons.checkstatus(getDetails)
        return getDetails.json()

    def getVDCLocalDetails(self):
        """
        Gets the details for the local VDC
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getDetails = requests.get(self.ecsAdminClient.url + GET_VDC_LOCAL_DETAILS, headers=headers, verify=False)
        self.commons.checkstatus(getDetails)
        return getDetails.json()

    def getVDCSecretKey(self):
        """
        Gets the details for the local VDC
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getDetails = requests.get(self.ecsAdminClient.url + GET_VDC_SECRET_KEY, headers=headers, verify=False)
        self.commons.checkstatus(getDetails)
        return getDetails.json()

    def getAllVDCList(self):
        """
        Gets the details of all configured VDCs
        """
        headers = {'x-sds-auth-token': self.token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        getDetails = requests.get(self.ecsAdminClient.url + GET_VDC_LIST, headers=headers, verify=False)
        self.commons.checkstatus(getDetails)
        return getDetails.json()
