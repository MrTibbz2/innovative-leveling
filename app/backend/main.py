import libs.bluetooth
import asyncio


ble = libs.bluetooth.BLEManager()  

async def main():
	await ble.connect()

	# Send a test JSON packet
	await ble.send_json({"hello": "from PC"})

	# Keep running to receive notifications
	while True:
		msg = await ble.receive_json()
		if msg:
			print("Received:", msg)
		await asyncio.sleep(0.1)

asyncio.run(main())