import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Scrollbar, Canvas
from backend import user_management
from datetime import datetime, timedelta

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List and Calendar App")
        self.username = None

        # Set the window to be resizable
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Initially create the login window
        self.login_window()

    def login_window(self):
        """Create the login or registration window."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="To-Do List and Calendar App", font=("Helvetica", 16)).pack(pady=20)

        # Username and password entry fields
        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # Login and register buttons
        login_button = tk.Button(self.root, text="Login", command=self.login_user)
        login_button.pack(pady=5)

        register_button = tk.Button(self.root, text="Register", command=self.register_user)
        register_button.pack(pady=5)

        # Add Dev button for admin functionality
        dev_button = tk.Button(self.root, text="Dev", command=self.dev_access)
        dev_button.pack(pady=5)

    def login_user(self):
        """Log in an existing user."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = user_management.login(username, password)
        if "successful" in result:
            self.username = username
            messagebox.showinfo("Login", result)
            self.create_tabs()  # Create tabs after successful login
        else:
            messagebox.showerror("Login Error", result)

    def register_user(self):
        """Register a new user."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = user_management.register(username, password)
        if "successful" in result:
            messagebox.showinfo("Registration", result)
        else:
            messagebox.showerror("Registration Error", result)

    def create_tabs(self):
        """Create tabs for task management and calendar, and remove the login screen."""
        # Clear all existing window content (including the login screen)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a notebook (tab system)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create a task manager tab
        self.task_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.task_tab, text='Task Manager')

        # Create a calendar tab
        self.calendar_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.calendar_tab, text='Calendar')

        # Initialize task and calendar windows
        self.task_manager_window()
        self.calendar_window()

    def task_manager_window(self):
        """Create the task manager window."""
        tk.Label(self.task_tab, text=f"Welcome, {self.username}!", font=("Helvetica", 16)).pack(pady=10)

        self.tasks_frame = tk.Frame(self.task_tab)
        self.tasks_frame.pack(pady=10)
        self.refresh_task_list()

        add_task_button = tk.Button(self.task_tab, text="Add Task", command=self.add_task)
        add_task_button.pack(pady=5)

    def refresh_task_list(self):
        """Refresh the list of tasks displayed."""
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        tasks = user_management.get_tasks(self.username)

        if tasks:
            for i, task in enumerate(tasks):
                task_label = tk.Label(self.tasks_frame, text=f"{i+1}. {task['task']} (Due: {task['due_date']} {task['due_time']})")
                task_label.grid(row=i, column=0, padx=10, pady=5)

                delete_button = tk.Button(self.tasks_frame, text="Delete", command=lambda i=i: self.delete_task(i))
                delete_button.grid(row=i, column=1)
        else:
            tk.Label(self.tasks_frame, text="No tasks yet!").pack()

    def add_task(self):
        """Prompt the user to add a new task and ask for a due date and time."""
        task = simpledialog.askstring("Add Task", "Enter your task:")
        if task:
            # Prompt for the due date
            due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
            due_time = simpledialog.askstring("Due Time", "Enter due time (HH:MM):")
            if due_date and due_time:
                user_management.save_task(self.username, task, due_date, due_time)
                self.refresh_task_list()
                self.refresh_calendar()  # Update the calendar after adding the task

    def delete_task(self, task_index):
        """Delete a specific task by index."""
        user_management.remove_task(self.username, task_index)
        self.refresh_task_list()
        self.refresh_calendar()  # Update the calendar after deleting the task

    def calendar_window(self):
        """Create the calendar window (monthly view)."""
        self.calendar_frame = tk.Frame(self.calendar_tab)
        self.calendar_frame.pack(expand=True, fill='both')
        self.refresh_calendar()

    def refresh_calendar(self):
        """Refresh the calendar, displaying tasks and events."""
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Current month and year
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month

        # Create a title with the month and year
        month_name = current_date.strftime('%B %Y')
        tk.Label(self.calendar_frame, text=month_name, font=("Helvetica", 16)).grid(row=0, column=0, columnspan=7)

        # Create the day labels (Sun to Sat)
        days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(days_of_week):
            tk.Label(self.calendar_frame, text=day, font=("Helvetica", 12), padx=10, pady=5).grid(row=1, column=i)

        # Get the first day of the month and the total number of days in the month
        first_day_of_month = datetime(year, month, 1)
        first_weekday = first_day_of_month.weekday()  # Monday is 0, Sunday is 6
        total_days_in_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        total_days = total_days_in_month.day

        # Adjust to Sunday as the first day of the week
        first_weekday = (first_weekday + 1) % 7

        # Configure calendar grid to resize proportionally
        for i in range(7):  # Columns for days of the week
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):  # Assume at most 6 rows (weeks) in a month
            self.calendar_frame.grid_rowconfigure(i + 2, weight=1)

        # Create the calendar grid with responsive day blocks
        day = 1
        row = 2
        col = first_weekday

        # Retrieve tasks and events
        tasks = user_management.get_tasks(self.username)
        events = user_management.get_events(self.username)

        # Create calendar blocks for each day
        while day <= total_days:
            day_cell = tk.Frame(self.calendar_frame, relief="solid", borderwidth=1)
            day_cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            # Label the day number
            day_label = tk.Label(day_cell, text=str(day), font=("Helvetica", 10, "bold"))
            day_label.pack(anchor="nw")

            # Add a scrollbar to handle multiple events/tasks
            canvas = Canvas(day_cell)
            scrollbar = Scrollbar(day_cell, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Check for tasks and events on this day
            day_str = f"{year}-{month:02d}-{day:02d}"

            # Display tasks on this day
            for task in tasks:
                if task['due_date'] == day_str:
                    tk.Label(scrollable_frame, text=f"{task['task']} @ {task['due_time']}", wraplength=130, anchor="w").pack(anchor="w", padx=5, pady=2)

            # Display events on this day
            for event in events:
                if event['date'] == day_str:
                    tk.Label(scrollable_frame, text=f"{event['event']}", wraplength=130, fg="blue", anchor="w").pack(anchor="w", padx=5, pady=2)

            # Move to the next day
            day += 1
            col += 1
            if col > 6:  # Move to the next row after Saturday
                col = 0
                row += 1

    def add_event_window(self):
        """Create a window to add events."""
        def add_event():
            event = event_entry.get()
            date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
            if event and date:
                user_management.save_event(self.username, event, date)
                messagebox.showinfo("Event Added", f"Event '{event}' added for {date}")
                self.refresh_calendar()
                add_event_win.destroy()

        # New window for adding an event
        add_event_win = tk.Toplevel(self.root)
        add_event_win.title("Add Event")

        tk.Label(add_event_win, text="Event:").pack(pady=5)
        event_entry = tk.Entry(add_event_win)
        event_entry.pack(pady=5)

        tk.Label(add_event_win, text="Date:").pack(pady=5)

        # Date dropdowns
        day_var = tk.StringVar(add_event_win)
        month_var = tk.StringVar(add_event_win)
        year_var = tk.StringVar(add_event_win)

        days = [str(i) for i in range(1, 32)]
        months = [str(i) for i in range(1, 13)]
        years = [str(i) for i in range(datetime.now().year, datetime.now().year + 10)]

        day_menu = tk.OptionMenu(add_event_win, day_var, *days)
        day_menu.pack(pady=5)
        month_menu = tk.OptionMenu(add_event_win, month_var, *months)
        month_menu.pack(pady=5)
        year_menu = tk.OptionMenu(add_event_win, year_var, *years)
        year_menu.pack(pady=5)

        add_button = tk.Button(add_event_win, text="Add Event", command=add_event)
        add_button.pack(pady=10)

    def dev_access(self):
        """Prompt for a password to access the dev features."""
        dev_password = simpledialog.askstring("Dev Access", "Enter the Dev Password", show='*')
        if dev_password == "Remmy34Martha23":
            self.admin_window()
        else:
            messagebox.showerror("Access Denied", "Incorrect Dev password")

    def admin_window(self):
        """Create a window for admin controls (reset and manage users)."""
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Admin Panel")

        # Reset all user data button
        reset_button = tk.Button(admin_win, text="Reset All Data", command=self.reset_data)
        reset_button.pack(pady=10)

        # Manage users button
        manage_users_button = tk.Button(admin_win, text="Manage Users", command=self.manage_users_window)
        manage_users_button.pack(pady=10)

    def reset_data(self):
        """Reset all user data."""
        result = user_management.reset_all_data()
        messagebox.showinfo("Reset", result)

    def manage_users_window(self):
        """Open a window to manage users."""
        manage_users_win = tk.Toplevel(self.root)
        manage_users_win.title("Manage Users")

        def delete_user():
            username = simpledialog.askstring("Delete User", "Enter the username to delete:")
            if username:
                result = user_management.delete_user(username)
                messagebox.showinfo("Manage Users", result)

        delete_user_button = tk.Button(manage_users_win, text="Delete User", command=delete_user)
        delete_user_button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
