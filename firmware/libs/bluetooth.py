import json
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from libs.ui import switch_bluetooth_status_indicator
class BLEManager:
    def __init__(self):
        self.ble = BLERadio()
        self.uart_service = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart_service)
        self.connected = False
        self.receive_buffer = ""
        self._advertising = False

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
