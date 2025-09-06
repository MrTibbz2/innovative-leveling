# 2025 - PyWebView API Bridge
# Exposes TaskInterface to frontend JavaScript via PyWebView bridge
import asyncio
import sys
import os

class TaskAPI:
    def __init__(self):
        # Add backend to path and import BLEManager directly like working code
        backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
        sys.path.insert(0, backend_path)
        import libs.bluetooth
        self.bt = libs.bluetooth.BLEManager()
        self.loop = None
        self._connect_sync()
    
    def _connect_sync(self):
        """Connect using the same pattern as working code"""
        async def main():
            await self.bt.connect()
        
        # Create and store the event loop like working code
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(main())
    
    def get_tasks(self):
        """Get all tasks from Clue and convert to frontend format"""
        async def _get():
            print("Sending get_tasks command to Clue...")
            send_result = await self.bt.send_json({"command": "get_tasks"})
            print(f"Send result: {send_result}")
            
            # Wait for response with timeout
            for i in range(20):  # Wait up to 2 seconds
                result = await self.bt.receive_json()
                if result:
                    print(f"Received response from Clue: {result}")
                    return result
                if i % 5 == 0:  # Log every 0.5 seconds
                    print(f"Waiting for response... ({i/10:.1f}s)")
                await asyncio.sleep(0.1)
            print("Timeout waiting for response from Clue")
            return None
        
        try:
            print("=== Getting tasks from Clue ===")
            # Use the same event loop
            result = self.loop.run_until_complete(_get())
            if result and 'tasks' in result:
                print(f"Converting {len(result['tasks'])} tasks to frontend format")
                # Convert backend format to frontend format
                tasks = []
                for task in result['tasks']:
                    converted_task = {
                        'id': task['uid'],
                        'title': task['name'],
                        'description': task['description'],
                        'completed': task['status'] == 2,
                        'status': task['status']
                    }
                    tasks.append(converted_task)
                    print(f"Converted task: {converted_task}")
                print(f"Returning {len(tasks)} tasks to frontend")
                return tasks
            else:
                print(f"No tasks in response or invalid response: {result}")
            return []
        except Exception as e:
            print(f"Error getting tasks: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def add_task(self, name, description, due=""):
        """Add new task to Clue"""
        async def _add():
            return await self.bt.send_json({
                "command": "add_task",
                "name": name,
                "description": description,
                "due": due
            })
        
        try:
            # Use the same event loop
            result = self.loop.run_until_complete(_add())
            return result
        except Exception as e:
            print(f"Error adding task: {e}")
            return False
    
    def delete_task(self, task_id):
        """Delete task from Clue"""
        async def _delete():
            print(f"Sending delete command for task_id: {task_id}")
            return await self.bt.send_json({
                "command": "delete_task",
                "uid": str(task_id)
            })
        
        try:
            # Use the same event loop
            result = self.loop.run_until_complete(_delete())
            print(f"Delete command result: {result}")
            return result
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False