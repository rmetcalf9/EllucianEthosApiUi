import PythonAPIClientBase.APIClientBase
from .BannerLoginSession import BannerLoginSession
import json

class BannerApiClient(PythonAPIClientBase.APIClientBase):

    def __init__(self, baseURL, mock=None, verboseLogging=PythonAPIClientBase.VerboseLoggingNullLogClass()):
        super().__init__(baseURL=baseURL, mock=mock, forceOneRequestAtATime=True, verboseLogging=verboseLogging)

    def getLoginSessionFromUsernameAndPassword(self, apiusername, apipassword):
        return BannerLoginSession(apiusername=apiusername, apipassword=apipassword)


    def _getListResource(self, url, loginSession, offset, prevresults, limit):
        params = {
            "limit": limit,
            "offset": offset
        }
        response = self.sendGetRequest(url=url, loginSession=loginSession, params=params)
        responseJson = json.loads(response.text)
        results = prevresults + responseJson
        if len(responseJson)==0:
            return results
        return self._getListResource(url, loginSession, offset + len(responseJson), results, limit)


    def getListResource(self, url, loginSession, limit=25):
        return self._getListResource(url, loginSession, 0, [], limit)

        return responseJson
