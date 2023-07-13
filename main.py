from datetime import datetime
import json


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


# Program main loop
# 1. Parse JSON file into simple list of Task elements
# 2. Endless loop for user to enter commands via match-case
# 3. Help menu option
# 4. Create new task option
# !!! add description field
# 5. List all tasks verbose description
# 6. Remove single task
# !!! rework so user could edit/remove/add multiple tasks
# 7. Edit single task
# 8. Start tracking task
# 9. Finish tracking task
# 10. Exit and save tasks

# 1. Parse JSON file into simple list of Task elements
with open("tasks.json", 'r') as file:   # JSON file containing our tasks
    dictToParse = json.load(file)       # here we store all our tasks which now need to be parsed into simple list
taskList = []                           # this one
for taskName, taskDesc in dictToParse.items():
    task = Task(taskName, *taskDesc)       # using second constructor
    taskList.append(task)                  # adding to list

# 2. Endless loop for user to enter commands via match-case
while True:
    print("What do you want to do? Type '?' for help.")
    command = input()   # initial input from user
    match command:
        # 3. Help menu option
        case '?':   # help menu
            print("? - help\n"
                  "n - new task\n"                  
                  "l - list tasks\n"                  
                  "r - remove task\n"
                  "e - edit task\n"
                  "s - start task\n"
                  "f - finish task\n"
                  "q - quit program\n")
        # 4. Create new task option
        # !!! add description field
        case 'n':   # add new task
            print("Type your task:")
            text = input()
            if len(text) > 0:   # task name length should be > 0
                if not any(task.name == text for task in taskList):     # check if task already exists in taskDict
                    task = Task(text)       # creating new instance of Task class
                    taskList.append(task)   # adding to list
                else:
                    print("Task with this name is already present in registered tasks.")
            else:
                print("Task name cannot be empty.")
        # 5. List all tasks verbose description
        case 'l':   # show all currently available tasks
            if len(taskList) > 0:   # if there are any tasks
                print("Current tasks available:")
                for task in taskList:
                    for key, value in task.get_task("USER").items():
                        print(f"{key}: {value}")  # print all info about the task: name, when task was registered etc
            else:
                print("There are no tasks registered.")
        # 6. Remove single task
        # !!! rework so user could edit/remove/add multiple tasks
        case 'r':   # remove task
            if len(taskList) > 0:   # if there are any tasks
                print("Select task number you want to remove:")
                # print formatted list with indexes
                print('\n'.join(f"{index+1}: {task.get_task('NAME')}" for index, task in enumerate(taskList)))
                taskNumber = input()
                try:    # check for correct input from user
                    taskNumber = int(taskNumber)
                except ValueError:  # if input is incorrect
                    print("Please input an integer.")
                    continue    # if not valid integer we skip this iteration of the loop
                if taskNumber - 1 in range(len(taskList)):      # if selected task is present in taskList
                    print("Task", taskList[taskNumber - 1].name, "removed.")
                    del taskList[taskNumber - 1]      # remove it
                else:
                    print("Please input a valid task index.")
            else:
                print("No tasks registered.")
        # 7. Edit single task
        case 'e':   # edit task
            if len(taskList) > 0:  # if there are any tasks
                print("Select task number you want to edit:")
                print('\n'.join(f"{index + 1}: {task.get_task('NAME')}" for index, task in enumerate(taskList)))
                taskNumber = input()
                try:  # check for correct input from user
                    taskNumber = int(taskNumber)
                except ValueError:  # if input is incorrect
                    print("Please input an integer.")
                    continue  # if not valid integer we skip this iteration of the loop
                if taskNumber - 1 in range(len(taskList)):  # if selected task is present in taskList
                    print("Please enter new name for selected task:")
                    text = input()
                    if len(text) > 0:  # task name length should be > 0
                        if not any(task.name == text for task in taskList):  # check if task already exists in taskDict
                            taskList[taskNumber - 1].set_task(text)
                        else:
                            print("Task with this name is already present in registered tasks.")
                    else:
                        print("Task name cannot be empty.")
                else:
                    print("Please input a valid task index.")
            else:
                print("No tasks registered.")
        # 8. Start tracking task
        case 's':
            # If there are any tasks and at least one of them is not running
            if len(taskList) > 0 and not all(task.get_task("RUNNING") for task in taskList):
                print("Select task number you want to start:")
                print('\n'.join(f"{index + 1}: {task.get_task('NAME')}" for index, task in enumerate(taskList)))
                taskNumber = input()
                try:  # check for correct input from user
                    taskNumber = int(taskNumber)
                except ValueError:  # if input is incorrect
                    print("Please input an integer.")
                    continue  # if not valid integer we skip this iteration of the loop
                if taskNumber - 1 in range(len(taskList)):  # if selected task is present in taskList
                    if taskList[taskNumber - 1].get_task("RUNNING"):
                        print("Task", taskList[taskNumber - 1].get_task("NAME"), "is already running.")
                    else:
                        print("Task", taskList[taskNumber - 1].get_task("NAME"), "started.")
                        taskList[taskNumber - 1].start_task()  # start task, wait for finish
                else:
                    print("Please input a valid task index.")
            elif all(task.get_task("RUNNING") for task in taskList):
                print("All tasks running.")
            elif len(taskList) == 0:
                print("No tasks registered.")
        # 9. Finish tracking task
        case 'f':
            if len(taskList) > 0 and any(task.get_task("RUNNING") for task in taskList):  # if there are any tasks
                print("Select task number you want to finish:")
                print('\n'.join(f"{index + 1}: {task.get_task('NAME')}" for index, task in enumerate(taskList)))
                taskNumber = input()
                try:  # check for correct input from user
                    taskNumber = int(taskNumber)
                except ValueError:  # if input is incorrect
                    print("Please input an integer.")
                    continue  # if not valid integer we skip this iteration of the loop
                if taskNumber - 1 in range(len(taskList)):  # if selected task is present in taskList
                    if not taskList[taskNumber - 1].get_task("RUNNING"):
                        print("Task", taskList[taskNumber - 1].get_task("NAME"), "is already stopped.")
                    else:
                        print("Task", taskList[taskNumber - 1].get_task("NAME"), "stopped.")
                        taskList[taskNumber - 1].end_task()  # start task, wait for finish
                else:
                    print("Please input a valid task index.")
            elif not any(task.get_task("RUNNING") for task in taskList):
                print("No tasks running.")
            elif len(taskList) == 0:
                print("No tasks registered.")
        # 10. Exit and save tasks
        case 'q':   # finishing program and printing result to JSON file
            with open("tasks.json", 'w') as file:   # open file
                dumpDict = {}                       # the result dict
                for task in taskList:               # pick every task we have
                    dumpDict.update(task.get_task("JSON"))  # placing them all in the result dict
                json.dump(dumpDict, file, indent=4)         # finally, saving file, ending program
            print("Goodbye.")
            break
        case _:
            print("Unrecognized command. Please try again.")
