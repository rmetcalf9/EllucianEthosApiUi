from SubMenuBaseClass import SubMenuEthosBaseClass

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import os
import json


def injectHeaderFN(headers):
    headers["Content-Type"] = "application/json"
    headers["accept"] = "application/json"


class Menu(SubMenuEthosBaseClass):
    def __init__(self, getNewEthosClientAndLoginSession, connection_name):
        super().__init__(menu_name="PersonManager", getNewEthosClientAndLoginSession=getNewEthosClientAndLoginSession, connection_name=connection_name)

    def _list_of_operations(self):
        return {
            "Person find or create - Match a person no creation": self.opt_person_search,
        }

    def opt_person_search(self):
        params = {}

        first_name = inquirer.text(
            message="First name to match with (Blank to not match with first name):",
            default=""
        ).execute()
        last_name = inquirer.text(
            message="Last name to match with (Blank to not match):",
            default=""
        ).execute()
        dob = inquirer.text(
            message="Date of birth to match with YYYY-MM-DD (Blank to not match):",
            default="1979-11-22"
        ).execute()

        if first_name == "":
            first_name = None
        if last_name == "":
            last_name = None
        if dob == "":
            dob = None

        data = {
            "skipCreate": True,
            "skipVerification": True,
            "skipUpdate": True,
            "source": "ellucianEthosApiUITest",
            "confidential": False,
            "otherInterestedSources": [
            ],
            "persons": {
                "dateOfBirth": dob,
                "names": [
                    {
                        "status": "active",
                        "firstName": first_name,
                        "fullName": first_name + " " + last_name,
                        "middleName": "James",
                        "lastName": last_name,
                    }
                ]
            }
        }

        result = self.ethosClient.sendPostRequest(
            url="/api/person-find-or-create-requests",
            params=params,
            data=json.dumps(data),
            loginSession=self.loginSession,
            injectHeadersFn=injectHeaderFN
        )
        if result.status_code != 201:
            print("Response:", result.status_code)
            print("Response test:", result.text)
            raise Exception("Exception returned")

        resultJson = json.loads(result.text)
        print("Received response:", resultJson)

        requestId = resultJson["id"]
        requestStatus = resultJson["status"]
        print("RequestId:", requestId)
        print("Status:", requestStatus)

        return self._get_request_update(requestId)

    def _get_request_update(self, requestId):
        if not inquirer.confirm(
            message="Re-query person manager to get update",
            default=True
        ).execute():
            return

        result = self.ethosClient.sendGetRequest(
            url="/api/person-find-or-create-requests/" + requestId,
            params=None,
            loginSession=self.loginSession,
            injectHeadersFn=injectHeaderFN
        )
        print("Result:", result.status_code)
        print("Body:", result.text)

        return self._get_request_update(requestId)

