import tkinter as tk
from tkinter import ttk, simpledialog
from tkcalendar import DateEntry
from plyer import notification
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Todo List")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        self.tasks = []
        self.completed_tasks = []
        self.categories = ["Work", "Personal", "Shopping"]
        self.edit_task_index = None

        self.azd_label = None

        self.main_menu()

    def main_menu(self):
        self.clear_frame()
        title = tk.Label(self.root, text="Todo List Main Menu", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=20)

        task_button = tk.Button(self.root, text="Add New Task", command=self.add_task_screen, bg="#4caf50", fg="white", width=25, height=2, font=("Helvetica", 14))
        task_button.pack(pady=10)

        task_list_button = tk.Button(self.root, text="View Task List", command=self.task_list_screen, bg="#2196f3", fg="white", width=25, height=2, font=("Helvetica", 14))
        task_list_button.pack(pady=10)

        completed_tasks_button = tk.Button(self.root, text="Completed Tasks", command=self.completed_tasks_screen, bg="#ff9800", fg="white", width=25, height=2, font=("Helvetica", 14))
        completed_tasks_button.pack(pady=10)

        category_button = tk.Button(self.root, text="Manage Categories", command=self.manage_categories_screen, bg="#9c27b0", fg="white", width=25, height=2, font=("Helvetica", 14))
        category_button.pack(pady=10)

        self.check_reminders()
        self.add_azd_label()

    def add_task_screen(self):
        self.clear_frame()

        title = tk.Label(self.root, text="Add New Task", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        task_label = tk.Label(self.root, text="Task Description:", bg="#f0f0f0", font=("Helvetica", 14))
        task_label.pack(pady=5)
        self.task_entry = tk.Entry(self.root, width=40, font=("Helvetica", 14))
        self.task_entry.pack(pady=5)

        date_frame = tk.Frame(self.root, bg="#f0f0f0")
        date_frame.pack(pady=10)

        start_date_label = tk.Label(date_frame, text="Start Date:", bg="#f0f0f0", font=("Helvetica", 14))
        start_date_label.grid(row=0, column=0, padx=10)
        self.start_date_entry = DateEntry(date_frame, width=12, background="darkblue", foreground="white", borderwidth=2, font=("Helvetica", 14))
        self.start_date_entry.grid(row=0, column=1, padx=10)

        self.end_date_var = tk.IntVar()
        end_date_check = tk.Checkbutton(date_frame, text="Has End Date?", variable=self.end_date_var, command=self.toggle_end_date, font=("Helvetica", 14), bg="#f0f0f0")
        end_date_check.grid(row=1, column=0, padx=10, pady=10)

        self.due_date_label = tk.Label(date_frame, text="End Date:", bg="#f0f0f0", font=("Helvetica", 14))
        self.due_date_entry = DateEntry(date_frame, width=12, background="darkblue", foreground="white", borderwidth=2, font=("Helvetica", 14))
        self.due_date_label.grid(row=2, column=0, padx=10, pady=10)
        self.due_date_entry.grid(row=2, column=1, padx=10)
        self.due_date_label.grid_remove()
        self.due_date_entry.grid_remove()

        category_reminder_frame = tk.Frame(self.root, bg="#f0f0f0")
        category_reminder_frame.pack(pady=10)

        category_label = tk.Label(category_reminder_frame, text="Select Category:", bg="#f0f0f0", font=("Helvetica", 14))
        category_label.grid(row=0, column=0, padx=10)
        self.category_var = tk.StringVar()
        self.category_var.set("Select")
        category_menu = ttk.OptionMenu(category_reminder_frame, self.category_var, "Select", *self.categories)
        category_menu.grid(row=0, column=1, padx=10)

        reminder_label = tk.Label(category_reminder_frame, text="Reminder Options:", bg="#f0f0f0", font=("Helvetica", 14))
        reminder_label.grid(row=0, column=2, padx=10)
        self.reminder_option = tk.StringVar()
        self.reminder_option.set("Select")
        options = ["One-time", "X Day of Every Month", "Every Week", "Specific Day Range"]
        reminder_menu = ttk.OptionMenu(category_reminder_frame, self.reminder_option, "Select", *options)
        reminder_menu.grid(row=0, column=3, padx=10)

        add_button = tk.Button(self.root, text="Add Task", command=self.add_task, bg="#4caf50", fg="white", font=("Helvetica", 14, "bold"))
        add_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, bg="#f44336", fg="white", font=("Helvetica", 14, "bold"))
        back_button.pack(pady=10)

        self.add_azd_label()

    def toggle_end_date(self):
        if self.end_date_var.get():
            self.due_date_label.grid()
            self.due_date_entry.grid()
        else:
            self.due_date_label.grid_remove()
            self.due_date_entry.grid_remove()

    def task_list_screen(self):
        self.clear_frame()

        title = tk.Label(self.root, text="Task List", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        self.task_listbox = tk.Listbox(self.root, width=50, height=10, font=("Helvetica", 14))
        self.task_listbox.pack(pady=10)

        self.update_task_listbox()

        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(pady=10)

        complete_button = tk.Button(control_frame, text="Complete", command=self.mark_complete, bg="#2196f3", fg="white", width=15, height=1, font=("Helvetica", 12))
        complete_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(control_frame, text="Delete", command=self.delete_task, bg="#f44336", fg="white", width=15, height=1, font=("Helvetica", 12))
        delete_button.grid(row=0, column=1, padx=5)

        edit_button = tk.Button(control_frame, text="Edit", command=self.edit_task_form, bg="#ff9800", fg="white", width=15, height=1, font=("Helvetica", 12))
        edit_button.grid(row=0, column=2, padx=5)

        back_button = tk.Button(self.root, text="Main Menu", command=self.main_menu, bg="#f44336", fg="white", font=("Helvetica", 12, "bold"))
        back_button.pack(pady=10)

        self.add_azd_label()

    def edit_task_form(self):
        try:
            selected_task = self.task_listbox.get(self.task_listbox.curselection()[0])
            task = next(task for task in self.tasks if task['task'] == selected_task)
            self.edit_task_index = self.tasks.index(task)

            self.clear_frame()

            title = tk.Label(self.root, text="Edit Task", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
            title.pack(pady=10)

            task_label = tk.Label(self.root, text="Task Description:", bg="#f0f0f0", font=("Helvetica", 14))
            task_label.pack(pady=5)
            self.edit_task_entry = tk.Entry(self.root, width=40, font=("Helvetica", 14))
            self.edit_task_entry.pack(pady=5)
            self.edit_task_entry.insert(0, task['task'].split(" (")[0])

            date_frame = tk.Frame(self.root, bg="#f0f0f0")
            date_frame.pack(pady=10)

            start_date_label = tk.Label(date_frame, text="Start Date:", bg="#f0f0f0", font=("Helvetica", 14))
            start_date_label.grid(row=0, column=0, padx=10)
            self.edit_start_date_entry = DateEntry(date_frame, width=12, background="darkblue", foreground="white", borderwidth=2, font=("Helvetica", 14))
            self.edit_start_date_entry.grid(row=0, column=1, padx=10)
            self.edit_start_date_entry.set_date(task['start_date'])

            self.edit_end_date_var = tk.IntVar()
            end_date_check = tk.Checkbutton(date_frame, text="Has End Date?", variable=self.edit_end_date_var, command=self.toggle_edit_end_date, font=("Helvetica", 14), bg="#f0f0f0")
            end_date_check.grid(row=1, column=0, padx=10, pady=10)

            self.edit_due_date_label = tk.Label(date_frame, text="End Date:", bg="#f0f0f0", font=("Helvetica", 14))
            self.edit_due_date_entry = DateEntry(date_frame, width=12, background="darkblue", foreground="white", borderwidth=2, font=("Helvetica", 14))
            self.edit_due_date_label.grid(row=2, column=0, padx=10, pady=10)
            self.edit_due_date_entry.grid(row=2, column=1, padx=10)

            if task['end_date']:
                self.edit_end_date_var.set(1)
                self.edit_due_date_entry.set_date(task['end_date'])
            else:
                self.edit_due_date_label.grid_remove()
                self.edit_due_date_entry.grid_remove()

            category_reminder_frame = tk.Frame(self.root, bg="#f0f0f0")
            category_reminder_frame.pack(pady=10)

            category_label = tk.Label(category_reminder_frame, text="Select Category:", bg="#f0f0f0", font=("Helvetica", 14))
            category_label.grid(row=0, column=0, padx=10)
            self.edit_category_var = tk.StringVar()
            self.edit_category_var.set(task['task'].split("Category: ")[1].split(",")[0])
            category_menu = ttk.OptionMenu(category_reminder_frame, self.edit_category_var, *self.categories)
            category_menu.grid(row=0, column=1, padx=10)

            reminder_label = tk.Label(category_reminder_frame, text="Reminder Options:", bg="#f0f0f0", font=("Helvetica", 14))
            reminder_label.grid(row=0, column=2, padx=10)
            self.edit_reminder_option = tk.StringVar()
            self.edit_reminder_option.set(task['reminder_type'])
            reminder_menu = ttk.OptionMenu(category_reminder_frame, self.edit_reminder_option, *["One-time", "X Day of Every Month", "Every Week", "Specific Day Range"])
            reminder_menu.grid(row=0, column=3, padx=10)

            button_frame = tk.Frame(self.root, bg="#f0f0f0")
            button_frame.pack(pady=10)

            save_button = tk.Button(button_frame, text="✔", command=self.save_task_edit, bg="#4caf50", fg="white", width=5, height=2, font=("Helvetica", 14, "bold"))
            save_button.grid(row=0, column=0, padx=10)

            cancel_button = tk.Button(button_frame, text="✘", command=self.task_list_screen, bg="#f44336", fg="white", width=5, height=2, font=("Helvetica", 14, "bold"))
            cancel_button.grid(row=0, column=1, padx=10)

            self.add_azd_label()

        except IndexError:
            self.set_message("Please select a task to edit", "red")

    def toggle_edit_end_date(self):
        if self.edit_end_date_var.get():
            self.edit_due_date_label.grid()
            self.edit_due_date_entry.grid()
        else:
            self.edit_due_date_label.grid_remove()
            self.edit_due_date_entry.grid_remove()

    def save_task_edit(self):
        edited_task = {
            "task": f"{self.edit_task_entry.get()} (Start: {self.edit_start_date_entry.get()}, Category: {self.edit_category_var.get()}, Reminder: {self.edit_reminder_option.get()})",
            "start_date": self.edit_start_date_entry.get(),
            "end_date": self.edit_due_date_entry.get() if self.edit_end_date_var.get() else None,
            "reminder_type": self.edit_reminder_option.get()
        }
        self.tasks[self.edit_task_index] = edited_task
        self.task_list_screen()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task['task'])

    def mark_complete(self):
        try:
            selected_task = self.task_listbox.get(self.task_listbox.curselection()[0])
            task = next(task for task in self.tasks if task['task'] == selected_task)
            self.tasks.remove(task)
            self.completed_tasks.append(selected_task)
            self.update_task_listbox()
            self.set_message(f"Task '{selected_task}' completed", "green")
        except IndexError:
            self.set_message("Please select a task to complete", "red")

    def delete_task(self):
        try:
            selected_task = self.task_listbox.get(self.task_listbox.curselection()[0])
            task = next(task for task in self.tasks if task['task'] == selected_task)
            self.tasks.remove(task)
            self.update_task_listbox()
            self.set_message(f"Task '{selected_task}' deleted", "green")
        except IndexError:
            self.set_message("Please select a task to delete", "red")

    def completed_tasks_screen(self):
        self.clear_frame()

        title = tk.Label(self.root, text="Completed Tasks", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        self.completed_task_listbox = tk.Listbox(self.root, width=50, height=10, font=("Helvetica", 14))
        self.completed_task_listbox.pack(pady=10)

        self.completed_task_listbox.delete(0, tk.END)
        for task in self.completed_tasks:
            self.completed_task_listbox.insert(tk.END, task)

        back_button = tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, bg="#f44336", fg="white", font=("Helvetica", 14, "bold"))
        back_button.pack(pady=10)

        self.add_azd_label()

    def manage_categories_screen(self):
        self.clear_frame()

        title = tk.Label(self.root, text="Manage Categories", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        self.category_listbox = tk.Listbox(self.root, width=30, height=10, font=("Helvetica", 14))
        self.category_listbox.pack(pady=10)

        self.category_listbox.delete(0, tk.END)
        for category in self.categories:
            self.category_listbox.insert(tk.END, category)

        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        add_category_button = tk.Button(button_frame, text="Add", command=self.add_category, bg="#4caf50", fg="white", width=10, height=1, font=("Helvetica", 12, "bold"))
        add_category_button.grid(row=0, column=0, padx=5)

        delete_category_button = tk.Button(button_frame, text="Delete", command=self.delete_category, bg="#f44336", fg="white", width=10, height=1, font=("Helvetica", 12, "bold"))
        delete_category_button.grid(row=0, column=1, padx=5)

        back_button = tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, bg="#f44336", fg="white", font=("Helvetica", 14, "bold"))
        back_button.pack(pady=10)

        self.add_azd_label()

    def add_category(self):
        new_category = simpledialog.askstring("Add Category", "New category name:")
        if new_category and new_category.strip() != "":
            self.categories.append(new_category.strip())
            self.manage_categories_screen()
        else:
            self.set_message("Please enter a valid category", "red")

    def delete_category(self):
        try:
            selected_category = self.category_listbox.get(self.category_listbox.curselection()[0])
            if selected_category in self.categories:
                self.categories.remove(selected_category)
                self.manage_categories_screen()
        except IndexError:
            self.set_message("Please select a category to delete", "red")

    def add_task(self):
        task = self.task_entry.get().strip()
        start_date = self.start_date_entry.get()
        category = self.category_var.get()
        reminder_type = self.reminder_option.get()

        if self.end_date_var.get():
            end_date = self.due_date_entry.get()
            task_details = f"{task} (Start: {start_date}, End: {end_date}, Category: {category}, Reminder: {reminder_type})"
        else:
            task_details = f"{task} (Start: {start_date}, Category: {category}, Reminder: {reminder_type})"

        if task != "":
            self.tasks.append({
                "task": task_details,
                "start_date": start_date,
                "end_date": end_date if self.end_date_var.get() else None,
                "reminder_type": reminder_type
            })
            self.task_entry.delete(0, tk.END)
            self.main_menu()
        else:
            self.set_message("Please enter a task", "red")

    def check_reminders(self):
        now = datetime.now().strftime("%Y-%m-%d")
        for task in self.tasks:
            if task['end_date'] == now:
                notification.notify(
                    title="Task Reminder",
                    message=f"The due date for '{task['task']}' is today!",
                    timeout=10
                )
        self.root.after(10000, self.check_reminders)

    def set_message(self, message, color="red"):
        self.message_label = tk.Label(self.root, text=message, fg=color, bg="#f0f0f0", font=("Helvetica", 12))
        self.message_label.pack(pady=5)
        self.message_label.after(3000, lambda: self.message_label.pack_forget())

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_azd_label(self):
        self.azd_label = tk.Label(self.root, text="AZD", bg="#f0f0f0", font=("Helvetica", 12, "bold"))
        self.azd_label.pack(side="bottom", pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
