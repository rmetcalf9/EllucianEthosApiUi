from .TestRunnerInstance import TestRunnerInstance, TestRunnerInstanceThread

# runs the test
# once as a baseline
# next as concurrent requests

class TestRunner():
    getNewEthosClientAndLoginSession = None
    testdict = None

    def __init__(self, getNewEthosClientAndLoginSession, testdict):
        self.getNewEthosClientAndLoginSession = getNewEthosClientAndLoginSession
        self.testdict = testdict

    def run_test(self):
        print("Running tests: ", self.testdict["name"])



        print("Running baseline")
        baseline_instance = TestRunnerInstance(self.getNewEthosClientAndLoginSession, self.testdict, runname="baseline")
        baseline_instance.run()

        print("Running concurrent")
        threads = []
        for x in range(0, self.testdict["num_concurrent"]):
            threads.append(TestRunnerInstanceThread(
                TestRunnerInstance(
                    self.getNewEthosClientAndLoginSession,
                    self.testdict,
                    runname="Run-" + str(x)
                )
            ))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        full_result = {}
        for resource in baseline_instance.getResults().keys():
            number_failed = 0
            number_passed = 0
            total_time = 0
            for thread in threads:
                if not thread.get().getResults()[resource]["succeded"]:
                    number_failed += 1
                else:
                    number_passed += 1
                    total_time += thread.get().getResults()[resource]["time"]

            average_time = None
            if number_passed>0:
                average_time = total_time / number_passed

            full_result[resource] = {
                "baseline": baseline_instance.getResults()[resource],
                "num_concurrent": self.testdict["num_concurrent"],
                "average_time": average_time,
                "number_failed": number_failed,
            }

        print("Result", full_result)

        print("Result CSV")
        print("api,baseline,num_concurrent_runs,average,num_fails")
        for resource in full_result.keys():
            print(resource, ",", end="")
            print(full_result[resource]["baseline"]["time"], ",", end="")
            print(full_result[resource]["num_concurrent"], ",", end="")
            print(full_result[resource]["average_time"], ",", end="")
            print(full_result[resource]["number_failed"], ",", end="")
            print("")

        # print("Baseline time:", baseline_instance.getRunname())
        # print("0 time:", threads[0].get().getRunname())
        # print("1 time:", threads[1].get().getRunname())


        # print("Baseline time:", self.baseline_instance.getResults()["crosswalk-rules"]["time"])
        # print("0 time:", self.concurrent_instances[0].getResults()["crosswalk-rules"]["time"])
        # print("1 time:", self.concurrent_instances[1].getResults()["crosswalk-rules"]["time"])
