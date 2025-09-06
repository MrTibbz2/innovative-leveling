/*leveling system*/
// 2025 Bryan Paul

// Main application class
class TaskProgressSystem {
    constructor() {
        this.tasks = []; // Stores tasks from Clue
        // Removed localStorage tracking - Clue is source of truth
        // Removed apiBaseUrl - using PyWebView bridge instead
        this.init();
    }

    // initialise the app
    init() {
        this.loadTasksFromBackend();  // Load directly from Clue, no localStorage needed
        this.updateProgressDisplay(); 
        this.updateProgressDiamond();  
        this.startFadeInAnimation();
        this.startPeriodicSync();     // Start periodic sync with Clue
        this.setupEventListeners();   // Setup UI event listeners
    }

    // No longer needed - all data comes from Clue
    // loadFromStorage removed since Clue is the source of truth

    // Load tasks from Clue via PyWebView API bridge
    async loadTasksFromBackend() {
        try {
            // Use PyWebView API bridge to get tasks from Clue
            // pywebview.api calls the Python TaskAPI methods
            const tasksData = await pywebview.api.get_tasks();
            this.tasks = tasksData || [];  // Tasks already in frontend format from API
            this.renderTasks();
        } catch (error) {
            console.error('Error loading tasks from Clue:', error);
            this.tasks = [];
            this.renderTasks();
        }
    }

    // No longer needed - API already returns tasks in frontend format
    // convertTask and applySavedCompletions removed since Clue is source of truth

    // No longer needed - Clue stores all data, no local storage required
    // saveToStorage removed since Clue is the source of truth

    // Fade in app container
    startFadeInAnimation() {
        const app = document.getElementById('appContainer');
        if (app) app.style.opacity = '1';
    }

    // Render tasks
    renderTasks() {
        const taskList = document.getElementById('taskList');
        if (!taskList) return;

        taskList.innerHTML = '';
        if (this.tasks.length === 0) {
            const noTasks = document.createElement('div');
            noTasks.className = 'no-tasks-message';
            noTasks.textContent = 'No tasks available.';
            taskList.appendChild(noTasks);
            return;
        }

        this.tasks.forEach(task => taskList.appendChild(this.createTaskElement(task)));
    }

    // Create HTML element for a task
    createTaskElement(task) {
        const isCompleted = task.completed || task.status === 2;
        const item = document.createElement('div');
        item.className = `task-item ${isCompleted ? 'completed' : ''}`;

        const content = document.createElement('div');
        content.className = 'task-content';
        const title = document.createElement('div');
        title.className = 'task-title';
        title.textContent = task.title;
        const desc = document.createElement('div');
        desc.className = 'task-description';
        desc.textContent = task.description;
        const status = document.createElement('div');
        status.className = 'task-status';
        status.textContent = this.getStatusText(task.status);

        content.append(title, desc, status);

        // Add delete button only
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-button';
        deleteBtn.textContent = '×';
        deleteBtn.addEventListener('click', async () => await this.deleteTask(task.id));
        
        item.append(content, deleteBtn);
        return item;
    }

    // Convert numeric status to text
    getStatusText(status) {
        switch (status) {
            case 0: return 'To Do';
            case 1: return 'In Progress';
            case 2: return 'Done';
            default: return 'Unknown';
        }
    }

    // Complete task method removed - tasks are completed on Clue device

    // Count completed tasks
    getCompletedTasksCount() {
        return this.tasks.filter(t => t.completed || t.status === 2).length;
    }

    // Update text showing progress
    updateProgressDisplay() {
        const progress = document.getElementById('progressText');
        if (progress) {
            progress.textContent = `${this.getCompletedTasksCount()} / ${this.tasks.length} tasks completed`;
        }
    }

    // Update the diamond progress
    updateProgressDiamond() {
        const diamond = document.getElementById('progressDiamond');
        if (!diamond) return;

        const percent = (this.getCompletedTasksCount() / this.tasks.length) * 100 || 0;
        const perimeter = 339.41; 
        const offset = perimeter - (percent / 100) * perimeter;

        diamond.style.strokeDasharray = perimeter;
        diamond.style.strokeDashoffset = offset;
        diamond.style.visibility = percent === 0 ? 'hidden' : 'visible';
    }

    // Check if all tasks are done
    checkAllTasksCompleted() {
        if (this.getCompletedTasksCount() === this.tasks.length && this.tasks.length > 0) {
            this.triggerCompletionAnimation();
        }
    }

    // animation when all tasks are done
    triggerCompletionAnimation() {
        const diamond = document.getElementById('diamond');
        if (!diamond) return;

        diamond.classList.add('completed');
        setTimeout(() => diamond.classList.remove('completed'), 800);
        this.updateProgressDisplay();
    }

    // Add periodic sync with Clue to get real-time updates
    startPeriodicSync() {
        // Sync with Clue every 5 seconds to get updates from device
        setInterval(async () => {
            await this.loadTasksFromBackend();
            this.updateProgressDisplay();
            this.updateProgressDiamond();
        }, 5000);
    }

    // Add new task to Clue
    async addTask(name, description, due = '') {
        try {
            const success = await pywebview.api.add_task(name, description, due);
            if (success) {
                await this.loadTasksFromBackend(); // Refresh to show new task
                this.updateProgressDisplay();
                this.updateProgressDiamond();
            }
            return success;
        } catch (error) {
            console.error('Error adding task:', error);
            return false;
        }
    }

    // Delete task from Clue
    async deleteTask(taskId) {
        try {
            const success = await pywebview.api.delete_task(taskId);
            if (success) {
                await this.loadTasksFromBackend(); // Refresh to remove deleted task
                this.updateProgressDisplay();
                this.updateProgressDiamond();
            }
            return success;
        } catch (error) {
            console.error('Error deleting task:', error);
            return false;
        }
    }
    
    // Setup event listeners for UI elements
    setupEventListeners() {
        const addBtn = document.getElementById('addTaskBtn');
        const nameInput = document.getElementById('taskName');
        const descInput = document.getElementById('taskDesc');
        const dueInput = document.getElementById('taskDue');
        
        // Add task button click
        addBtn.addEventListener('click', async () => {
            const name = nameInput.value.trim();
            const desc = descInput.value.trim();
            const due = dueInput.value;
            
            if (name) {
                const success = await this.addTask(name, desc, due);
                if (success) {
                    // Clear form on success
                    nameInput.value = '';
                    descInput.value = '';
                    dueInput.value = '';
                }
            }
        });
        
        // Enter key in name field submits form
        nameInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') addBtn.click();
        });
    }

    // Reset all progress - removed since Clue manages state
    // resetProgress removed - would need backend implementation
}

// initialise when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    window.taskProgressSystem = new TaskProgressSystem();
});

