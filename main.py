# !!! Task start_task might not be necessary
# !!! Task end_task might not be necessary
# !!! case 's' finish
# !!! try block in case 'r' might not be necessary


from datetime import datetime
import json


class Task:
    def __init__(self, name):  # constructor
        self.startTime = datetime.now()     # when task was registered
        self.runningTime = 0
        self.endTime = 0
        self.name = name
        self.isRunning = False

    def set_task(self, t):          # setter
        self.name = t

    def get_task(self, mode="ALL"):       # getter
        if mode == "ALL":
            return self.name, self.startTime
        elif mode == "ALL_WITHOUT_NAME":
            return self.startTime
        elif mode == "NAME":
            return self.name
        elif mode == "START_TIME":
            return self.startTime

    def start_task(self):   # ending task by user !!!
        self.isRunning = True

    def end_task(self):     # starting task by user !!!
        self.isRunning = False


with open("tasks.json", 'r') as file:   # JSON file containing our tasks
    taskDict = json.load(file)  # here we store all our tasks
while True:
    print("What do you want to do? Type '?' for help.")
    command = input()   # initial input from user
    match command:
        case '?':   # help menu
            print("? - help\n"
                  "n - new task\n"
                  "l - list tasks\n"
                  "r - remove task\n"
                  "s - start task\n"
                  "e - exit program\n")
        case 'n':   # add new task
            print("Type your task:")
            text = input()
            if len(text) > 0:           # task name length should be > 0
                if text not in taskDict.keys():     # check if task already exists in taskDict
                    task = Task(text)  # creating new instance of Task class
                    taskDict[task.get_task("NAME")] = task.get_task("ALL_WITHOUT_NAME")     # adding to list
                else:
                    print("Task with this name is already present in registered tasks.")
            else:
                print("Task cannot be empty.")
        case 'l':   # show all currently available tasks
            if len(taskDict) > 0:   # if there are any tasks
                print("Current tasks available:")
                for taskName, taskDesc in taskDict.items():  # !!! work on unfolding
                    print(taskName, taskDesc)     # print all info about the task: name and when task was registered
            else:
                print("There are no tasks registered.")
        case 'r':   # remove task
            if len(taskDict) > 0:   # if there are any tasks
                print("Pick task number you want to remove:")
                taskList = []   # here we will save task names to delete them via index, not names
                for index, taskName in enumerate(taskDict):     # print formatted list with indexes
                    print(index, taskName)
                    taskList.append(taskName)
                taskNumber = input()
                try:    # check for correct input from user !!!
                    taskNumber = int(taskNumber)
                except ValueError:  # if input is incorrect
                    print("Please input an integer.")
                if taskNumber in range(len(taskList)):      # if selected task is present in taskList
                    print("Task", taskList[taskNumber], "removed.")
                    del taskDict[taskList[taskNumber]]      # remove it
                else:
                    print("Please input a valid task index.")
            else:
                print("No tasks registered.")
        case 's':   # start task processing !!!
            print("WORK IN PROGRESS!")
        case 'e':
            with open("tasks.json", 'w') as file:
                json.dump(taskDict, file, indent=2)
            print("Goodbye.")
            break
        case _:
            print("Unrecognized command. Please try again.")
