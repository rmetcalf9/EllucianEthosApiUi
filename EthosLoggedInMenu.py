from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import EllucianCommonUtils
from CommonDefaults import CommonDefaults
import json
import GraphQlMenu
import BpapiMenu
import EthosPerformanceTesting
from PersonManager import Menu as PersonManagerMenu
from PythonAPIClientBase.APIClientBase import APIClientException

class LoggedInMenu():
    getNewEthosClientAndLoginSession = None
    ethosClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None

    def __init__(self, getNewEthosClientAndLoginSession, connection_name):
        self.getNewEthosClientAndLoginSession = getNewEthosClientAndLoginSession
        (self.ethosClient, self.loginSession) = getNewEthosClientAndLoginSession()
        print("Login session established")
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults(connection_name)

    def run(self):
        operations = {
            "Appconfig": self.opt_appconfig,
            "Get Resource": self.opt_get_resource,
            "Get Resource List": self.opt_get_resource_list,
            "Get Person by name": self.opt_get_person_by_name,
            "Graph QL": self.opt_graph_ql,
            "Business Process API": self.opt_bpapi,
            "Performance Tests": self.opt_performance,
            "Personmanager": self.opt_personamanger,
        }
        operation_list = []
        for operation in operations:
            operation_list.append(Choice(value=operation, name=operation))

        logout_text = "Logout and Exit (" + self.connection_name + ")"

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

    def _output_resource(self, resource_val):
        if  resource_val is None:
            print("Returned None - resource not found")
        else:
            print("Returned Value", resource_val)
            print(" resourceName:", resource_val.resourceName  )
            print(" resourceID:", resource_val.resourceID )
            print(" version :", resource_val.version )
            print(" data")
            print(resource_val.dict)
            print("")

    def opt_get_resource_list(self):
        resource = EllucianCommonUtils.select_resource()
        if resource is None:
            return

        resourceItemsIterator = self.ethosClient.getResourceIterator(
            loginSession=self.loginSession,
            resourceName=resource["name"],
            params=None,
            version=resource["opts"]["default_version_to_set"],
            pageSize=5
        )

        max = 5
        cur = 0
        try:
            for resource_item in resourceItemsIterator:
                print("Result " + str(cur), resource_item.dict)
                cur += 1
                if cur > max:
                    break
        except APIClientException as err:
            print("Exception occured")
            print(err.getDescriptionString())
            return

    def opt_get_resource(self):
        resource = EllucianCommonUtils.select_resource()
        if resource is None:
            return
        resourceID_default_name = "opt_get_resource_" + resource["name"] + "_resourceID"

        resourceID = inquirer.text(
            message="Enter resource ID:",
            default=self.commonDefaults.get_default_string_value(resourceID_default_name)
        ).execute()


        resource_val = self.ethosClient.getResource(
            loginSession=self.loginSession,
            resourceName=resource["name"],
            resourceID=resourceID,
            version=resource["opts"]["default_version_to_set"]
        )
        if  resource_val is not None:
            self.commonDefaults.set_default_string_value(resourceID_default_name, resourceID)

        self._output_resource(resource_val)

    def opt_get_person_by_name(self):
        resource = EllucianCommonUtils.resource_list["persons"]

        possible_criteria = [
            "names[0]firstName",
            "names[0]lastName"
        ]
        def get_criteria_default_name(criteria_name):
            return "opt_get_person_by_name_criteria_" + criteria_name
        final_criteria = []
        for criteria in possible_criteria:
            value = inquirer.text(
                message="Criteria " + criteria + " (Blank for ignore):",
                default=self.commonDefaults.get_default_string_value(get_criteria_default_name(criteria))
            ).execute()
            if value != "":
                final_criteria.append({
                    "name": criteria,
                    "value": value
                })

        if len(final_criteria) == 0:
            print("No criteria selected")
            return

        criteria_dict = {}
        for criteria in final_criteria:
            if criteria["name"] == "names[0]firstName":
                if "names" not in criteria_dict:
                    criteria_dict["names"] = [{}]
                criteria_dict["names"][0]["firstName"] = criteria["value"]
            if criteria["name"] == "names[0]lastName":
                if "names" not in criteria_dict:
                    criteria_dict["names"] = [{}]
                criteria_dict["names"][0]["lastName"] = criteria["value"]

        version_default_name = "opt_get_person_by_name_version"
        version = inquirer.text(
            message="Enter requested version:",
            default=self.commonDefaults.get_default_string_value(version_default_name, resource["default_version_to_set"])
        ).execute()
        # empty string is ok

        maxrows_default_name = "opt_get_person_by_name_maxrows"
        maxrows = inquirer.text(
            message="Max rows to return:",
            default=self.commonDefaults.get_default_string_value(maxrows_default_name, "5")
        ).execute()

        offset_default_name = "opt_get_person_by_name_offset"
        offset = inquirer.text(
            message="Offset:",
            default=self.commonDefaults.get_default_string_value(offset_default_name, "0")
        ).execute()

        params = {"criteria": json.dumps(criteria_dict), "limit": maxrows, "offset": offset}



        def injectHeadersFn(headers):
            headers["Content-Type"] = "application/json"
            headers["accept"] = "application/vnd.hedtech.integration.v" + version + "+json"

        response = self.ethosClient.sendGetRequest(
            url="/api/persons",
            loginSession=self.loginSession,
            params=params,
            injectHeadersFn=injectHeadersFn
        )
        def get_criteria(criteria_name):
            for x in final_criteria:
                if x["name"] == criteria_name:
                    return x
            return None
        if response.status_code == 200:
            for criteria_name in possible_criteria:
                criteria = get_criteria(criteria_name)
                if criteria is None:
                    self.commonDefaults.set_default_string_value(get_criteria_default_name(criteria_name), "")
                else:
                    self.commonDefaults.set_default_string_value(get_criteria_default_name(criteria_name), criteria["value"])
            self.commonDefaults.set_default_string_value(version_default_name, version)
            self.commonDefaults.set_default_string_value(maxrows_default_name, maxrows)
            self.commonDefaults.set_default_string_value(offset_default_name, offset)

        if response.status_code != 200:
            print("Error response:")
            print(" status", response.status_code)
            print(" text", response.text)
        else:
            print("OK response")
            responseJSON = json.loads(response.text)
            print("Rows returned:", len(responseJSON))
            for row in responseJSON:
                print(row)
                print("--")

    def opt_appconfig(self):
        response = self.ethosClient.sendGetRequest(url="/appconfig", loginSession=self.loginSession)
        if response.status_code != 200:
            print("Error response:")
            print(" status", response.status_code)
            print(" text", response.text)
        else:
            obj = json.loads(response.text)
            print("ID:", obj["id"])
            print("Name:", obj["name"])
            print("Metadata:", obj["metadata"])
            print("Description:", obj["description"])
            if "subscriptions" in obj:
                print("# subscriptions:", len(obj["subscriptions"]))
            else:
                print("# subscriptions: Not present")
            print("# ownerOverrides:", len(obj["ownerOverrides"]))

            if "subscriptions" in obj:
                showsubs = inquirer.confirm(
                    message="Do you want to Show subscriptions?",
                    default=True
                ).execute()
                if showsubs:
                    for sub in obj["subscriptions"]:
                        print(sub)

            showoverrides = inquirer.confirm(
                message="Do you want to show ownerOverrides?",
                default=True
            ).execute()
            if showoverrides:
                for sub in obj["ownerOverrides"]:
                    print(sub)


    def opt_graph_ql(self):
        gralhQlMenu = GraphQlMenu.GraphQlMenu(self.ethosClient, self.loginSession, self.connection_name)
        return gralhQlMenu.run()

    def opt_bpapi(self):
        bpapiMenu = BpapiMenu.BpapiMenu(self.ethosClient, self.loginSession, self.connection_name)
        return bpapiMenu.run()

    def opt_performance(self):
        performacneMenu = EthosPerformanceTesting.Menu(self.getNewEthosClientAndLoginSession, self.connection_name)
        return performacneMenu.run()

    def opt_personamanger(self):
        personamangermenu = PersonManagerMenu(self.getNewEthosClientAndLoginSession, self.connection_name)
        return personamangermenu.run()