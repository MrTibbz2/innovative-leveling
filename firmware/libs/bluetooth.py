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
                # amazonq-ignore-next-line
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
                # amazonq-ignore-next-line
                raw = self.uart_service.read(self.uart_service.in_waiting).decode("utf-8")
                self.receive_buffer += raw

            # Try to parse complete JSON messages delimited by newline
            if "\n" in self.receive_buffer:
                line, self.receive_buffer = self.receive_buffer.split("\n", 1)
                if line.strip():
                    # amazonq-ignore-next-line
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
        for task in self.task_manager.tasks:
            if task.uid == tasks_uid:
                self.task_manager.tasks.remove(task)
                return
    def getTasks(self):
        result = self.ble_manager.send_json({"tasks": self.task_manager.tasks})
        if result:
            print("Tasks sent")
        else: 
            print("Fail send tasks")

    def check_commands(self): # chcecks the json buffer for incoming commands
        command = self.ble_manager.receive_json()
        if command:
            print("command recv")
            if command["command"] == self.ADD_TASK:
                self.addTask(command["name"], command["description"], command["due"])
            elif command["command"] == self.DELETE_TASK:
                self.deleteTask(command["uid"])
            elif command["command"] == self.GET_TASKS:
                self.getTasks()
            else:
                print("Unknown command")
                self.ble_manager.send_json({"error": "Unknown command"})
        else:
            pass


    
            
    