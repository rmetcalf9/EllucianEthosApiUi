from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import json
import EllucianEthosPythonClient
import PythonAPIClientBase
import os
import copy
import EthosLoggedInMenu

CONNECITON_FILE_NAME = "_local_connections.json"

class EthosConnectionMenu():
    connections = None

    def __init__(self):
        self.connections = {}
        self.load_connections()

    def load_connections(self):
        self.connections = {}
        if os.path.isfile(CONNECITON_FILE_NAME):
            with open(CONNECITON_FILE_NAME) as json_data:
                self.connections = copy.deepcopy(json.load(json_data))

    def save_connections(self):
        with open(CONNECITON_FILE_NAME, 'w') as fp:
            output_data = json.dumps(self.connections, indent=4, sort_keys=True)
            fp.write(output_data)

    def run(self):
        self.main_menu()

    def main_menu(self):
        continue_program = True
        while continue_program:
            # a copy deepcopy won't copy a function reference
            operations = {
                "Add Ethos Connection": self.opt_add_ethos_connection
            }
            # relying on the fact that the only operations added are the main choices
            main_choices = []
            for operation in operations:
                main_choices.append(Choice(value=operation, name=operation))

            connection_choices = []
            def get_connection_fn(connection):
                def F():
                    self.connect(connection)
                return F

            first_connection = None
            print("self conns IN LOOP", self.connections)
            for connection in self.connections:
                prompt_string = "Connect to " + connection
                if first_connection is None:
                    first_connection = prompt_string
                operations[prompt_string] = get_connection_fn(connection)
                connection_choices.append(Choice(value=prompt_string, name=prompt_string))

            action = inquirer.select(
                message="Select connection to use:",
                choices=connection_choices + [Separator()] + main_choices + [
                    Separator(),
                    Choice(value=None, name="Exit"),
                ],
                default=first_connection,
                height=8
            ).execute()
            if action is None:
                continue_program = False
            else:
                print("")
                (continue_program) = operations[action]()
                print("")

    def opt_add_ethos_connection(self):
        print("opt_add_ethos_connection self", self)
        name = inquirer.text(message="Enter name of connection:").execute()
        if name == "":
            return True
        if name in self.connections.keys():
            print("ERROR Connection with this name exists")
            return True

        endpoint = inquirer.text(message="Enter Ethos endpoint:", default="https://integrate.elluciancloud.ie").execute()
        if endpoint == "":
            return True
        apikey = inquirer.secret(message="Enter APIkey from Ethos:").execute()
        if apikey == "":
            return True

        connection = {
            "name": name,
            "endpoint": endpoint,
            "apikey": apikey
        }

        self.connections[name] = connection
        ##print("self conns IN ADD Before save", self.connections)
        self.save_connections()
        ##print("self conns IN ADD After save", self.connections)

        print("Connection ", name, " added")
        return True

    def connect(self, connection_name):
        connection = self.connections[connection_name]
        print("Connecting to", connection["name"])


        def getNewEthosClientAndLoginSession():
            ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(
                baseURL=connection["endpoint"],
                mock=None,
                verboseLogging=PythonAPIClientBase.VerboseLoggingOutputAllClass(
                    call=True,
                    include_data=True,
                    result=False
                )
            )
            loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=connection["apikey"])
            return (ethosClient, loginSession)

        loggedInMenu = EthosLoggedInMenu.LoggedInMenu(getNewEthosClientAndLoginSession, connection_name)
        return loggedInMenu.run()

