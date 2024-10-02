import PythonAPIClientBase.APIClientBase
from .BannerLoginSession import BannerLoginSession

class BannerApiClient(PythonAPIClientBase.APIClientBase):

    def __init__(self, baseURL, mock=None, verboseLogging=PythonAPIClientBase.VerboseLoggingNullLogClass()):
        super().__init__(baseURL=baseURL, mock=mock, forceOneRequestAtATime=True, verboseLogging=verboseLogging)

    def getLoginSessionFromUsernameAndPassword(self, apiusername, apipassword):
        return BannerLoginSession(apiusername=apiusername, apipassword=apipassword)
