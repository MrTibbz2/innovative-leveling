import asyncio
import json
from bleak import BleakClient, BleakScanner

# Nordic UART Service UUIDs
UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Notify (Clue → PC)
UART_TX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # Write  (PC → Clue)

class BLEManager:
    def __init__(self):
        self.client: BleakClient | None = None
        self._connected = False
        self._buffer = ""
        self._message_queue: asyncio.Queue = asyncio.Queue()

    @property
    def connected(self) -> bool:
        return self._connected and self.client and self.client.is_connected

    # ------------------- Internal Callbacks ------------------- #
    def _handle_disconnect(self, client):
        print("Device disconnected!")
        self._connected = False

    def _notification_handler(self, _, data: bytearray):
        """Handle incoming JSON from Clue."""
        try:
            text = data.decode("utf-8")
            self._buffer += text
            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    msg = json.loads(line)
                    self._message_queue.put_nowait(msg)
        except Exception as e:
            print("Error decoding message:", e)

    # ------------------- Public Methods ------------------- #
    async def connect(self):
        """Scan for CIRCUITPY devices and connect, auto-retry if disconnected."""
        while not self.connected:
            print("Scanning for CIRCUITPY BLE devices...")
            devices = await BleakScanner.discover()
            target = None
            for d in devices:
                if d.name and d.name.upper().startswith("CIRCUITPY"):
                    target = d
                    break

            if not target:
                print("No CIRCUITPY device found, retrying in 2s...")
                await asyncio.sleep(2)
                continue

            print(f"Connecting to {target.name} ({target.address})...")
            try:
                self.client = BleakClient(target.address, disconnected_callback=self._handle_disconnect)
                await self.client.connect()
                self._connected = True
                print("Connected!")

                # Subscribe to notifications from Clue
                await self.client.start_notify(UART_RX_CHAR_UUID, self._notification_handler)
            except Exception as e:
                print("Connection failed:", e)
                await asyncio.sleep(2)

    async def _ensure_connection(self):
        """Reconnect if disconnected."""
        if not self.connected:
            await self.connect()

    async def send_json(self, data: dict) -> bool:
        """Send JSON to Clue."""
        await self._ensure_connection()
        if not self.connected:
            print("Cannot send, not connected.")
            return False
        try:
            json_str = json.dumps(data) + "\n"
            await self.client.write_gatt_char(UART_TX_CHAR_UUID, json_str.encode("utf-8"))
            print("shat jason into the clue it should work")
            return True
        except Exception as e:
            print("Error sending JSON:", e)
            return False

    async def receive_json(self) -> dict | None:
        """Get next received JSON message, or None if none available."""
        await self._ensure_connection()
        if not self.connected:
            return None
        try:
            return self._message_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def disconnect(self):
        """Disconnect cleanly."""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
        self._connected = False
        print("Disconnected.")
