from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import EllucianCommonUtils
from CommonDefaults import CommonDefaults
import json

base_url= "/IntegrationApi/api/extension-definitions"

class ExtensionDefsMenu():
    bannerClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None

    def __init__(self, bannerClient, loginSession, connection_name):
        self.bannerClient = bannerClient
        self.loginSession = loginSession
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults("banner____a__.extension_def" + connection_name)

    def run(self):
        operations = {
            "View Extension Definitions": self.opt_view_extension_defs,
            "Create Extension Definition": self.opt_create_extension_def,
            "Delete Extension Definition": self.opt_del_extension_def
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

    def opt_view_extension_defs(self):
        response = self.bannerClient.sendGetRequest(url=base_url, loginSession=self.loginSession)
        print("\n".join(map(str, json.loads(response.text))))

    def opt_del_extension_def(self):
        response = self.bannerClient.sendGetRequest(url=base_url, loginSession=self.loginSession)
        codes = json.loads(response.text)

        # "": my_extension_code,
        # "jsonLabel": jsonLabel,
        # "sqlProcessCode": "HEDM_EXTENSIONS",
        # "resourceName": "persons",
        # "jsonPath": "/",
        # "sqlReadRuleCode": sqlReadRuleCode,
        # "jsonPropertyType": "S",
        # "description": "Created for training",
        # "columnName": columnName

        operation_list = []
        for code in codes:
            opt_str = "ID:" + str(code["id"])
            opt_str += " extensionCode:" + code["extensionCode"]
            opt_str += " jsonLabel:" + code["jsonLabel"]
            opt_str += " resourceName:" + code["resourceName"]
            opt_str += " description:" + code["description"]
            operation_list.append(Choice(value=code["id"], name=opt_str))
        operation_list.append(Separator())
        operation_list.append(Choice(value=-1, name="Cancel"))

        selected_code = inquirer.select(
            message="Select Definition to delete:",
            choices=operation_list
        ).execute()

        if (selected_code == -1):
            return True

        def injectHeaders(headers):
            headers["Content-Type"] = "application/json"
            headers["Accept"] = "application/json"

        response = self.bannerClient.sendDeleteRequest(url= base_url + "/" + str(selected_code), loginSession=self.loginSession, injectHeadersFn=injectHeaders)
        if response.status_code != 200:
            print("There was an error deleting definition with ID " + str(selected_code) + ":", response.text, response.status_code)
        else:
            print("Delete definition successful: ", response.text)
        return True

    def opt_create_extension_def(self):
        code_default_name = "opt_create_extension_codes_code"
        code = inquirer.text(
            message="Extension Code:",
            default=self.commonDefaults.get_default_string_value(code_default_name, "RJM_TRAINING_EXTENSIONS")
        ).execute()

        jsonLabel_default_name = "opt_create_extension_codes_jsonLabel"
        jsonLabel = inquirer.text(
            message="Json Label:",
            default=self.commonDefaults.get_default_string_value(jsonLabel_default_name, "RJM_extraData")
        ).execute()

        sqlReadRuleCode_default_name = "opt_create_extension_codes_SqlReadRuleCode"
        sqlReadRuleCode = inquirer.text(
            message="Sql Read Rule Code:",
            default=self.commonDefaults.get_default_string_value(sqlReadRuleCode_default_name, "RJM_EXTRA_DATA")
        ).execute()

        columnName_default_name = "opt_create_extension_codes_columnName"
        columnName = inquirer.text(
            message="Column Name:",
            default=self.commonDefaults.get_default_string_value(columnName_default_name, "RJM_EXTRA_DATA")
        ).execute()

        resourceName_default_name = "opt_create_extension_codes_resourceName"
        resourceName = inquirer.text(
            message="Resource Name:",
            default=self.commonDefaults.get_default_string_value(resourceName_default_name, "persons")
        ).execute()

        description_default_name = "opt_create_extension_codes_description"
        description = inquirer.text(
            message="Description:",
            default=self.commonDefaults.get_default_string_value(description_default_name, "Created for training")
        ).execute()

        post_data = {
            "extensionCode": code,
            "jsonLabel": jsonLabel,
            "sqlProcessCode": "HEDM_EXTENSIONS",
            "resourceName": resourceName,
            "jsonPath": "/",
            "sqlReadRuleCode": sqlReadRuleCode,
            "jsonPropertyType": "S",
            "description": description,
            "columnName": columnName
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
            print("There was an error creating definition:", response.text, response.status_code)
        else:
            self.commonDefaults.set_default_string_value(code_default_name, code)
            self.commonDefaults.set_default_string_value(jsonLabel_default_name, jsonLabel)
            self.commonDefaults.set_default_string_value(sqlReadRuleCode_default_name, sqlReadRuleCode)
            self.commonDefaults.set_default_string_value(columnName_default_name, columnName)
            self.commonDefaults.set_default_string_value(resourceName_default_name, resourceName)
            self.commonDefaults.set_default_string_value(description_default_name, description)
            print("Create definition successful: ", response.text)

        return True