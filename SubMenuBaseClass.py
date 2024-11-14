from CommonDefaults import CommonDefaults
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

class SubMenuEthosBaseClass():
    getNewEthosClientAndLoginSession = None
    connection_name = None
    commonDefaults = None
    ethosClient = None
    loginSession = None

    def __init__(self, menu_name, getNewEthosClientAndLoginSession, connection_name):
        self.getNewEthosClientAndLoginSession = getNewEthosClientAndLoginSession
        (self.ethosClient, self.loginSession) = getNewEthosClientAndLoginSession()
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults(connection_name + ":" + menu_name)

    def run(self):
        operations = self._list_of_operations()
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

    def _list_of_operations(self):
        raise Exception("Error should be overridden")

        # return {
        #     "Person find or create - Match a person no creation": self.opt_person_search,
        # }