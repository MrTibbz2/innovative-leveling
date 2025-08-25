import time
import json
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

class BLEManager:
    def __init__(self):
        self.ble = BLERadio()
        self.uart_service = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart_service)
        self.connected = False
        self.receive_buffer = ""

    def _advertise_until_connected(self):
        """Start advertising until a central connects."""
        if not self.ble.connected:
            print("Advertising BLE...")
            self.ble.start_advertising(self.advertisement)
            while not self.ble.connected:
                time.sleep(0.5)
            self.ble.stop_advertising()
            self.connected = True
            print("Connected!")

    def _check_reconnect(self):
        """Automatically reconnect if disconnected."""
        if not self.ble.connected:
            if self.connected:
                print("Disconnected! Reconnecting...")
            self.connected = False
            self._advertise_until_connected()

    def send_json(self, data: dict) -> bool:
        """Send JSON data over BLE."""
        self._check_reconnect()
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
        self._check_reconnect()
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
