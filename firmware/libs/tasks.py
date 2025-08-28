import time
import json

class Task:
    def __init__(self, name, due_date, completed=False, uid=None):
        self.name = name
        if not uid:
            raise ValueError("UID must be provided for Clue tasks")
        self.uid = uid
        self.due_date = due_date  # ISO format string
        self.completed = completed

    def to_dict(self):
        return {
            "name": self.name,
            "uid": self.uid,
            "due_date": self.due_date,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(
            name=data["name"],
            uid=data["uid"],
            due_date=data["due_date"],
            completed=data["completed"]
        )

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, name, due_date, uid):
        task = Task(name, due_date, uid=uid)
        self.tasks[task.uid] = task
        return task

    def update_task(self, task: Task):
        self.tasks[task.uid] = task

    def complete_task(self, uid):
        if uid in self.tasks:
            self.tasks[uid].completed = True

    def remove_completed(self):
        self.tasks = {uid: t for uid, t in self.tasks.items() if not t.completed}

    def sync_from_pc(self, pc_tasks):
        for t in pc_tasks:
            task = Task.from_dict(t)
            self.tasks[task.uid] = task

    def sync_to_pc(self):
        return [t.to_dict() for t in self.tasks.values()]

    def get_tasks(self):
        return list(self.tasks.values())

    def get_task(self, uid):
        return self.tasks.get(uid)

    def to_json(self):
        return json.dumps(self.sync_to_pc())

    def from_json(self, json_str):
        self.sync_from_pc(json.loads(json_str))
