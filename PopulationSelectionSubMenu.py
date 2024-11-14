from SubMenuBaseClass import SubMenuEthosBaseClass
import json
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

def injectHeaderFN(headers):
    headers["Content-Type"] = "application/json"
    headers["accept"] = "application/json"

class PopulationSelectionSubMenu(SubMenuEthosBaseClass):
    def __init__(self, getNewEthosClientAndLoginSession, connection_name):
        super().__init__(menu_name="PopulationSelection", getNewEthosClientAndLoginSession=getNewEthosClientAndLoginSession, connection_name=connection_name)

    def _list_of_operations(self):
        return {
            "List all person-filters": self.opt_get_person_filters,
            "Get person filter by code": self.opt_get_person_filter_by_code,
            "Get persons matching filter": self.opt_get_person_matching_filter,
        }

    def _get_list_of_person_filters(self):
        retVal = []
        iterator = self.ethosClient.getResourceIterator(
            loginSession=self.loginSession,
            resourceName="person-filters"
        )
        for result in iterator:
            retVal.append(result)
        return retVal

    def _select_person_filter_id(self, msg="Select person filter"):
        operation_list = []
        for person_filter in self._get_list_of_person_filters():
            operation_list.append(
                Choice(value={
                    "id": person_filter.dict["id"],
                    "code": person_filter.dict["code"]
                }, name=person_filter.dict["code"] + " " + person_filter.dict["title"])
            )

        return inquirer.select(
            message=msg,
            choices=operation_list,
            default=None,
            height=8
        ).execute()

    def opt_get_person_filters(self):
        for result in self._get_list_of_person_filters():
            print(result.dict)


    def opt_get_person_matching_filter(self):
        filter_id = self._select_person_filter_id()
        if filter_id is None:
            return

        personFilter = {
            "personFilter": {
                "id": filter_id["id"]
            }
        }
        params = {
            "personFilter": json.dumps(personFilter)
        }

        response = self.ethosClient.sendGetRequest(
            url="/api/persons",
            loginSession=self.loginSession,
            params=params,
            injectHeadersFn=injectHeaderFN
        )

        print("response")
        if response.status_code != 200:
            print("Error")
            print("Status", response.status_code)
            print("Headers", response.headers)
            print("Text", response.text)

        print("Response returned")
        print("Total in this popsel=", response.headers["x-total-count"])
        resposneJson = json.loads(response.text)
        print(" rows in this page=", len(resposneJson))
        if not inquirer.confirm(
                message="List returned response rows",
                default=False
        ).execute():
            return

        for responseRow in resposneJson:
            print(responseRow)

    def opt_get_person_filter_by_code(self):
        filter_code_default_name = "filter_code"
        filter_code = inquirer.text(
            message="Enter filter code:",
            default=self.commonDefaults.get_default_string_value(filter_code_default_name, "ACTIVE_STUDENTS")
        ).execute()
        if filter_code=="":
            return

        criteria = {
            "code": filter_code
        }
        params = {
            "criteria": json.dumps(criteria)
        }

        response = self.ethosClient.sendGetRequest(
            url="/api/person-filters",
            loginSession=self.loginSession,
            params=params,
            injectHeadersFn=injectHeaderFN
        )

        if response.status_code != 200:
            print("Error")
            print("Status", response.status_code)
            print("Headers", response.headers)
            print("Text", response.text)

        print("Success:")
        print("Text", response.text)

        self.commonDefaults.set_default_string_value(filter_code_default_name, filter_code)





