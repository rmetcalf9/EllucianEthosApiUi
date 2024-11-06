


from CommonDefaults import CommonDefaults
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import os
import json


class Menu():
    getNewEthosClientAndLoginSession = None
    connection_name = None
    commonDefaults = None
    ethosClient = None
    loginSession = None

    def __init__(self, getNewEthosClientAndLoginSession, connection_name):
        self.getNewEthosClientAndLoginSession = getNewEthosClientAndLoginSession
        (self.ethosClient, self.loginSession) = getNewEthosClientAndLoginSession()
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults(connection_name)


    def run(self):
        operations = {
            "Person find or create": self.opt_person_search,
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

    def opt_person_search(self):
        params = {}
        data = {}

        data = {
            "skipCreate": True,
            "skipVerification": True,
            "skipUpdate": True,
            "source": "ellucianEthosApiUITest",
            "confidential": False,
            "otherInterestedSources": [
            ],
            "persons": {
                "id": "00000000-0000-0000-0000-000000000000",
                "confidential": False,
                "dateOfBirth": "2004-05-31",
                "birthCountry": "USA",
                "birthRegion": "NorthAmerica",
                "birthLocality": "Reston",
                "dateDeceased": None,
                "deceased": "notDeceased",
                "races": [
                    {
                        "reporting": {
                            "code": "USA",
                            "racialCategory": "americanIndianOrAlaskaNative"
                        }
                    }
                ],
                "ethnicities": [
                    {
                        "reporting": {
                            "ethnicCategory": "nonHispanic",
                            "code": "USA"
                        }
                    }
                ],
                "religion": {
                    "id": "472c2097-5d7a-4d6f-b95a-85b30bf6e36c"
                },
                "maritalStatus": [
                    {
                        "maritalCategory": "single"
                    }
                ],
                "gender": {
                    "value": "female"
                },
                "citizenship": [
                    {
                        "status": "citizen",
                        "country": "USA"
                    }
                ],
                "languages": [
                    {
                        "code": "ENG",
                        "preference": "primary"
                    }
                ],
                "names": [
                    {
                        "status": "active",
                        "fullName": "Jennifer Lewis",
                        "firstName": "Jennifer",
                        "middleName": None,
                        "lastName": "Lewis",
                        "preference": "preferred",
                        "type": {
                            "category": "legal"
                        },
                        "professionalAbbreviations": [
                            "Ph.D"
                        ],
                        "prefix": "Ms."
                    }
                ],
                "addresses": [
                    {
                        "status": "active",
                        "addressLines": [
                            "1029 Sailboat Ave"
                        ],
                        "countryCode": "USA",
                        "countryTitle": "United States of America",
                        "locality": "Herndon",
                        "postalCode": "20170",
                        "regionTitle": "Virginia",
                        "regionCode": "US-VA",
                        "subRegionCode": "FAX",
                        "subRegionTitle": "Fairfax",
                        "type": {
                            "detail": {
                                "id": "d8cdba43-0a36-4acc-bcde-23de54c1cced"
                            },
                            "category": "mailing"
                        }
                    }
                ],
                "phones": [
                    {
                        "status": "active",
                        "number": "703-444-2233",
                        "type": {
                            "category": "home"
                        },
                        "countryCallingCode": "+1",
                        "preference": "primary"
                    }
                ],
                "emails": [
                    {
                        "status": "active",
                        "address": "jlewis@example.com",
                        "type": {
                            "category": "personal"
                        }
                    }
                ],
                "socialMedia": [
                    {
                        "type": "linkedIn",
                        "status": "active",
                        "address": "linkedin.com/in/jennlewis/"
                    }
                ],
                "identityDocuments": [
                    {
                        "status": "active",
                        "documentId": "221384755",
                        "type": {
                            "category": "ssn"
                        },
                        "countryCode": "USA"
                    }
                ],
                "visas": [
                    {
                        "status": "active",
                        "type": {
                            "category": "nonImmigrant",
                            "detail": {
                                "id": "80bbd446-0f35-49d1-9097-09bd834ed5d6"
                            }
                        },
                        "visaId": "155657789",
                        "requestedOn": "2020-12-12",
                        "issuedOn": "2020-12-12",
                        "expiresOn": "2030-12-31"
                    }
                ],
                "alternativeCredentials": [
                    {
                        "credentialId": "Test Alternative Credential",
                        "type": {
                            "id": "9e09373b-44d1-452d-a5ef-ff4e1866d9a0"
                        }
                    }
                ],
                "emergencyContacts": [
                    {
                        "name": {
                            "fullName": "Olivia Conrad",
                            "firstName": "Olivia",
                            "lastName": "Conrad"
                        },
                        "types": [
                            {
                                "id": "d8adfb93-4c49-4c0e-b378-3c739b9f7542"
                            }
                        ],
                        "relationship": {
                            "category": "Sister",
                            "detail": {
                                "id": "aab8965d-1003-4bbf-8337-47bf652679cf"
                            }
                        },
                        "phones": [
                            {
                                "number": "703-678-2211"
                            }
                        ],
                        "emails": [
                            {
                                "address": "olivia@example.com"
                            }
                        ],
                        "address": {
                            "addressLines": [
                                "12008 Olivia St."
                            ],
                            "countryCode": "USA",
                            "countryTitle": "United States of America",
                            "locality": "Vienna",
                            "postalCode": "22180",
                            "regionTitle": "Virginia",
                            "regionCode": "US-VA",
                            "subRegionCode": "FAX",
                            "subRegionTitle": "Fairfax"
                        },
                        "priority": None,
                        "notes": "Adding EC record",
                        "lastConfirmedDate": None,
                        "startOn": None,
                        "endOn": None,
                        "statusDate": None
                    }
                ]
            }
        }

        #self.ethosClient, self.loginSession

        def injectHeaderFN(headers):
            headers["Content-Type"] = "application/json"
            headers["accept"] = "application/json"

        result = self.ethosClient.sendPostRequest(
            url="/api/person-find-or-create-requests",
            params=params,
            data=data,
            loginSession=self.loginSession,
            injectHeadersFn=injectHeaderFN
        )
        if result.status_code != 200:
            print("Response:", result.status_code)
            print("Response test:", result.text)
            raise Exception("Exception returned")

        print("TODO", result.text)
