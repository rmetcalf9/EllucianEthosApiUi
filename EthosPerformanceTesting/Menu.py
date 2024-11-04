from CommonDefaults import CommonDefaults
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import os
import json
from .TestRunner import TestRunner

SAVE_FILE_NAME="_performance_tests.json"

class Menu():
    ethosClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None

    saved_data = None

    def __init__(self, ethosClient, loginSession, connection_name):
        self.ethosClient = ethosClient
        self.loginSession = loginSession
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults(connection_name)
        self.saved_data = {}

        if os.path.isfile(SAVE_FILE_NAME):
            with open(SAVE_FILE_NAME) as json_data:
                self.saved_data = json.load(json_data)

    def _save_tests_to_file(self):
        with open(SAVE_FILE_NAME, 'w') as fp:
            output_data = json.dumps(self.saved_data, indent=4, sort_keys=True)
            fp.write(output_data)

    def run(self):
        operations = {
            "Run performance tests": self.opt_run_test,
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

    def _select_or_create_performance_test(self):
        if len(self.saved_data.keys()) > 0:
            operation_list = []
            for operation in self.saved_data.keys():
                operation_list.append(Choice(value=operation, name=operation))

            action = inquirer.select(
                message="Select test to run:",
                choices=operation_list + [
                    Separator(),
                    Choice(value=None, name="Create new test"),
                ],
                default=list(self.saved_data.keys())[0],
                height=8
            ).execute()
            if action is not None:
                return self.saved_data[action]

        test_name = None
        while test_name == None:
            inpval = inquirer.text(
                message="Enter a name for this test:",
                default=""
            ).execute()
            if inpval == "":
                print("Cancelled")
                return
            if inpval in self.saved_data.keys():
                print("Test with that name already exists")
            else:
                test_name = inpval

        # creation
        resource_names_text = inquirer.text(
            message="Enter a comma separated list of resources to test:",
            default=""
        ).execute()
        if resource_names_text == "":
            print("Cancelled")
            return None

        num_concurrent = inquirer.text(
            message="Number of concurrent runs:",
            default="10"
        ).execute()
        if num_concurrent == "":
            print("Cancelled")
            return None
        num_concurrent = int(num_concurrent)

        resources = []
        for x in resource_names_text.split(","):
            resources.append(x.strip().lower())

        test = {
            "name": test_name,
            "resources": resources,
            "num_concurrent": num_concurrent
        }

        print("Is the following correct?")
        print(test)
        isok = inquirer.confirm(
            message="Is this correct?",
            default=True
        ).execute()
        if not isok:
            return None

        self.saved_data[test["name"]] = test
        self._save_tests_to_file()

        return test

    def opt_run_test(self):
        performance_test_name = self._select_or_create_performance_test()
        if performance_test_name is None:
            return

        testRunner = TestRunner(self.ethosClient, self.loginSession, performance_test_name)
        testRunner.run_test()

