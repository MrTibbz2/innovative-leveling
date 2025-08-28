import asyncio
import libs.bluetooth
import libs.tasks
import uuid

# BLE and task manager setup
ble = libs.bluetooth.BLEManager()
task_manager = libs.tasks.TaskManager()

# Internal helper functions
async def sync_to_clue():
    """Send all tasks to Clue device."""
    await ble.connect()
    await ble.send_json({"tasks": task_manager.sync_to_clue()})
    await ble.disconnect()

async def sync_from_clue():
    """Fetch all tasks from Clue device."""
    await ble.connect()
    await ble.send_json({"request": "tasks"})
    await asyncio.sleep(1)
    msg = await ble.receive_json()
    if msg and "tasks" in msg:
        task_manager.sync_from_clue(msg["tasks"])
    await ble.disconnect()

def print_tasks():
    """Print all tasks in a readable format."""
    for t in task_manager.get_tasks():
        print(f"{t.name} | Due: {t.due_date} | Completed: {t.completed} | UID: {t.uid}")

async def interactive_cli():
    """Interactive terminal menu for managing tasks and syncing with Clue."""
    while True:
        print("\n--- TASK MANAGER ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task completed")
        print("4. Remove completed tasks")
        print("5. Sync to Clue")
        print("6. Sync from Clue")
        print("7. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            print_tasks()
        elif choice == "2":
            name = input("Task name: ").strip()
            due_date = input("Due date (YYYY-MM-DD): ").strip()
            uid = str(uuid.uuid4())
            task_manager.add_task(name, due_date, uid)
            print("Task added.")
        elif choice == "3":
            uid = input("Enter UID of task to mark completed: ").strip()
            task_manager.complete_task(uid)
            print("Task marked completed.")
        elif choice == "4":
            task_manager.remove_completed()
            print("Completed tasks removed.")
        elif choice == "5":
            await sync_to_clue()
            print("Synced tasks to Clue.")
        elif choice == "6":
            await sync_from_clue()
            print("Synced tasks from Clue.")
        elif choice == "7":
            print("Exiting.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    asyncio.run(interactive_cli())
