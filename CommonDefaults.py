# This class stores and supplies common defaults
#  it saves these on disk as they are changed
import os
import json

DEFAULT_FILE_NAME = "_local_defaults.json"

class CommonDefaults():
    default_values = None
    connection_name = None

    def __init__(self, connection_name):
        self.default_values = {}
        self.connection_name = connection_name
        if os.path.isfile(DEFAULT_FILE_NAME):
            with open(DEFAULT_FILE_NAME) as json_data:
                self.default_values = json.load(json_data)

    def _save_to_file(self):
        with open(DEFAULT_FILE_NAME, 'w') as fp:
            output_data = json.dumps(self.default_values, indent=4, sort_keys=True)
            fp.write(output_data)

    def get_default_string_value(self, default_name, default_if_no_default=""):
        if self.connection_name not in self.default_values:
            return default_if_no_default
        if default_name not in self.default_values[self.connection_name]:
            return default_if_no_default
        return self.default_values[self.connection_name][default_name]

    # only call this if call got a 2xx response
    def set_default_string_value(self, default_name, value):
        if self.connection_name not in self.default_values:
            self.default_values[self.connection_name] = {}
        self.default_values[self.connection_name][default_name] = value
        self._save_to_file()