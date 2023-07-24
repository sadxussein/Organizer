from datetime import datetime


# Task class
# 1. All types of constructors
# 2. Setter
# !!! update Task setter, add more fields
# 3. Getter
# 4. Start task
# 5. End task

class Task:
    # 1. All types of constructors
    def __init__(self, name, register_time=None, is_running=None, start_time=None, end_time=None, time_ranges=None):
        # Constructor for Task which has been present for some time and has time ranges
        if register_time is not None and is_running is not None and start_time is not None\
                and end_time is not None and time_ranges is not None:
            self.registerTime = datetime.strptime(register_time, "%Y-%m-%d %H:%M:%S")
            self.name = name
            self.isRunning = is_running
            self.startTime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            self.endTime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            self.timeRanges = []
            for time_range in time_ranges:
                time = tuple(datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time in time_range)
                self.timeRanges.append(time)
        # Constructor for Task which is running but never ended once
        elif register_time is not None and is_running is not None and start_time is not None:
            self.registerTime = datetime.strptime(register_time, "%Y-%m-%d %H:%M:%S")
            self.name = name
            self.isRunning = is_running
            self.startTime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            self.endTime = None
            self.timeRanges = []
        # Constructor for Task which has never started
        elif register_time is not None and is_running is not None:  # constructor for importing task from json
            self.registerTime = datetime.strptime(register_time, "%Y-%m-%d %H:%M:%S")
            self.name = name
            self.isRunning = is_running
            self.startTime = None
            self.endTime = None
            self.timeRanges = []
        # Constructor for creating task from scratch
        else:
            self.registerTime = datetime.now()  # when task was registered
            self.name = name
            self.isRunning = False
            self.startTime = None
            self.endTime = None
            self.timeRanges = []

    # 2. Setter
    def set_task(self, name):   # setter !!!
        self.name = name

    # 3. Getter
    def get_task(self, mode):
        # Parse program data for JSON output in analogy with constructors
        if mode == "JSON":
            if any(self.timeRanges) and self.endTime is not None:
                time_ranges_json = []
                for timeRange in self.timeRanges:
                    time_ranges_json.append(tuple(time.strftime("%Y-%m-%d %H:%M:%S") for time in timeRange))
                return {
                    self.name: [
                        self.registerTime.strftime("%Y-%m-%d %H:%M:%S"),
                        self.isRunning,
                        self.startTime.strftime("%Y-%m-%d %H:%M:%S"),
                        self.endTime.strftime("%Y-%m-%d %H:%M:%S"),
                        time_ranges_json
                    ]
                }
            elif self.startTime is not None:
                return {
                    self.name: [
                        self.registerTime.strftime("%Y-%m-%d %H:%M:%S"),
                        self.isRunning,
                        self.startTime.strftime("%Y-%m-%d %H:%M:%S")
                    ]
                }
            else:
                return {
                    self.name: [
                        self.registerTime.strftime("%Y-%m-%d %H:%M:%S"),
                        self.isRunning
                    ]
                }
        # Print some info for user
        elif mode == "USER":
            return {
                "Task name": self.name,
                "Register time": self.registerTime.strftime("%Y-%m-%d %H:%M:%S"),
                "Currently running": self.isRunning
            }
        # Task name caller
        elif mode == "NAME":
            return self.name
        # Task status caller
        elif mode == "RUNNING":
            return self.isRunning

    # 4. Start task
    def start_task(self):
        self.startTime = datetime.now()
        self.isRunning = True

    # 5. End task
    def end_task(self):
        self.endTime = datetime.now()
        self.isRunning = False
        self.timeRanges.append((self.startTime, self.endTime))