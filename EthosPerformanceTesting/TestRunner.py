from .TestRunnerInstance import TestRunnerInstance

# runs the test
# once as a baseline
# next as concurrent requests

class TestRunner():
    getNewEthosClientAndLoginSession = None
    testdict = None

    baseline_instance = None
    concurrent_instances = None

    def __init__(self, getNewEthosClientAndLoginSession, testdict):
        self.getNewEthosClientAndLoginSession = getNewEthosClientAndLoginSession
        self.testdict = testdict

        self.baseline_instance = TestRunnerInstance(getNewEthosClientAndLoginSession, testdict, runname="baseline")
        self.concurrent_instances = []
        for x in range(0, testdict["num_concurrent"]):
            self.concurrent_instances.append(TestRunnerInstance(
                getNewEthosClientAndLoginSession,
                testdict,
                runname="Run-" + str(x)
            ))

    def run_test(self):
        print("Running tests: ", self.testdict["name"])

        print("Running baseline")
        self.baseline_instance.run()

