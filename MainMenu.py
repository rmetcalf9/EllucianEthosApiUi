import EthosConnectionMenu
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from EthosConnectionMenu import EthosConnectionMenu
from BannerConnectionMenu import BannerConnectionMenu

class MainMenu():

    def run(self):
        continue_program = True
        while continue_program:
            # a copy deepcopy won't copy a function reference
            default = "Connect to Ethos"
            operations = {
                default: self.opt_connect_to_ethos,
                "Connect to Banner Integration API": self.opt_connect_to_banner
            }
            main_choices = []
            for operation in operations:
                main_choices.append(Choice(value=operation, name=operation))

            action = inquirer.select(
                message="Select connection to use:",
                choices=main_choices + [Separator()] + [Choice(value=None, name="Exit")],
                default="Connect to Ethos",
                height=8
            ).execute()
            if action is None:
                continue_program = False
            else:
                print("")
                (continue_program) = operations[action]()
                print("")


    def opt_connect_to_ethos(self):
        ethosConnectionMenu = EthosConnectionMenu()
        ethosConnectionMenu.run()
        return False

    def opt_connect_to_banner(self):
        return BannerConnectionMenu().run()
