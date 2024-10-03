from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import EllucianCommonUtils
from CommonDefaults import CommonDefaults
import json

base_url= "/IntegrationApi/api/extension-versions"

class ExtensionVersMenu():
    bannerClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None

    def __init__(self, bannerClient, loginSession, connection_name):
        self.bannerClient = bannerClient
        self.loginSession = loginSession
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults("banner____a__.extension_ver" + connection_name)

    def run(self):
        operations = {
            "View Extension Versions": self.opt_view_extension_vers,
            "Create Extension Version": self.opt_create_extension_ver,
            "Delete Extension Version": self.opt_del_extension_ver
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

    def _get_ver_id(self, prompt="Select Version:"):
        def injectHeaders(headers):
            headers["Content-Type"] = "application/json"
            headers["Accept"] = "application/json"
        response = self.bannerClient.sendGetRequest(url= base_url, loginSession=self.loginSession, injectHeadersFn=injectHeaders)
        response_json = json.loads(response.text)

        operation_list = []
        for cur_response in response_json:
            operation_list.append(Choice(value=cur_response["id"], name=self._get_str_fn(cur_response)))
        operation_list.append(Separator())
        operation_list.append(Choice(value=-1, name="Cancel"))

        return inquirer.select(
            message=prompt,
            choices=operation_list
        ).execute()



    def _get_str_fn(self, dict):
        sp='                           '
        return f"{(sp  + str(dict['id']))[-3:]} {(dict['extensionCode'] + sp)[:28]} {(dict['resourceName'] + sp)[:25]} {dict['knownMediaType']}"

    def opt_view_extension_vers(self):
        def injectHeaders(headers):
            headers["Content-Type"] = "application/json"
            headers["Accept"] = "application/json"
        response = self.bannerClient.sendGetRequest(url= base_url, loginSession=self.loginSession, injectHeadersFn=injectHeaders)
        print("id  ExtensionCode                resourceName              knownMediaType")
        print("\n".join(map(self._get_str_fn,json.loads(response.text))))

    def opt_del_extension_ver(self):
        ver_id = self._get_ver_id()
        if ver_id == -1:
            return True

        def injectHeaders(headers):
            headers["Content-Type"] = "application/json"
            headers["Accept"] = "application/json"

        response = self.bannerClient.sendDeleteRequest(url= base_url + "/" + str(ver_id), loginSession=self.loginSession, injectHeadersFn=injectHeaders)
        if response.status_code != 200:
            print("There was an error deleting version with ID " + str(ver_id) + ":", response.text, response.status_code)
        else:
            print("Delete version successful: ", response.text)
        return True


        return True

    def opt_create_extension_ver(self):
        extensionCode_default_name = "opt_create_extension_codes_extensionCode"
        extensionCode = inquirer.text(
            message="Extension Code:",
            default=self.commonDefaults.get_default_string_value(extensionCode_default_name, "RJM_TRAINING_EXTENSIONS")
        ).execute()

        comment_default_name = "opt_create_extension_codes_comment"
        comment = inquirer.text(
            message="Comment:",
            default=self.commonDefaults.get_default_string_value(comment_default_name, "Created in training")
        ).execute()

        resourceName_default_name = "opt_create_extension_codes_resourceName"
        resourceName = inquirer.text(
            message="Resource Name:",
            default=self.commonDefaults.get_default_string_value(resourceName_default_name, "persons")
        ).execute()

        knownMediaType_default_name = "opt_create_extension_codes_knownMediaType"
        knownMediaType = inquirer.text(
            message="knownMediaType:",
            default=self.commonDefaults.get_default_string_value(knownMediaType_default_name, "application/json")
        ).execute()

        post_data = {
          "extensionCode": extensionCode,
          "comment": comment,
          "resourceName": resourceName,
          "knownMediaType": knownMediaType
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
            print("There was an error creating version:", response.text, response.status_code)
        else:
            self.commonDefaults.set_default_string_value(extensionCode_default_name, extensionCode)
            self.commonDefaults.set_default_string_value(comment_default_name, comment)
            self.commonDefaults.set_default_string_value(resourceName_default_name, resourceName)
            self.commonDefaults.set_default_string_value(knownMediaType_default_name, knownMediaType)
            print("Create version successful: ", response.text)

        return True

