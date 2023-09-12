from datetime import datetime


class Job:
    def __init__(self, name, end_time=None, parent_task=None, register_date=None):
        self.__name = name
        self.__end_time = end_time
        self.__parent_task = parent_task
        if register_date is None:
            self.__register_date = datetime.now()
        else:
            self.__register_date = register_date

    def set_job_name(self, name):
        self.__name = name

    def get_job_name(self):
        return self.__name

    def set_job_end_time(self, end_time):
        self.__end_time = end_time

    def get_job_end_time(self):
        return self.__end_time

    def set_job_parent_task(self, parent_task):
        self.__parent_task = parent_task

    def get_job_parent_task(self):
        return self.__parent_task

    def set_register_date(self, register_date):
        self.__register_date = register_date

    def get_register_date(self):
        return self.__register_date

    def serialize(self):
        return {
            "name": self.__name,
            "endTime": self.__end_time,
            "parentTask": self.__parent_task,
            "registerDate": self.__register_date.strftime("%Y-%m-%d %H:%M:%S")
        }
