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
            "View Extension Codes": self.opt_view_extension_codes,
            "Create Extension Code": self.opt_create_extension_codes,
            "Delete Extension Code": self.opt_del_extension_codes
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

    def opt_del_extension_codes(self):
        response = self.bannerClient.sendGetRequest(url=base_url, loginSession=self.loginSession)
        codes = json.loads(response.text)

        operation_list = []
        for code in codes:
            opt_str = "ID:" + str(code["id"]) + " code:" + code["code"] + " description:" + code["description"]
            operation_list.append(Choice(value=code["id"], name=opt_str))
        operation_list.append(Separator())
        operation_list.append(Choice(value=-1, name="Cancel"))

        selected_code = inquirer.select(
            message="Select Code to delete:",
            choices=operation_list
        ).execute()

        if (selected_code == -1):
            return True

        def injectHeaders(headers):
            headers["Content-Type"] = "application/json"
            headers["Accept"] = "application/json"

        response = self.bannerClient.sendDeleteRequest(url= base_url + "/" + str(selected_code), loginSession=self.loginSession, injectHeadersFn=injectHeaders)
        if response.status_code != 200:
            print("There was an error deleting code with ID " + str(selected_code) + ":", response.text, response.status_code)
        else:
            print("Delete code successful: ", response.text)
        return True

    def opt_create_extension_codes(self):
        code_default_name = "opt_create_extension_codes_code"
        code = inquirer.text(
            message="Extension Code Name:",
            default=self.commonDefaults.get_default_string_value(code_default_name, "RJM_TRAINING_EXTENSIONS")
        ).execute()

        post_data = {
            "code": code,
            "description": "Code added as part of training"
        }
        def injectHeaders(headers):
            headers["Content-Type"] = "application/json"
            headers["Accept"] = "application/json"

        response = self.bannerClient.sendPostRequest(
            url=base_url,
            loginSession=self.loginSession,
            injectHeadersFn=injectHeaders,
            data=json.dumps(post_data)
        )
        if response.status_code != 201:
            print("There was an error creating code:", response.text, response.status_code)
        else:
            self.commonDefaults.set_default_string_value(code_default_name, code)
            print("Create code successful: ", response.text)

        return True
