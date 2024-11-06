import time

class Stopwatch():
    start_time = None

    def __init__(self):
        self.start_time = time.time()

    def get_time_value_and_reset(self):
        old_start_time = self.start_time
        self.start_time = time.time()
        return self.start_time - old_start_time
