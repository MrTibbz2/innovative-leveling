import libs.bluetooth

import time
ble_manager = libs.bluetooth.BLEManager()

while True:
    # Auto reconnect handled internally
    ble_manager.send_json({"temperature": 23, "humidity": 50})

    incoming = ble_manager.receive_json()
    if incoming:
        
        print("Received:", incoming)

    time.sleep(2)