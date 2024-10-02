from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import EllucianCommonUtils
from CommonDefaults import CommonDefaults
import json

class BpapiMenu():
    ethosClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None

    def __init__(self, ethosClient, loginSession, connection_name):
        self.ethosClient = ethosClient
        self.loginSession = loginSession
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults(connection_name)

    def run(self):
        operations = {
            "BPAPI person-search": self.opt_get_person_search,
            "BPAPI get_general_student": self.opt_get_general_student,
            "BPAPI emergency-contacts": self.opt_emergency_contacts
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

    def opt_get_person_search(self):
        params = {}

        def injectHeadersFn(headers):
            headers["Content-Type"] = "application/json"
            #headers["accept"] = "application/vnd.hedtech.integration.v" + version + "+json"
            headers["accept"] = "application/json"

        response = self.ethosClient.sendGetRequest(
            url="/api/person-search",
            loginSession=self.loginSession,
            params=params,
            injectHeadersFn=injectHeadersFn
        )

        print("Response:")
        print(" status", response.status_code)
        print(" text", response.text)

    def opt_get_general_student(self):
        student_id_default_name = "opt_get_general_student_student_id"

        print("""
Banner SQL to get a student ID:        
select sp.spriden_id
from spriden sp
inner join sgbstdn sg on sg.sgbstdn_pidm=sp.spriden_pidm
;
        """)

        student_id = "000020050"
        student_id = inquirer.text(
            message="Student ID:",
            default=self.commonDefaults.get_default_string_value(student_id_default_name)
        ).execute()

        params = {
            "id": student_id
        }

        def injectHeadersFn(headers):
            headers["Content-Type"] = "application/json"
            headers["accept"] = "application/json"

        response = self.ethosClient.sendGetRequest(
            url="/api/general-student-learner-and-curricula",
            loginSession=self.loginSession,
            params=params,
            injectHeadersFn=injectHeadersFn
        )

        self.commonDefaults.set_default_string_value(student_id_default_name, student_id)

        print("Response:")
        print(" status", response.status_code)
        print(" text", response.text)


    def opt_emergency_contacts(self):
        params = {
        }

        def injectHeadersFn(headers):
            headers["Content-Type"] = "application/json"
            headers["accept"] = "application/json"

        response = self.ethosClient.sendGetRequest(
            url="/api/emergency-contacts",
            loginSession=self.loginSession,
            params=params,
            injectHeadersFn=injectHeadersFn
        )

        print("Response:")
        print(" status", response.status_code)
        print(" text", response.text)

