class Average_time_calculator(object):
    list_of_execution_times = []
    times_sum = 0
    result = 0
    def __init__(self, list_of_execution_times):
        self.list_of_execution_times = list_of_execution_times
    def get_execution_times_average(self):
        length = len(self.list_of_execution_times)
        for t in self.list_of_execution_times:
            self.times_sum = self.times_sum + t
        self.result = self.times_sum / length
        return self.result
