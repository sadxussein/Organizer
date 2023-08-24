import sys
import json
from PyQt5.QtWidgets import QApplication
from task import Task
from main_window import MainWindow


# Program main loop
# !!!
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

if __name__ == "__main__":
    # !!!
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

    # # 1. Parse JSON file into simple list of Task elements
    # with open("tasks.json", 'r') as file:   # JSON file containing our tasks
    #     dictToParse = json.load(file)       # store all our tasks which now need to be parsed into simple list
    # taskList = []                           # this one
    # for taskName, taskDesc in dictToParse.items():
    #     task = Task(taskName, *taskDesc)       # using second constructor
    #     taskList.append(task)                  # adding to list
    #
    # # 2. Endless loop for user to enter commands via match-case
    # while True:
    #     print("What do you want to do? Type '?' for help.")
    #     command = input()   # initial input from user
    #     match command:
    #         # 3. Help menu option
    #         case '?':   # help menu
    #             print("? - help\n"
    #                   "n - new task\n"
    #                   "l - list tasks\n"
    #                   "r - remove task\n"
    #                   "e - edit task\n"
    #                   "s - start task\n"
    #                   "f - finish task\n"
    #                   "q - quit program\n")
    #         # 4. Create new task option
    #         # !!! add description field
    #         case 'n':   # add new task
    #             print("Type your task:")
    #             text = input()
    #             if len(text) > 0:   # task name length should be > 0
    #                 if not any(task.name == text for task in taskList):     # check if task already exists in taskDict
    #                     task = Task(text)       # creating new instance of Task class
    #                     taskList.append(task)   # adding to list
    #                 else:
    #                     print("Task with this name is already present in registered tasks.")
    #             else:
    #                 print("Task name cannot be empty.")
    #         # 5. List all tasks verbose description
    #         case 'l':   # show all currently available tasks
    #             if len(taskList) > 0:   # if there are any tasks
    #                 print("Current tasks available:")
    #                 for task in taskList:
    #                     for key, value in task.get_task("USER").items():
    #                         print(f"{key}: {value}")  # info about the task: name, when task was registered etc
    #             else:
    #                 print("There are no tasks registered.")
    #         # 6. Remove single task
    #         # !!! rework so user could edit/remove/add multiple tasks
    #         case 'r':   # remove task
    #             if len(taskList) > 0:   # if there are any tasks
    #                 print("Select task number you want to remove:")
    #                 # print formatted list with indexes
    #                 print('\n'.join(f"{index+1}: {task.get_task('NAME')}" for index, task in enumerate(taskList)))
    #                 taskNumber = input()
    #                 try:    # check for correct input from user
    #                     taskNumber = int(taskNumber)
    #                 except ValueError:  # if input is incorrect
    #                     print("Please input an integer.")
    #                     continue    # if not valid integer we skip this iteration of the loop
    #                 if taskNumber - 1 in range(len(taskList)):      # if selected task is present in taskList
    #                     print("Task", taskList[taskNumber - 1].name, "removed.")
    #                     del taskList[taskNumber - 1]      # remove it
    #                 else:
    #                     print("Please input a valid task index.")
    #             else:
    #                 print("No tasks registered.")
    #         # 7. Edit single task
    #         case 'e':   # edit task
    #             if len(taskList) > 0:  # if there are any tasks
    #                 print("Select task number you want to edit:")
    #                 print('\n'.join(f"{index + 1}: {task.get_task('NAME')}" for index, task in enumerate(taskList)))
    #                 taskNumber = input()
    #                 try:  # check for correct input from user
    #                     taskNumber = int(taskNumber)
    #                 except ValueError:  # if input is incorrect
    #                     print("Please input an integer.")
    #                     continue  # if not valid integer we skip this iteration of the loop
    #                 if taskNumber - 1 in range(len(taskList)):  # if selected task is present in taskList
    #                     print("Please enter new name for selected task:")
    #                     text = input()
    #                     if len(text) > 0:  # task name length should be > 0
    #                         if not any(task.name == text for task in taskList):  # if task exists in taskDict
    #                             taskList[taskNumber - 1].set_task(text)
    #                         else:
    #                             print("Task with this name is already present in registered tasks.")
    #                     else:
    #                         print("Task name cannot be empty.")
    #                 else:
    #                     print("Please input a valid task index.")
    #             else:
    #                 print("No tasks registered.")
    #         # 8. Start tracking task
    #         case 's':
    #             # If there are any tasks and at least one of them is not running
    #             if len(taskList) > 0 and not all(task.get_task("RUNNING") for task in taskList):
    #                 print("Select task number you want to start:")
    #                 print('\n'.join(f"{index + 1}: {task.get_task('NAME')}" for index, task in enumerate(taskList)))
    #                 taskNumber = input()
    #                 try:  # check for correct input from user
    #                     taskNumber = int(taskNumber)
    #                 except ValueError:  # if input is incorrect
    #                     print("Please input an integer.")
    #                     continue  # if not valid integer we skip this iteration of the loop
    #                 if taskNumber - 1 in range(len(taskList)):  # if selected task is present in taskList
    #                     if taskList[taskNumber - 1].get_task("RUNNING"):
    #                         print("Task", taskList[taskNumber - 1].get_task("NAME"), "is already running.")
    #                     else:
    #                         print("Task", taskList[taskNumber - 1].get_task("NAME"), "started.")
    #                         taskList[taskNumber - 1].start_task()  # start task, wait for finish
    #                 else:
    #                     print("Please input a valid task index.")
    #             elif all(task.get_task("RUNNING") for task in taskList):
    #                 print("All tasks running.")
    #             elif len(taskList) == 0:
    #                 print("No tasks registered.")
    #         # 9. Finish tracking task
    #         case 'f':
    #             if len(taskList) > 0 and any(task.get_task("RUNNING") for task in taskList):  # if there are any tasks
    #                 print("Select task number you want to finish:")
    #                 print('\n'.join(f"{index + 1}: {task.get_task('NAME')}" for index, task in enumerate(taskList)))
    #                 taskNumber = input()
    #                 try:  # check for correct input from user
    #                     taskNumber = int(taskNumber)
    #                 except ValueError:  # if input is incorrect
    #                     print("Please input an integer.")
    #                     continue  # if not valid integer we skip this iteration of the loop
    #                 if taskNumber - 1 in range(len(taskList)):  # if selected task is present in taskList
    #                     if not taskList[taskNumber - 1].get_task("RUNNING"):
    #                         print("Task", taskList[taskNumber - 1].get_task("NAME"), "is already stopped.")
    #                     else:
    #                         print("Task", taskList[taskNumber - 1].get_task("NAME"), "stopped.")
    #                         taskList[taskNumber - 1].end_task()  # start task, wait for finish
    #                 else:
    #                     print("Please input a valid task index.")
    #             elif not any(task.get_task("RUNNING") for task in taskList):
    #                 print("No tasks running.")
    #             elif len(taskList) == 0:
    #                 print("No tasks registered.")
    #         # 10. Exit and save tasks
    #         case 'q':   # finishing program and printing result to JSON file
    #             with open("tasks.json", 'w') as file:   # open file
    #                 dumpDict = {}                       # the result dict
    #                 for task in taskList:               # pick every task we have
    #                     dumpDict.update(task.get_task("JSON"))  # placing them all in the result dict
    #                 json.dump(dumpDict, file, indent=4)         # finally, saving file, ending program
    #             print("Goodbye.")
    #             break
    #         case _:
    #             print("Unrecognized command. Please try again.")
