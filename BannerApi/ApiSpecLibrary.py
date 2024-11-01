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
