import libs.bluetooth
import asyncio


ble = libs.bluetooth.BLEManager()  # Change name if needed

async def main():
	await ble.connect()

	# Send a test JSON packet
	await ble.send_json({"hello": "from PC"})

	# Keep running to receive notifications
	await asyncio.sleep(5)

	await ble.disconnect()

asyncio.run(main())