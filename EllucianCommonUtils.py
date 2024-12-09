from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from BannerApi.ApiSpecLibrary import ApiSpecLibrary


resource_list = {
    "persons": {
        "default_version_to_set": "12"
    },
    "person-holds": {
        "default_version_to_set": None
    },
    "person-visas": {
        "default_version_to_set": None
    },
    "addresses": {
        "default_version_to_set": None
    },
    "address-types": {
        "default_version_to_set": None
    },
    "alternative-credential-types": {
        "default_version_to_set": None
    },
    "marital-statuses": {
        "default_version_to_set": None
    },
    "person-name-types": {
        "default_version_to_set": None
    },
    "hesa-courses": {
        "default_version_to_set": None
    }
}

def select_custom_resource():
    operation_list = []
    api_spec_library = ApiSpecLibrary()
    for resource in api_spec_library.get_resource_name_list():
        operation_list.append(Choice(value=resource, name=resource))
    action = inquirer.select(
        message="Select a custom resource:",
        choices=operation_list,
        default="Logout",
    ).execute()
    return {
        "name": action,
        "opts": {
            "default_version_to_set": None
        }
    }



def select_resource():
    operation_list = []
    for resource in resource_list.keys():
        operation_list.append(Choice(value=resource, name=resource))
    operation_list.append(Separator())
    operation_list.append(Choice(value="Other", name="Other"))
    operation_list.append(Choice(value="Custom", name="Custom"))

    action = inquirer.select(
        message="Select a resource:",
        choices=operation_list,
        default="Logout",
    ).execute()
    if action == "Other":
        resourceName = inquirer.text(message="Enter Resource Name:").execute().strip()
        return {
            "name": resourceName,
            "opts": {
                "default_version_to_set": None
            }
        }
    if action == "Custom":
        return select_custom_resource()

    return {
        "name": action,
        "opts": resource_list[action]
    }
