from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import EllucianCommonUtils
from CommonDefaults import CommonDefaults
import json

query_to_get_schema = """
query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
        directives {
          name
          description
          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
"""

class GraphQlMenu():
    ethosClient = None
    loginSession = None
    connection_name = None
    commonDefaults = None

    def __init__(self, ethosClient, loginSession, connection_name):
        self.ethosClient = ethosClient
        self.loginSession = loginSession
        self.connection_name = connection_name
        self.commonDefaults = CommonDefaults(connection_name)

    def run(self):
        operations = {
            "Get Schema": self.opt_get_schema,
            "Get person-holds6": self.opt_get_person_holds,
            "Get personHoldTypes6": self.opt_get_person_holds_types,
            "Get persons": self.opt_get_persons,
            "Get addresses": self.opt_get_addresses
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

    def _make_graphql_query(self, query, limitresponse=True, outputresult=True, second_try=False):
        def injectHeadersFn(headers):
            headers["Content-Type"] = "application/json"
        operationName = ""
        variables = {
        }

        params={}
        post_data={
          "query": query,
          "operationName": operationName,
          "variables": variables
        }

        response = self.ethosClient.sendPostRequest(
            url="/graphql",
            loginSession=self.loginSession,
            params=params,
            data=json.dumps(post_data),
            injectHeadersFn=injectHeadersFn
        )

        # check for 401 and retry
        if response.status_code == 200:
            responsejson = json.loads(response.text)
            if "errors" in responsejson:
                for current_error in responsejson["errors"]:
                    if "message" in current_error:
                        if current_error["message"] == "Authentication failed.":
                            if "extensions" in current_error:
                                if "code" in current_error["extensions"]:
                                    if current_error["extensions"]["code"] == "401":
                                        if not second_try:
                                            print("Got a GraphQL 401 - refreshing login then retrying")
                                            if not self.loginSession.refresh():
                                                raise Exception("Login session expired and could not refresh")
                                            return self._make_graphql_query(
                                                query=query,
                                                limitresponse=limitresponse,
                                                outputresult=outputresult,
                                                second_try=True
                                            )

        if outputresult:
            if response.status_code == 200:
                print("Got ok response")
                responsejson = json.loads(response.text)
                if "errors" in responsejson:
                    print("There were ", len(responsejson["errors"]), "errors")
                else:
                    print("No errors in response")
                print("Response data (First 2048 chars):")
                if limitresponse:
                    print(response.text[:1024])
                else:
                    print(response.text)

            if response.status_code != 200:
                print("Got ERROR response")
                print(response.status_code)

        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def opt_get_schema(self):
        limitresult = inquirer.confirm(
            message="Do you want to limit response printed?",
            default=True
        ).execute()
        result = self._make_graphql_query(query_to_get_schema, True, True)
        if result != None:
            filename = "graphql_schema.json"
            save = inquirer.confirm(
                message="Save to " + filename + "?",
                default=False
            ).execute()
            if save:
                with open(filename, 'w') as fp:
                    output_data = json.dumps(result, indent=4, sort_keys=True)
                    fp.write(output_data)

    def opt_get_person_holds(self):
        query = "{personHolds6(limit:10,sort:{id:ASC}) {totalCount}}"
        self._make_graphql_query(query)

    def opt_get_person_holds_types(self):
        # Add code and category fields to query
        query = "{personHoldTypes6(limit:10,sort:{id:ASC}) {totalCount edges {node {id category code}}}}"
        self._make_graphql_query(query)


    def opt_get_addresses(self):
        # Add code and category fields to query
        ## ,filter: {id: {EQ: "293c109c-7064-4b5b-8a00-b45019abfa31"}}
        query = """
        {
          addresses11(limit:10,sort:{id:ASC}) {
            totalCount
            edges {
              node {

                id,
                addressLines,
                place{
                  country{
                    code,
                    locality,
                    postalCode,
                    postalTitle,

                    region{
                        code,
                        title
                    },
                    title
                    }
                }

              }
            }
          }
        }
        """
        self._make_graphql_query(query)

    def opt_get_persons(self):
        query = "{persons12(limit:10,sort:{id:ASC}) {totalCount}}"



        query2= """
{
  persons12(
    limit:10,
    sort:{id:ASC},
    filter: {
        id: {EQ: "b79b33fc-c874-4324-b37a-b4287e4f1de7"}
    }
  ) {
    totalCount
    edges {
      node {
        id,
        gender,
        dateOfBirth,
        names {
          firstName,
          fullName,
          lastName,
          preference,
          title
        }
      }
    }
  }
}
"""
        self._make_graphql_query(query2)