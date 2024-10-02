from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator


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
    "alternative-credential-types": {
        "default_version_to_set": None
    },
    "marital-statuses": {
        "default_version_to_set": None
    },
    "person-name-types": {
        "default_version_to_set": None
    }
}


def select_resource():
    operation_list = []
    for resource in resource_list.keys():
        operation_list.append(Choice(value=resource, name=resource))
    operation_list.append(Separator())
    operation_list.append(Choice(value="Other", name="Other"))

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

    return {
        "name": action,
        "opts": resource_list[action]
    }
