import json
import libs.bluetooth 
import asyncio
class Task:
    def __init__(self, name, uid, description, due):
        self.name = name
        self.uid = uid 
        self.description = description
        self.status = 0 #0 = todo, 1 = in progress, 2 = done
        self.due = due
    


    def start (self):
        self.status = 1

    def finish (self):
        self.status = 2

    def dict (self) -> dict:
        return {
            "name": self.name,
            "uid": self.uid,
            "description": self.description,
            "status": self.status,
            }
    
class taskManager:
    def __init__(self):
        self.tasks = []
        self.toDo = 0
        self.inProgress = 0
        self.Done = 0
        self.uidCounter = 0 
        self.taskDicts = []


    def add_task(self, name, description, due) -> Task:
        task = Task(name, self.uidCounter, description, due)
        self.tasks.append(task)
        self.uidCounter += 1 
        return task
    
    def list_tasks(self):
        return self.tasks
    
    def get_task(self, name):
        for task in self.tasks:
            if task.name == name: 
                return task
        return "Task not found"

    def taskStatus(self) -> tuple:
        for task in self.tasks:
            if task.status == 0:
                self.toDo += 1
            elif task.status == 1:
                self.inProgress += 1
            elif task.status == 2:
                self.Done += 1
            else:
                print(f"Task '{task.name}' has an unknown status.")
            return self.toDo, self.inProgress, self.Done
        

    def returnTasksAsDict(self):
        taskDictslist = []
        for task in self.tasks:
            taskDictslist.append(task.dict())
        return taskDictslist
    
    def loadTasksFromDict(self, dicts: list): # safe, as long as only called on program start
        print(f"Loading {len(dicts)} tasks from dict")
        for taskDict in dicts:
            print(f"Processing task: {taskDict}")
            task = Task(
                name = taskDict["name"],
                uid = taskDict["uid"],
                description = taskDict["description"],
                due = taskDict.get("due", None)
            )
            task.status = taskDict["status"]
            self.uidCounter = max(self.uidCounter, task.uid + 1)
            self.tasks.append(task)
            print(f"Added task: {task.name} with uid {task.uid}")
        print(f"Total tasks in memory: {len(self.tasks)}")

    
    
    def dumpTasksToSave(self):
        with open("tasks.json", "w") as f:
            json.dump(self.returnTasksAsDict(), f)
        print("shoved it into a json file so that we can delete it later")

    async def dumpTasksToClue(self, bt):
            
        await bt.send_json({"tasks": self.returnTasksAsDict()})



    def loadTasksFromSave(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                print(f"JSON data loaded: {data}")
                self.loadTasksFromDict(data)
            print("loaded tasks from save file")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading tasks: {e}")
            print("No save file found, starting fresh.")




    def deleteDuplicateTasks(self):
        try:
            with open("tasks.json", "r") as f
                dicts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No tasks file to deduplicate.")
            return
        
        uniqueTasks = []
        seen = set()
        deletedCopies = 0
        for taskDict in dicts: 
            if taskDict["uid"] not in seen:
                seen.add(taskDict["uid"])
                uniqueTasks.append(taskDict)
            else:
                deletedCopies += 1
        
        with open("tasks.json", "w") as f:
            json.dump(uniqueTasks, f)

        print("Deleted", deletedCopies, "duplicate tasks.")
          

taskManager = taskManager() 
taskManager.loadTasksFromSave()
print(f"loaded tasks: {taskManager.tasks}")
bt = libs.bluetooth.BLEManager() 
async def main():
    await bt.connect()
    await taskManager.dumpTasksToClue(bt)


for task in taskManager.list_tasks():
    task.start() 
taskManager.dumpTasksToSave()
taskManager.deleteDuplicateTasks()
asyncio.run(main())

