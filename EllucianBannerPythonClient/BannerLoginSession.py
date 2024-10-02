import PythonAPIClientBase
from requests.auth import HTTPBasicAuth

class BannerLoginSession(PythonAPIClientBase.LoginSession):
    apiusername = None
    apipassword = None
    def __init__(self, apiusername, apipassword):
        self.apiusername = apiusername
        self.apipassword = apipassword

    def injectHeaders(self, headers):
        headers["Authorization"] = "Bearer " + HTTPBasicAuth._basic_auth_str(username=self.apipassword, password=self.apipassword)
