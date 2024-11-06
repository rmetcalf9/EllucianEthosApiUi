from .Stopwatch import Stopwatch
from threading import Thread

class TestRunnerInstanceThread(Thread):
    testRunnerInstance = None
    def __init__(self, testRunnerInstance):
        super().__init__() # Must call __init__() in the Thread class
        self.testRunnerInstance = testRunnerInstance

    def run(self):
        self.testRunnerInstance.run()

    def get(self):
        return self.testRunnerInstance

class TestRunnerInstance():
    getNewEthosClientAndLoginSession = None
    ethosClient = None
    loginSession = None
    testdict = None
    runname = None

    results = None

    hasRun = None

    def __init__(self, getNewEthosClientAndLoginSession, testdict, runname):
        print('CREATE TEST RUNNER INSTANCWE', runname)
        self.getNewEthosClientAndLoginSession = getNewEthosClientAndLoginSession
        (self.ethosClient, self.loginSession) = getNewEthosClientAndLoginSession()
        self.testdict = testdict
        self.runname = runname
        self.hasRun = False
        self.results = {}

    def run(self):
        print("Start of instance", self.runname)

        def injectHeaderFN(headers):
            headers["Accept"] = "application/json"

        for resource in self.testdict["resources"]:
            stopwatch = Stopwatch()
            result = self.ethosClient.sendGetRequest(
                url="/api/" + resource,
                params={},
                loginSession=self.loginSession,
                injectHeadersFn=injectHeaderFN
            )
            succeded = True
            if result.status_code != 200:
                succeded = False
                #self.ethosClient.raiseResponseException(result)

            result_time = stopwatch.get_time_value_and_reset()
            self.results[resource] = {
                "runname": self.runname,
                "time": result_time,
                "succeded": succeded
            }
        self.hasRun = True

    def getResults(self):
        return self.results

    def getRunname(self):
        return self.runname
