import hashlib
import json
import os

USER_DATA_FILE = "users.json"
TASK_DATA_FILE = "backend/tasks.json"

# Initialize user data files if they don't exist
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(TASK_DATA_FILE):
    with open(TASK_DATA_FILE, 'w') as f:
        json.dump({}, f)

# Function to hash passwords using SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
def register(username, password):
    with open(USER_DATA_FILE, 'r+') as f:
        users = json.load(f)
        if username in users:
            return "Username already exists"
        users[username] = hash_password(password)
        f.seek(0)
        json.dump(users, f)
        return "Registration successful"

# Log in an existing user
def login(username, password):
    with open(USER_DATA_FILE, 'r') as f:
        users = json.load(f)
        if username in users and users[username] == hash_password(password):
            return "Login successful"
        else:
            return "Invalid credentials"

# Delete a user
def delete_user(username):
    with open(USER_DATA_FILE, 'r+') as f:
        users = json.load(f)
        if username in users:
            del users[username]
            f.seek(0)
            json.dump(users, f)
            return f"User {username} deleted successfully"
        return "User not found"

# Reset all user data
def reset_all_data():
    with open(USER_DATA_FILE, 'w') as f:
        json.dump({}, f)
    with open(TASK_DATA_FILE, 'w') as f:
        json.dump({}, f)
    return "All user data has been reset"

# Save task for a user
def save_task(username, task, due_date, due_time):
    with open(TASK_DATA_FILE, 'r+') as f:
        tasks = json.load(f)
        if username not in tasks:
            tasks[username] = {'tasks': [], 'events': []}
        tasks[username]['tasks'].append({"task": task, "due_date": due_date, "due_time": due_time})
        f.seek(0)
        json.dump(tasks, f)

# Fetch tasks for a user
def get_tasks(username):
    with open(TASK_DATA_FILE, 'r') as f:
        tasks = json.load(f)
        return tasks.get(username, {}).get('tasks', [])

# Remove a task for a user
def remove_task(username, task_index):
    with open(TASK_DATA_FILE, 'r+') as f:
        tasks = json.load(f)
        if username in tasks and 0 <= task_index < len(tasks[username]['tasks']):
            tasks[username]['tasks'].pop(task_index)
            f.seek(0)
            json.dump(tasks, f)

# Save event for a user
def save_event(username, event, date):
    with open(TASK_DATA_FILE, 'r+') as f:
        tasks = json.load(f)
        if username not in tasks:
            tasks[username] = {'tasks': [], 'events': []}
        tasks[username]['events'].append({"event": event, "date": date})
        f.seek(0)
        json.dump(tasks, f)

# Fetch events for a user
def get_events(username):
    with open(TASK_DATA_FILE, 'r') as f:
        tasks = json.load(f)
        return tasks.get(username, {}).get('events', [])
