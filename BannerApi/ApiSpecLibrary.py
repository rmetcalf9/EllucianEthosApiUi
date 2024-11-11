import os
import shutil
import json

endpoint_filename = "/endpoint.json"
logic_filename = "/logic.json"

class ApiSpecLibrary():
    library_path = None
    def __init__(self, library_path="./banner_api_spec_library"):
        self.library_path = library_path
        if not os.path.isdir(library_path):
            os.makedirs(library_path)

    def getSpec(self, resource_name, resource_version):
        return ApiSpecLibraryItem(self.library_path, resource_name, resource_version)

    def get_resource_name_list(self):
        retVal = []
        for x in os.listdir(self.library_path):
            retVal.append(x)
        return retVal

    def get_major_versions_for_resource(self, resource_name):
        retVal = []
        for x in os.listdir(self.library_path + "/" + resource_name):
            retVal.append(x)
        return retVal

class SpecValidationError():
    file = None
    text = None
    def __init__(self, file, text):
        self.file = file
        self.text = text

    def getText(self):
        return self.file.upper()[:7] + ":" + self.text

class ApiSpecLibraryItem():
    library_path = None
    resource_name = None
    resource_version = None
    def __init__(self, library_path, resource_name, resource_version):
        if resource_name.__class__.__name__ != "str":
            raise Exception("Resource name must be a string")
        if resource_version.__class__.__name__ != "int":
            raise Exception("Resource version must be an integer")
        self.library_path = library_path
        self.resource_name = resource_name
        self.resource_version = resource_version

    def get_text(self):
        return self.resource_name + ":" + str(self.resource_version)

    def _get_directory(self):
        return self.library_path + "/" + self.resource_name + "/" + str(self.resource_version)


    def get_spec_directory(self):
        directory = self._get_directory()
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return directory

    def exists(self):
        return os.path.isdir(self._get_directory())

    def delete(self):
        shutil.rmtree(self._get_directory())

    def write_endpoint_json(self, payload):
        with open(self.get_spec_directory() + endpoint_filename, 'w') as fp:
            fp.write(payload)

    def write_logic_json(self, payload):
        with open(self.get_spec_directory() + logic_filename, 'w') as fp:
            fp.write(payload)

    def _read_endpoint_dict(self):
        endpoint = None
        with open(self.get_spec_directory() + endpoint_filename, 'r') as fp:
            endpoint = json.load(fp)
        return endpoint

    def _get_endpoint_validation_errors(self):
        retVal = []
        endpoint_dict = None
        try:
            endpoint_dict = self._read_endpoint_dict()
        except Exception as err:
            retVal.append(SpecValidationError(endpoint_filename, "Invalid JSON " + str(err)))
            return retVal

        for path in endpoint_dict["paths"].keys():
            if not path.startswith("/"):
                retVal.append(SpecValidationError(endpoint_filename, "Path should start with / (Actual: " + path + ")"))
            if path[1:].split("/")[0] != self.resource_name:
                retVal.append(SpecValidationError(endpoint_filename, "Path should start with /" + self.resource_name + " (Actual: " + path + ")"))

            for method in endpoint_dict["paths"][path]:
                resource_tag_found = False
                for tag in endpoint_dict["paths"][path][method]["tags"]:
                    if tag == self.resource_name:
                        resource_tag_found = True
                if not resource_tag_found:
                    retVal.append(SpecValidationError(
                        endpoint_filename,
                        "Path " + path + " method " + method + " should have a tag " + self.resource_name + " (Actual: " + str(endpoint_dict["paths"][path][method]["tags"]) + ")"
                    ))

        if endpoint_dict["info"]["title"] != self.resource_name:
            retVal.append(SpecValidationError(
                endpoint_filename,
                "/info/title should be " + self.resource_name + " (Actual: " + endpoint_dict["info"]["title"] + ")"
            ))

        return retVal

    def _get_logic_validation_errors(self):
        return []


    def get_validation_errors(self):
        ret_errors = []
        ret_errors += self._get_endpoint_validation_errors()
        ret_errors += self._get_logic_validation_errors()
        return ret_errors
