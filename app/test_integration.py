# Simple test script to verify the integration works
# Run this to add some test tasks to the Clue for testing the frontend
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Front end'))

from Frontend.api import TaskAPI
import asyncio

async def test_integration():
    api = TaskAPI()
    
    print("Testing API integration...")
    
    # Test adding tasks
    print("Adding test tasks...")
    success1 = api.add_task("Complete project", "Finish the innovative leveling system", "2025-02-01")
    success2 = api.add_task("Test Bluetooth", "Verify BLE communication works", "2025-01-25")
    
    print(f"Task 1 added: {success1}")
    print(f"Task 2 added: {success2}")
    
    # Test getting tasks
    print("\nGetting tasks from Clue...")
    tasks = api.get_tasks()
    print(f"Retrieved {len(tasks)} tasks:")
    for task in tasks:
        print(f"  - {task['title']}: {task['description']} (Status: {task['status']})")
    
    print("\nIntegration test complete!")

if __name__ == "__main__":
    asyncio.run(test_integration())