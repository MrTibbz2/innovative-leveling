# Lachlan McKenna 2025
# interface for changing tasks on the clue via bluetooth.py
import asyncio
from libs import bluetooth

class TaskInterface:
    def __init__(self):
        self.ble_manager = bluetooth.BLEManager()
        # Don't auto-connect during init to avoid event loop issues
        # Connection will be handled when methods are called
    
    async def add_task(self, name: str, description: str, due: str) -> dict | None:
        await self.ble_manager.send_json({
            "command": "add_task",
            "name": name,
            "description": description,
            "due": due
        })
        return await self.ble_manager.receive_json()
    
    async def delete_task(self, uid: str) -> dict | None:
        await self.ble_manager.send_json({
            "command": "delete_task",
            "uid": uid
        })
        return await self.ble_manager.receive_json()
    
    async def get_tasks(self) -> dict | None:
        await self.ble_manager.send_json({
            "command": "get_tasks"
        })
        return await self.ble_manager.receive_json()
    
    async def receive_response(self) -> dict | None:
        return await self.ble_manager.receive_json()
    
    async def disconnect(self):
        await self.ble_manager.disconnect()