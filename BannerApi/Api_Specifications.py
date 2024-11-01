from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from CommonDefaults import CommonDefaults
import json

base_url= "/IntegrationApi/api/api-specifications"

class ApiSpecificationsMenu():
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
            "View Api Specifications": self.opt_view_api_specifications
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

    def opt_view_api_specifications(self):
        response = self.bannerClient.sendGetRequest(url=base_url, loginSession=self.loginSession)
        responseJson = json.loads(response.text)

        operation_list = []
        for apispec in responseJson:
            operation_list.append(Choice(value=apispec, name=apispec["resource"] + str(apispec["majorVersion"]) + apispec["status"]))
        #print("\n".join(map(str, json.loads(response.text))))

        action = inquirer.select(
            message="Select Spec to view in detail:",
            choices=operation_list,
            default=None,
            height=8
        ).execute()

        print("-------------------------")
        print("Resource:", action["resource"], " - ver", str(action["majorVersion"]), " status:",  action["status"])
        print("Json:")
        print(json.dumps(action, indent=2))
        print("-------------------------")

