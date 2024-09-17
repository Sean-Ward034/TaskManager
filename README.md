
# To-Do List and Calendar App

This project is a Python-based To-Do List and Calendar application with a graphical user interface (GUI) built using Tkinter. Users can create accounts, log in, add tasks with due dates and times, and manage their tasks. Additionally, users can view their tasks and events in a responsive monthly calendar view, which dynamically resizes based on the screen size.

## Features

- **User Registration and Login**: Users can register and log in with a username and password.
- **Task Management**: Users can add, delete, and view tasks. Each task can have a due date and time.
- **Calendar View**: Tasks and events are displayed in a monthly calendar layout.
  - Calendar cells dynamically resize to fit the screen size.
  - Scrollbars are added to handle overflow if there are too many events or tasks on a single day.
- **Admin/Dev Access**: Special admin functionality allows resetting all user data and managing (adding or deleting) users.
- **Responsive Layout**: The calendar automatically adjusts to the window size.

## Installation

### Prerequisites

Make sure you have the following installed on your system:
- **Python 3.7+**: Download from [python.org](https://www.python.org/downloads/).
- **Tkinter**: Tkinter is usually bundled with Python. If not, install it via your package manager:

#### Windows

Tkinter should already be installed with Python on Windows. If it's not, try reinstalling Python with the Tkinter option enabled.

#### MacOS

Tkinter is usually installed with Python, but if missing, you can install it using Homebrew:

```bash
brew install python-tk
```

#### Linux

For Ubuntu/Debian:

```bash
sudo apt-get install python3-tk
```

### Cloning the Repository

To clone the repository, run the following command:

```bash
git clone https://github.com/your-username/my_todo_app.git
cd my_todo_app
```

### Running the App

1. Ensure you're in the project directory:
   ```bash
   cd my_todo_app
   ```

2. Run the app:
   ```bash
   python app.py
   ```

## Usage

Once the app is running, you'll be greeted with a login screen.

### Login and Registration

- **Login**: Enter your username and password if you already have an account.
- **Register**: If you don't have an account, click the "Register" button and enter your username and password.

### Task Management

- **Add Task**: After logging in, go to the "Task Manager" tab and click "Add Task". You'll be prompted to enter:
  - Task description
  - Due date (in the format `YYYY-MM-DD`)
  - Due time (in the format `HH:MM`)
  
  Your task will then be added to the list and displayed in the calendar.

- **Delete Task**: Click the "Delete" button next to any task to remove it.

### Calendar View

- Tasks and events are displayed in a calendar under the "Calendar" tab.
- Each task or event appears in its respective day. If there are too many tasks or events, a scrollbar will appear within the day cell.

### Admin/Dev Access

- To access the **Dev Panel**, click the "Dev" button on the login screen.
- You will be prompted to enter a password. The password is:

  ```
  Remmy34Martha23
  ```

  Once authenticated, the **Admin Panel** will open with the following options:
  
  - **Reset All Data**: This will delete all users, tasks, and events.
  - **Manage Users**: Allows the admin to manually delete or add users.
  - **It is highly reccomended that the dev password be changed for your own usage while this repo is still in development**

## File Structure

```bash
my_todo_app/
├── app.py              # Main Python script (GUI + Task/Calendar Management)
├── backend/
│   ├── user_management.py  # Handles user data, task/event management
│   └── tasks.json      # Stores tasks and events for each user
├── users.json          # Stores user credentials
└── README.md           # Documentation for the app
```

## Future Enhancements

Here are some ideas for future improvements:
- **Event Notifications**: Add notifications for upcoming tasks and events.
- **Task Priority**: Add a feature to set task priorities (e.g., High, Medium, Low).
- **Recurring Tasks/Events**: Allow users to schedule recurring tasks/events.
- **Color Coding**: Assign different colors to tasks and events based on type or priority.
- **Cloud Storage**: Allow syncing tasks and events across multiple devices.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, issues, or suggestions, please contact `tnvolfan034@gmail.com` or create an issue on the repository.
