# 2025 Lachlan McKenna 
# interface for bluetooth communication with the clue


import json
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from libs.ui import switch_bluetooth_status_indicator
from libs.taskManager import taskManager
class BLEManager:
    def __init__(self):
        self.ble = BLERadio()
        self.uart_service = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart_service)
        self.connected = False
        self.receive_buffer = ""
        self._advertising = False

    # amazonq-ignore-next-line
    def _start_advertising(self):
        """Start advertising if not already advertising."""
        if not self._advertising:
            print("Advertising BLE...")
            self.ble.start_advertising(self.advertisement)
            self._advertising = True

    def _stop_advertising(self):
        """Stop advertising if currently advertising."""
        if self._advertising:
            self.ble.stop_advertising()
            self._advertising = False

    def check_reconnect(self):
        """Non-blocking reconnect logic. Call this in your main loop."""
        reload_ui = False
        ble_is_connected = self.ble.connected
        if ble_is_connected:
            if not self.connected:
                print("Connected!")
                switch_bluetooth_status_indicator(True)
                reload_ui = True
                self.connected = True
            self._stop_advertising()
        else:
            if self.connected:
                switch_bluetooth_status_indicator(False)
                reload_ui = True
                print("Disconnected! Re-advertising...")
                self.connected = False
            self._start_advertising()
        return reload_ui

    def send_json(self, data: dict) -> bool:
        """Send JSON data over BLE."""
        self.check_reconnect()
        if not self.connected:
            print("Error: Not connected!")
            return False
        try:
            json_str = json.dumps(data) + "\n"  # newline as delimiter
            self.uart_service.write(json_str.encode("utf-8"))
            return True
        except Exception as e:
            print("Error sending JSON:", e)
            return False

    def receive_json(self):
        """Receive JSON data over BLE. Returns dict or None."""
        self.check_reconnect()
        if not self.connected:
            return None
        try:
            while self.uart_service.in_waiting:

                raw = self.uart_service.read(self.uart_service.in_waiting).decode("utf-8")
                self.receive_buffer += raw

            # Try to parse complete JSON messages delimited by newline
            if "\n" in self.receive_buffer:
                line, self.receive_buffer = self.receive_buffer.split("\n", 1)
                if line.strip():

                    return json.loads(line)
        except Exception as e:
            print("Error receiving JSON:", e)
        return None


class Commands:
    def __init__(self, task_manager: taskManager, ble_manager: BLEManager):
        self.ADD_TASK = "add_task"
        self.DELETE_TASK = "delete_task"
        self.GET_TASKS = "get_tasks"
        self.task_manager = task_manager
        self.ble_manager = ble_manager

    def addTask(self, name, description, due):
        
        self.task_manager.add_task(name, description, due)
        print(f"Task added")
    def deleteTask(self, tasks_uid):
        print(f"Attempting to delete task with uid: {tasks_uid} (type: {type(tasks_uid)})")
        # Convert string to int since UIDs are integers
        try:
            uid_int = int(tasks_uid)
        except ValueError:
            print(f"Invalid uid format: {tasks_uid}")
            return
            
        for task in self.task_manager.tasks:
            print(f"Checking task uid {task.uid} (type: {type(task.uid)}) against {uid_int}")
            if task.uid == uid_int:
                print(f"Found matching task, deleting: {task.name}")
                self.task_manager.tasks.remove(task)
                return
        print(f"No task found with uid: {uid_int}")
    def getTasks(self):
        tasks_dict = self.task_manager.returnTasksAsDict()
        print(f"Sending {len(tasks_dict)} tasks: {tasks_dict}")
        result = self.ble_manager.send_json({"tasks": tasks_dict})
        if result:
            print("Tasks sent successfully")
        else: 
            print("Failed to send tasks")

    def check_commands(self): # chcecks the json buffer for incoming commands
        command = self.ble_manager.receive_json()
        if command:
            print(f"Command received: {command}")
            cmd = command["command"]
            print(f"Command type: '{cmd}', ADD_TASK: '{self.ADD_TASK}', DELETE_TASK: '{self.DELETE_TASK}', GET_TASKS: '{self.GET_TASKS}'")
            
            if cmd == self.ADD_TASK:
                print("Matched ADD_TASK")
                self.addTask(command["name"], command["description"], command["due"])
            elif cmd == self.DELETE_TASK:
                print("Matched DELETE_TASK")
                self.deleteTask(command["uid"])
            elif cmd == self.GET_TASKS:
                print("Matched GET_TASKS")
                self.getTasks()
            else:
                print(f"No match for command: '{cmd}'")
                self.ble_manager.send_json({"error": "Unknown command"})
        # No else clause - don't spam logs when no command


    
            
    
        # No else clause - don't spam logs when no command


    
            
    