import logging
import urllib2

from TokenGetter import TokenGetter

from DataWriter import writeDataToFile
LOG = logging.getLogger(name="autoWaker")

"""
  Used to query the API so we can get the data.
  
  To be implemented:
    getClientSecret() make it so that we don't hard code the client's secret >.>
    breaking the MakeAPICall() up.
    Logging
    
  Author: Alex Hoff
  License: ---
"""
class APIHandler():
    def __init__(self, ini_file, out_file, key_getter):
        self.ini_file_ = ini_file
        self.out_file_ = out_file
        self.key_getter_ = key_getter
    
    @classmethod
    def fromfilename(cls, filename):
        data = open(filename).readlines()
        self.ini_file_ = data[0].strip()
        self.out_file_ = data[1].strip()
        self.key_getter_ = TokenGetter(data[2].strip())
        
    
    #  This makes an API call to retrieve data from fitbit.
    #  Returns:
    #   callSucceeded, callData
    #   callSucceeded - boolean that holds whether or not this call was  good.
    #   callData - the data returned from the call.
    def makeAPICall(self):
        #Start the request
        access_token, refresh_token = self.key_getter_.getTokens()
        LOG.info('The passed access_token to MakeAPICall is ' + str(access_token))
        req = self.makeReq(access_token)
        try:
            return self.callAPI(req)
            
        # Catch errors, e.g. A 401 error that signifies the need for a new access token
        except urllib2.URLError as e:
            LOG.info('Initial call to the URL failed.')
            http_error_message = e.read()
            LOG.info('ERROR message: \n   ' + str(http_error_message))
            
            # See what the error was
            if (e.code == 401) and (http_error_message.find("Access token expired") > 0):
                LOG.info('ERROR was out of date tokens, refreshing tokens.')
                access_token, refresh_token = self.key_getter_.getNewAccessToken(refresh_token)
                return self.makeAPICall()
            else:
                if(refresh_token!=None) and (http_error_message.find("Refresh token invalid: ")):
                    LOG.error('Refresh token was invalid.')
                    raise IOError, 'Need to refresh tokens using new a new auth token.'
                self.key_getter_.setTokens(access_token = access_token, refresh_token = refresh_token)
                return self.makeAPICall()
                #return self.makeAPICall(access_token, refresh_token)
            #TODO: catch other errors
            LOG.error('API call failed and it was not out of date tokens.')
            return False, 'ERROR'
    #End MakeAPICall()
    
    def cancelIfAPICallBad(self):
        api_call_ok, api_response = self.makeAPICall()
        if not api_call_ok:
            return -1
        else:
            return api_response
            
    def callAPI(req):
        LOG.info('Trying to open the URL')
        response = urllib2.urlopen(req)
        LOG.info('Reading the response')
        full_response = response.read()
        writeDataToFile(data = full_response, location = self.out_file_)
        LOG.info('Call to the URL succeeded.')
        return True, full_response
    
    def makeReq(access_token):
        req = urllib2.Request(self.ini_file_)
        req.add_header('Authorization', 'Bearer ' + access_token)
        LOG.info("Url is: " + str(self.ini_file_))
    
    #######CLASS VARIABLES#########
    key_getter_ = None
    ini_file_ = None
    out_file_ = None
    #######CLASS VARIABLES#########

#End APIHandler class