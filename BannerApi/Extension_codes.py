from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import EllucianCommonUtils
from CommonDefaults import CommonDefaults
import json

base_url = "/IntegrationApi/api/extension-codes"

class ExtensionCodesMenu():
    bannerClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None

    def __init__(self, bannerClient, loginSession, connection_name):
        self.bannerClient = bannerClient
        self.loginSession = loginSession
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults("banner____a__.extension_codes" + connection_name)

    def run(self):
        operations = {
            "View Extension Codes": self.opt_view_extension_codes
        }
        operation_list = []
        for operation in operations:
            operation_list.append(Choice(value=operation, name=operation))

        logout_text = "Back (" + self.connection_name + ")"

        action = inquirer.select(
            message="Select an action:",
            choices=operation_list + [
                Separator(),
                Choice(value=None, name=logout_text),
            ],
            default=logout_text,
            height=8
        ).execute()
        if action is None:
            return False
        print("")
        operations[action]()
        print("")
        self.run()

    def opt_view_extension_codes(self):
        response = self.bannerClient.sendGetRequest(url=base_url, loginSession=self.loginSession)
        print("\n".join(map(str, json.loads(response.text))))


