class Job:
    def __init__(self, name, end_time=None, parent_task=None):
        self.name = name
        self.end_time = end_time
        self.parent_task = parent_task

    def set_job_name(self, name):
        self.name = name

    def get_job_name(self):
        return self.name

    def set_job_end_time(self, end_time):
        self.end_time = end_time

    def get_job_end_time(self):
        return self.end_time

    def set_job_parent_task(self, parent_task):
        self.parent_task = parent_task

    def get_job_parent_task(self):
        return self.parent_task
