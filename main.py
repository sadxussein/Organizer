# !!! Task start_task might not be necessary
# !!! Task end_task might not be necessary
# !!! case 's' finish
# !!! update Task setter, add more fields
# !!! check for name validity in edit option

# 1. Parse JSON file into simple list of Task elements
# 2. Endless loop for user to enter commands via match-case
# 3. Help menu option
# 4. Create new task option
# 5. List all tasks verbose description
# 6. Remove single task
# 7. Edit single task
# 8. Start tracking task
# 9. Exit and save tasks

from datetime import datetime
import json


class Task:
    def __init__(self, name, start_time=None, is_running=None):
        if start_time is None and is_running is None:   # constructor for creating task from scratch
            self.startTime = datetime.now()  # when task was registered
            self.name = name
            self.isRunning = False
        elif start_time is not None and is_running is not None:     # constructor for importing task from json
            self.startTime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            self.name = name
            self.isRunning = is_running

    def set_task(self, name):   # setter !!!
        self.name = name

    def get_task(self, mode):     # getter
        if mode == "JSON":
            return {
                self.name: [
                    self.startTime.strftime("%Y-%m-%d %H:%M:%S"),
                    self.isRunning
                ]
            }
        elif mode == "USER":
            return {
                "Task name": self.name,
                "Register time": self.startTime.strftime("%Y-%m-%d %H:%M:%S"),
                "Currently running": self.isRunning
            }
        elif mode == "NAME":
            return self.name

    def start_task(self):   # ending task by user !!!
        self.isRunning = True

    def end_task(self):     # starting task by user !!!
        self.isRunning = False


# 1. Parse JSON file into simple list of Task elements
with open("tasks.json", 'r') as file:   # JSON file containing our tasks
    dictToParse = json.load(file)       # here we store all our tasks which now need to be parsed into simple list
taskList = []                           # this one
for taskName, taskDesc in dictToParse.items():
    t = Task(taskName, *taskDesc)       # using second constructor
    taskList.append(t)                  # adding to list

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
                  "q - quit program\n")
        # 4. Create new task option
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
                print("Task cannot be empty.")
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
        case 'r':   # remove task
            if len(taskList) > 0:   # if there are any tasks
                print("Select task number you want to remove:")
                # print formatted list with indexes
                print('\n'.join(f"{index+1}: {task.name}" for index, task in enumerate(taskList)))
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
                print("Select task number you want to start:")
                print('\n'.join(f"{index + 1}: {task.name}" for index, task in enumerate(taskList)))
                taskNumber = input()
                try:  # check for correct input from user
                    taskNumber = int(taskNumber)
                except ValueError:  # if input is incorrect
                    print("Please input an integer.")
                    continue  # if not valid integer we skip this iteration of the loop
                if taskNumber - 1 in range(len(taskList)):  # if selected task is present in taskList
                    print("Please enter new name for selected task:")
                    taskList[taskNumber - 1].set_task(input())  # should check for name validity !!!
                else:
                    print("Please input a valid task index.")
            else:
                print("No tasks registered.")
        # 8. Start tracking task
        case 's':   # start task processing !!!
            print("WORK IN PROGRESS!")
        # 9. Exit and save tasks
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
