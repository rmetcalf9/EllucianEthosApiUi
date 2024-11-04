from .TestRunnerInstance import TestRunnerInstance

# runs the test
# once as a baseline
# next as concurrent requests

class TestRunner():
    ethosClient = None
    loginSession = None
    testdict = None

    baseline_instance = None
    concurrent_instances = None

    def __init__(self, ethosClient, loginSession, testdict):
        self.ethosClient = ethosClient
        self.loginSession = loginSession
        self.testdict = testdict

        self.baseline_instance = TestRunnerInstance(ethosClient, loginSession, testdict, runname="baseline")
        self.concurrent_instances = []
        for x in range(0, testdict["num_concurrent"]):
            # TODO Clone loginSession and ethosClient
            self.concurrent_instances.append(TestRunnerInstance(
                ethosClient,
                loginSession,
                testdict,
                runname="Run-" + str(x)
            ))

    def run_test(self):
        print("Running tests: ", self.testdict["name"])

        print("Running baseline")
        self.baseline_instance.run()

