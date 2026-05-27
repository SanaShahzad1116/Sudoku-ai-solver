import time

class PerformanceTracker:
    def __init__(self):
        self.reset()

    def reset(self):
        self.states_explored = 0
        self.backtracks = 0
        self.start_time = None
        self.end_time = None

    def start(self):
        self.reset()
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def add_state(self):
        self.states_explored += 1

    def add_backtrack(self):
        self.backtracks += 1

    def get_time(self):
        if self.start_time and self.end_time:
            return round(self.end_time - self.start_time, 4)
        return 0

    def get_results(self, algorithm_name):
        return {
            'algorithm': algorithm_name,
            'time':      self.get_time(),
            'states':    self.states_explored,
            'backtracks': self.backtracks
        }