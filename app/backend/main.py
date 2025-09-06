import libs.bluetooth
import asyncio


ble = libs.bluetooth.BLEManager()  

async def main():
	await ble.connect()

	# Send a test JSON packet
	await ble.send_json({"command": "add_task", "name": "Test Task", "description": "This is a test", "due": "2024-12-31"})
	
	# Keep running to receive notifications
	while True:
		msg = await ble.receive_json()
		if msg:
			print("Received:", msg)
		await asyncio.sleep(0.1)

asyncio.run(main())