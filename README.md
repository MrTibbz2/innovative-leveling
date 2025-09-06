# innovative-leveling
this is a project for APC2025 made by bryan, charlie and lachlan.

# project structure

keep it simple. 

- put all code for the CPX under /firmware
- put everything for the desktop app under /app.

# communication of the device to the app:

- probably all in bluetooth if possible
- send data in json, none of this data seperated by dots in floating strings garbage 
- 

structure for comms:

- clue stores all the data for tasks
- app simply takes that and displays it as well as giving a ui to interact, add delete tasks and add leveling. 