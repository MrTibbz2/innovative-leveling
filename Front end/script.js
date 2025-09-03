/*leveling system*/

class TaskProgressSystem {
    constructor() {
        this.tasks = []; // Stores tasks
        this.taskCompletions = {}; // Track completed tasks
        this.apiBaseUrl = 'http://localhost:3000/api'; // Backend API URL (not required for now)
        this.init();
    }

    // initialise the app
    init() {
        this.loadFromStorage();       
        this.loadTasksFromBackend();
        this.updateProgressDisplay(); 
        this.updateProgressDiamond();  
        this.startFadeInAnimation();   
    }

    // Load saved progress from localStorage
    loadFromStorage() {
        const savedData = localStorage.getItem('taskProgressData');
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                if (data.taskCompletions) this.taskCompletions = data.taskCompletions;
            } catch (error) {
                console.error('Error loading saved data:', error);
            }
        }
    }

    // Load tasks from local JSON or backend
    async loadTasksFromBackend() {
        try {
            const response = await fetch('/tasks.json');
            if (response.ok) {
                const tasksData = await response.json();
                this.tasks = tasksData.map(task => this.convertTask(task));
                this.applySavedCompletions();
                this.renderTasks();
            } else {
                this.tasks = [];
                this.renderTasks();
            }
        } catch (error) {
            this.tasks = [];
            this.renderTasks();
        }
    }

    // Convert backend JSON format to frontend format
    convertTask(task) {
        return {
            id: task.uid,
            title: task.name,
            description: task.description,
            completed: task.status === 2,
            status: task.status
        };
    }

    // Apply saved task completions
    applySavedCompletions() {
        this.tasks.forEach(task => {
            if (this.taskCompletions[task.id]) {
                task.completed = true;
                task.status = 2;
            }
        });
    }

    // Save progress
    saveToStorage() {
        const completions = {};
        this.tasks.forEach(task => {
            if (task.completed) completions[task.id] = true;
        });
        localStorage.setItem('taskProgressData', JSON.stringify({ taskCompletions: completions }));
    }

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

        const button = document.createElement('button');
        button.className = `task-button ${isCompleted ? 'completed' : 'complete'}`;
        button.textContent = isCompleted ? 'Completed' : 'Complete';
        button.disabled = isCompleted;

        if (!isCompleted) button.addEventListener('click', () => this.completeTask(task.id));

        item.append(content, button);
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

    // Mark task as complete
    completeTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task || task.completed) return;

        task.completed = true;
        task.status = 2;
        this.saveToStorage();

        this.renderTasks();
        this.updateProgressDisplay();
        this.updateProgressDiamond();
        this.checkAllTasksCompleted();
    }

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

    // Reset all progress
    resetProgress() {
        this.tasks.forEach(task => {
            task.completed = false;
            if (task.status === 2) task.status = 1;
        });
        this.saveToStorage();
        this.renderTasks();
        this.updateProgressDisplay();
        this.updateProgressDiamond();
    }
}

// initialise when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    window.taskProgressSystem = new TaskProgressSystem();
});

