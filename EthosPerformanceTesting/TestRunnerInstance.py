


class TestRunnerInstance():
    getNewEthosClientAndLoginSession = None
    ethosClient = None
    loginSession = None
    testdict = None
    runname = None

    hasRun = None

    def __init__(self, getNewEthosClientAndLoginSession, testdict, runname):
        self.getNewEthosClientAndLoginSession = getNewEthosClientAndLoginSession
        (self.ethosClient, self.loginSession) = getNewEthosClientAndLoginSession()
        self.testdict = testdict
        self.runname = runname
        self.hasRun = False

    def run(self):
        print("Start of instance", self.runname)

        def injectHeaderFN(headers):
            headers["Accept"] = "application/json"

        for resource in self.testdict["resources"]:
            result = self.ethosClient.sendGetRequest(
                url="/api/" + resource,
                params={},
                loginSession=self.loginSession,
                injectHeadersFn=injectHeaderFN
            )
            if result.status_code != 200:
                self.ethosClient.raiseResponseException(result)

            print("DD", result)

            print("TODO RUN resource test", resource)