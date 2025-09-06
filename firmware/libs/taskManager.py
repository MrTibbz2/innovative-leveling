import json


# MAX_NVM = len(microcontroller.nvm)  # usually ~512 bytes

# def save_json_to_nvm(data):
#     """Save a dict/list as JSON in NVM."""
#     encoded = json.dumps(data).encode("utf-8")
#     if len(encoded) > MAX_NVM:
#         raise ValueError(f"Data too large for NVM ({len(encoded)} > {MAX_NVM})")
#     # Clear old data first
#     microcontroller.nvm[0:MAX_NVM] = b"\x00" * MAX_NVM
#     # Write new data
#     microcontroller.nvm[0:len(encoded)] = encoded

# def load_json_from_nvm():
#     """Load JSON from NVM. Returns None if empty or invalid."""
#     raw = bytes(microcontroller.nvm)
#     # Find the first null byte (end of stored data)
#     try:
#         end = raw.index(0)
#     except ValueError:
#         end = len(raw)
#     if end == 0:
#         return None  # nothing stored
#     try:
#         return json.loads(raw[:end].decode("utf-8"))
#     except Exception:
#         return None
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
    def list_tasks(self):
        return self.tasks
    
    def get_task(self, name):
        for task in self.tasks:
            if task.name == name: 
                return task
        return "Task not found"

    # def taskStatus(self) -> tuple: # returns (toDo, inProgress, Done)
    #     for task in self.tasks:
    #         if task.status == 0:
    #             self.toDo += 1
    #         elif task.status == 1:
    #             self.inProgress += 1
    #         elif task.status == 2:
    #             self.Done += 1
    #         else:
    #             print(f"Task '{task.name}' has an unknown status.")
    #         return self.toDo, self.inProgress, self.Done
        

    def returnTasksAsDict(self):
        taskDictslist = []
        for task in self.tasks:
            taskDictslist.append(task.dict())
        return taskDictslist
    
    def loadTasksFromDict(self, dicts: list): # safe, as long as only called on program start
        #print(f"Loading {len(dicts)} tasks from dict")
        for taskDict in dicts:
            #print(f"Proccesing: {taskDict}")
            task = Task(
                name = taskDict["name"],
                uid = taskDict["uid"],
                description = taskDict["description"],
                due = taskDict.get("due", None)
            )
            task.status = taskDict["status"]
            self.uidCounter = max(self.uidCounter, task.uid + 1)
            self.tasks.append(task)
            #print(f"Added: {task.name} of uid {task.uid}")
        print(f"Total tasks: {len(self.tasks)}")

    
    
    def dumpTasksToSave(self):
        with open("sd/tasks.json", "w") as f:
            json.dump(self.returnTasksAsDict(), f)
        print("saved tasks to file")




    def loadTasksFromSave(self):
        try:
            with open("sd/tasks.json", "r") as f:
                data = json.load(f)
                #print(f"JSON data loaded: {data}")
                self.loadTasksFromDict(data)
            print("loaded tasks save")
        except (OSError, ValueError) as e:
            print(f"Error loading tasks: {e}")
            print("No save, creating..")




    # def deleteDuplicateTasks(self):
    #     try:
    #         with open("sd/tasks.json", "r") as f:
    #             dicts = json.load(f)
    #     except (OSError, ValueError):
    #         print("No tasks file to deduplicate.")
    #         return
        
    #     uniqueTasks = []
    #     seen = set()
    #     deletedCopies = 0
    #     for taskDict in dicts: 
    #         if taskDict["uid"] not in seen:
    #             seen.add(taskDict["uid"])
    #             uniqueTasks.append(taskDict)
    #         else:
    #             deletedCopies += 1
        
    #     with open("sd/tasks.json", "w") as f:
    #         json.dump(uniqueTasks, f)

    #     print("Deleted", deletedCopies, "duplicate tasks.")
          