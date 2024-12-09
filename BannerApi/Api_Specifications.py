from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from CommonDefaults import CommonDefaults
import json
from .ApiSpecLibrary import ApiSpecLibrary

base_url= "/IntegrationApi/api/api-specifications"

endpoint_spec_content_type="application/vnd.hedtech.integration.endpoint-specifications.v1+json"
resource_spec_content_type="application/vnd.hedtech.integration.resource-specifications.v1+json"
logic_spec_content_type="application/vnd.hedtech.integration.logic-specifications.v1+json"

class ApiSpecificationsMenu():
    bannerClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None
    apiSpecLibrary = None

    def __init__(self, bannerClient, loginSession, connection_name):
        self.bannerClient = bannerClient
        self.loginSession = loginSession
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults("banner____a__.extension_def" + connection_name)
        self.apiSpecLibrary = ApiSpecLibrary()

    def run(self):
        operations = {
            "View Api Specifications": self.opt_view_api_specifications,
            "View Api endpoint Specification": self.opt_view_api_endpoint_specification,
            "View Api resource Specification": self.opt_view_api_resource_specification,
            "View Api logic Specification": self.opt_view_api_logic_specification,
            "Clone spec to local Library": self.opt_clone_logic_specification,
            "Validate Spec in Library": self.opt_validate_specification,
            "Deploy spec from local Library": self.opt_deploy_full_specification,
            "Delete custom API spec": self.opt_delete_api_specification
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

    def _select_api_specification(self, msg="Select Spec to view in detail:"):
        responseJson = self.bannerClient.getListResource(url=base_url, loginSession=self.loginSession)

        operation_list = []
        for apispec in responseJson:
            majorVersion = ""
            if "majorVersion" in apispec:
                majorVersion = str(apispec["majorVersion"])
            operation_list.append(Choice(value=apispec, name=apispec["resource"] + ":" + majorVersion + " " + apispec["status"]))
        #print("\n".join(map(str, json.loads(response.text))))

        return inquirer.select(
            message=msg,
            choices=operation_list,
            default=None,
            height=8
        ).execute()

    def opt_view_api_specifications(self):
        action = self._select_api_specification()

        print("-------------------------")
        print("Resource:", action["resource"], " - ver", str(action["majorVersion"]), " status:",  action["status"])
        print("Json:")
        print(json.dumps(action, indent=2))
        print("-------------------------")


    def _get_api_spec_detail(self, detail_content_type, output_fn=print, action_id=None):
        if action_id is None:
            action = self._select_api_specification("Select api specification to view endpoint information")
            action_id = action["id"]
        def injectHeadersFn(headers):
            headers["Accept"] = detail_content_type
            headers["Content-type"] = detail_content_type

        response = self.bannerClient.sendGetRequest(url=base_url + "/" + action_id, loginSession=self.loginSession, injectHeadersFn=injectHeadersFn)
        responseJson = json.loads(response.text)
        output_fn(json.dumps(responseJson, indent=2))

    def opt_view_api_endpoint_specification(self):
        return self._get_api_spec_detail(endpoint_spec_content_type)

    def opt_view_api_resource_specification(self):
        return self._get_api_spec_detail(resource_spec_content_type)

    def opt_view_api_logic_specification(self):
        return self._get_api_spec_detail(logic_spec_content_type)

    def opt_clone_logic_specification(self):
        print("This step will get an api spec from Banner and save it into the local")
        print(" file system library using a new resource name and version")
        print(" it is a useful tool for starting development of a new resource")
        input("Press Enter to continue...")

        api_spec_to_clone = self._select_api_specification("Select api specification to clone")

        resource_name = inquirer.text(
            message="Enter a name for the new resource:",
            default="x-"
        ).execute()
        if resource_name == "":
            print("Cancelled")
            return

        resource_version = inquirer.text(
            message="Enter a major version the new resource:",
            default="1"
        ).execute()
        if resource_version == "":
            print("Cancelled")
            return
        resource_version = int(resource_version)

        libspec = self.apiSpecLibrary.getSpec(resource_name=resource_name, resource_version=resource_version)

        if libspec.exists():
            overrwrite = inquirer.confirm(
                message="The api spec for " + resource_name + " ver " + str(resource_version) + " exists - do you want to delete and recreate?",
                default=False
            ).execute()
            if not overrwrite:
                print("Cancelled")
                return
            libspec.delete()

        self._get_api_spec_detail(endpoint_spec_content_type, libspec.write_endpoint_json, action_id=api_spec_to_clone["id"])
        self._get_api_spec_detail(resource_spec_content_type, libspec.write_resource_json, action_id=api_spec_to_clone["id"])
        self._get_api_spec_detail(logic_spec_content_type, libspec.write_logic_json, action_id=api_spec_to_clone["id"])

    def _get_spec_from_library(self, res_msg="Select resource to deploy", ver_msg="Select major version of resource to deploy"):
        operation_list = []
        for resource_name in self.apiSpecLibrary.get_resource_name_list():
            operation_list.append(Choice(value=resource_name, name=resource_name))
        if len(operation_list) == 0:
            return None
        #print("\n".join(map(str, json.loads(response.text))))

        resource_name = inquirer.select(
            message=res_msg,
            choices=operation_list,
            default=None,
            height=8
        ).execute()

        major_versions = self.apiSpecLibrary.get_major_versions_for_resource(resource_name)
        if len(major_versions)==1:
            retVal = self.apiSpecLibrary.getSpec(resource_name=resource_name, resource_version=int(major_versions[0]))
            if not retVal.exists():
                raise Exception("Error resource selected doesn't exist")
                return None
            return retVal

        operation_list = []
        for version in major_versions:
            operation_list.append(Choice(value=int(version), name=version))
        if len(operation_list) == 0:
            raise Exception("ERROR NO VERSIONS")
            return None

        resource_version = inquirer.select(
            message=res_msg,
            choices=operation_list,
            default=None,
            height=8
        ).execute()

        retVal = self.apiSpecLibrary.getSpec(resource_name=resource_name, resource_version=resource_version)
        if not retVal.exists():
            print("Selected resource_name:", resource_name)
            print("Selected resource_version:", resource_version)
            raise Exception("Error resource selected doesn't exist")
        return retVal

    def opt_validate_specification(self):
        spec = self._get_spec_from_library()
        if spec is None:
            print("No resources in library")
            return

        while True:
            validation_errors = spec.get_validation_errors()
            if len(validation_errors) == 0:
                print("No errors found")

            for validation_error in validation_errors:
                print(validation_error.getText())

            if not inquirer.confirm(
                message="Re-run validation of " + spec.library_path,
                default=True
            ).execute():
                break


    def opt_deploy_full_specification(self):
        spec = self._get_spec_from_library()
        if spec is None:
            print("No resources in library")
            return

        validation_errors = spec.get_validation_errors()
        if len(validation_errors) != 0:
            print("This spec has validation errors. Clear them before deploying")
            return

        def find_resource():
            responseJson = self.bannerClient.getListResource(url=base_url, loginSession=self.loginSession)
            for resp in responseJson:
                if resp["resource"] == spec.resource_name:
                    return resp
            return None

        found_resource = find_resource()

        print("Selected resource to deploy:", spec.get_text())

        if found_resource:
            print("Resource has been deployed - will overwrite")
        else:
            print("This resource is not yet deployed - will create new deployment")

        print("This step will deploy and overwrite the api specification in Banner")
        if not inquirer.confirm(
                message="Continue",
                default=False
        ).execute():
            return

        if not found_resource:
            def injectHeadersFn(headers):
                headers["Accept"] = "application/json"
                headers["Content-type"] = "application/json"

            post_data = {
                "id": "00000000-0000-0000-0000-000000000000",
                "resource": spec.resource_name
            }
            response = self.bannerClient.sendPostRequest(
                url=base_url,
                loginSession=self.loginSession,
                data=json.dumps(post_data),
                injectHeadersFn=injectHeadersFn
            )
            if response.status_code != 201:
                print("Status:", response.status_code)
                print("Text:", response.text)
                raise Exception("Error creating spec")

            responseJson = json.loads(response.text)
            found_resource = find_resource()
            if responseJson["id"] != found_resource["id"]:
                raise Exception("Created resource GUID doesn't match searched for id")

        def injectHeadersEndpointFn(headers):
            headers["Accept"] = endpoint_spec_content_type
            headers["Content-type"] = endpoint_spec_content_type
        put_endpoint_response = self.bannerClient.sendPutRequest(
            url=base_url + "/" + found_resource["id"],
            loginSession=self.loginSession,
            data=json.dumps(spec.read_endpoint_dict()),
            injectHeadersFn=injectHeadersEndpointFn
        )
        if put_endpoint_response.status_code != 200:
            print("Status:", put_endpoint_response.status_code)
            print("Text:", put_endpoint_response.text)
            raise Exception("Error sending PUT request for endpoint")
        print("PUT Endpoint Success 200 returned")
        print(put_endpoint_response.text)
        print("")

        def injectHeadersResourceFn(headers):
            headers["Accept"] = resource_spec_content_type
            headers["Content-type"] = resource_spec_content_type
        put_resource_response = self.bannerClient.sendPutRequest(
            url=base_url + "/" + found_resource["id"],
            loginSession=self.loginSession,
            data=json.dumps(spec.read_resource_dict()),
            injectHeadersFn=injectHeadersResourceFn
        )
        if put_resource_response.status_code != 200:
            print("Status:", put_resource_response.status_code)
            print("Text:", put_resource_response.text)
            raise Exception("Error sending PUT request for resource")
        print("PUT resource Success 200 returned")
        print(put_resource_response.text)
        print("")

        def injectHeadersLogicFn(headers):
            headers["Accept"] = logic_spec_content_type
            headers["Content-type"] = logic_spec_content_type
        put_logic_response = self.bannerClient.sendPutRequest(
            url=base_url + "/" + found_resource["id"],
            loginSession=self.loginSession,
            data=json.dumps(spec.read_logic_dict()),
            injectHeadersFn=injectHeadersLogicFn
        )
        if put_logic_response.status_code != 200:
            print("Status:", put_logic_response.status_code)
            print("Text:", put_logic_response.text)
            print("Error sending PUT request for logic")
            return
            #raise Exception("Error sending PUT request for logic")
        print("PUT logic Success 200 returned")
        print(put_logic_response.text)
        print("")

        print("Spec deployed")

    def opt_delete_api_specification(self):
        api_spec = self._select_api_specification(msg="Select api spec to delete")
        print("Delete ", api_spec)
        if not inquirer.confirm(
                message="Are you sure",
                default=False
        ).execute():
            return

        response = self.bannerClient.sendDeleteRequest(
            url=base_url + "/" + api_spec["id"],
            loginSession=self.loginSession,
            injectHeadersFn=None
        )
        if response.status_code != 200:
            print("Status:", response.status_code)
            print("Text:", response.text)
            raise Exception("Error deleting spec")

        print("Delete successful")

