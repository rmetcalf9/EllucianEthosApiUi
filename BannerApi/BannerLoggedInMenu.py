from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import EllucianCommonUtils
from CommonDefaults import CommonDefaults
import json
from .Extension_codes import ExtensionCodesMenu
from .Extension_definitions import ExtensionDefsMenu
from .Extension_versions import ExtensionVersMenu

class LoggedInMenu():
    bannerClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None

    def __init__(self, bannerClient, loginSession, connection_name):
        self.bannerClient = bannerClient
        self.loginSession = loginSession
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults("banner____a__" + connection_name)

    def run(self):
        operations = {
            "IntegrationApi_extension_codes": self.opt_integrationapi_extension_codes,
            "IntegrationApi_extension_definitions": self.opt_integrationapi_extension_definitions,
            "IntegrationApi_extension_versions": self.opt_integrationapi_extension_versions
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

    def opt_integrationapi_extension_codes(self):
        return ExtensionCodesMenu(self.bannerClient, self.loginSession, self.connection_name).run()

    def opt_integrationapi_extension_definitions(self):
        return ExtensionDefsMenu(self.bannerClient, self.loginSession, self.connection_name).run()

    def opt_integrationapi_extension_versions(self):
        return ExtensionVersMenu(self.bannerClient, self.loginSession, self.connection_name).run()

