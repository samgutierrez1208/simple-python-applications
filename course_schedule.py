import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Schedule Application")
        self.root.geometry("1350x700")
        self.root.configure(bg="#f4f4f4")

        self.schedule_data = []
        self.show_courses()

    def show_courses(self):
        self.clear_frame()

        courses_frame = tk.Frame(self.root, bg="#f4f4f4")
        courses_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(courses_frame, bg="#4CAF50", height=50)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame, text="Courses", font=("Arial", 18, "bold"), fg="white", bg="#4CAF50")
        header_label.pack(pady=10)

        self.course_table = ttk.Treeview(courses_frame, columns=("Name", "Code", "Instructor", "Classroom", "Day", "Time"), show="headings")
        self.course_table.heading("Name", text="Course Name")
        self.course_table.heading("Code", text="Course Code")
        self.course_table.heading("Instructor", text="Instructor")
        self.course_table.heading("Classroom", text="Classroom")
        self.course_table.heading("Day", text="Day")
        self.course_table.heading("Time", text="Time")
        self.course_table.column("Name", width=150, anchor=tk.W)
        self.course_table.column("Code", width=100, anchor=tk.CENTER)
        self.course_table.column("Instructor", width=150, anchor=tk.CENTER)
        self.course_table.column("Classroom", width=100, anchor=tk.CENTER)
        self.course_table.column("Day", width=100, anchor=tk.CENTER)
        self.course_table.column("Time", width=100, anchor=tk.CENTER)
        self.course_table.pack(pady=20, fill=tk.BOTH, expand=True)

        self.load_courses()

        # Footer Buttons
        btn_frame = tk.Frame(courses_frame, bg="#f4f4f4")
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        self.name_entry = self.create_placeholder_entry(btn_frame, "Course Name", width=15)
        self.name_entry.pack(side=tk.LEFT, padx=5, pady=10)

        self.code_entry = self.create_placeholder_entry(btn_frame, "Code", width=10)
        self.code_entry.pack(side=tk.LEFT, padx=5, pady=10)

        self.instructor_entry = self.create_placeholder_entry(btn_frame, "Instructor", width=15)
        self.instructor_entry.pack(side=tk.LEFT, padx=5, pady=10)

        self.classroom_entry = self.create_placeholder_entry(btn_frame, "Classroom", width=10)
        self.classroom_entry.pack(side=tk.LEFT, padx=5, pady=10)

        self.day_entry = tk.Entry(btn_frame, font=("Arial", 12), width=10, state="readonly")
        self.day_entry.pack(side=tk.LEFT, padx=5, pady=10)

        self.time_entry = tk.Entry(btn_frame, font=("Arial", 12), width=15, state="readonly")
        self.time_entry.pack(side=tk.LEFT, padx=5, pady=10)

        day_button = tk.Button(btn_frame, text="Select Day", font=("Arial", 12), bg="#FFC107", fg="black", command=self.select_day)
        day_button.pack(side=tk.LEFT, padx=5, pady=10)

        time_button = tk.Button(btn_frame, text="Select Time", font=("Arial", 12), bg="#FFC107", fg="black", command=self.select_time)
        time_button.pack(side=tk.LEFT, padx=5, pady=10)

        add_button = tk.Button(btn_frame, text="Add", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=self.add_course)
        add_button.pack(side=tk.LEFT, padx=20)

        delete_button = tk.Button(btn_frame, text="Delete", font=("Arial", 12, "bold"), bg="#F44336", fg="white", command=self.delete_course)
        delete_button.pack(side=tk.LEFT, padx=10)

        edit_button = tk.Button(btn_frame, text="Edit", font=("Arial", 12, "bold"), bg="#FFC107", fg="black", command=self.edit_course)
        edit_button.pack(side=tk.LEFT, padx=10)

        azd_label = tk.Label(btn_frame, text="AZD", font=("Arial", 12, "bold"), bg="#f4f4f4", fg="black")
        azd_label.pack(side=tk.LEFT, padx=20, pady=10)

    def create_placeholder_entry(self, parent, placeholder, width):
        entry = tk.Entry(parent, font=("Arial", 12), width=width)
        entry.insert(0, placeholder)

        def clear_placeholder(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)

        def restore_placeholder(event):
            if entry.get() == "":
                entry.insert(0, placeholder)

        entry.bind("<FocusIn>", clear_placeholder)
        entry.bind("<FocusOut>", restore_placeholder)
        return entry

    def select_day(self):
        day_window = tk.Toplevel(self.root)
        day_window.title("Select Day")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        selected_day = tk.StringVar(value="Monday")

        for day in days:
            tk.Radiobutton(day_window, text=day, variable=selected_day, value=day, font=("Arial", 12)).pack(anchor=tk.W, pady=5)

        def save_day():
            self.day_entry.config(state="normal")
            self.day_entry.delete(0, tk.END)
            self.day_entry.insert(0, selected_day.get())
            self.day_entry.config(state="readonly")
            day_window.destroy()

        tk.Button(day_window, text="Save", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=save_day).pack(pady=10)

    def select_time(self):
        time_window = tk.Toplevel(self.root)
        time_window.title("Select Time")

        tk.Label(time_window, text="Start Time:", font=("Arial", 12)).pack(pady=5)
        start_time = ttk.Combobox(time_window, values=[f"{hour:02d}:00" for hour in range(24)], font=("Arial", 12))
        start_time.pack(pady=5)
        start_time.set("08:00")

        tk.Label(time_window, text="End Time:", font=("Arial", 12)).pack(pady=5)
        end_time = ttk.Combobox(time_window, values=[f"{hour:02d}:00" for hour in range(24)], font=("Arial", 12))
        end_time.pack(pady=5)
        end_time.set("17:00")

        def save_time():
            self.time_entry.config(state="normal")
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, f"{start_time.get()} - {end_time.get()}")
            self.time_entry.config(state="readonly")
            time_window.destroy()

        tk.Button(time_window, text="Save", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=save_time).pack(pady=10)

    def add_course(self):
        course = {
            "name": self.name_entry.get(),
            "code": self.code_entry.get(),
            "instructor": self.instructor_entry.get(),
            "classroom": self.classroom_entry.get(),
            "day": self.day_entry.get(),
            "time": self.time_entry.get()
        }
        self.schedule_data.append(course)
        self.load_courses()

    def load_courses(self):
        self.course_table.delete(*self.course_table.get_children())
        sorted_courses = sorted(self.schedule_data, key=lambda x: (x["day"], x["time"]))
        for course in sorted_courses:
            self.course_table.insert("", "end", values=(course["name"], course["code"], course["instructor"], course["classroom"], course["day"], course["time"]))

    def delete_course(self):
        selected_item = self.course_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No course selected to delete.")
            return
        item = self.course_table.item(selected_item)
        course_values = item["values"]
        for course in self.schedule_data:
            if (course["name"], course["code"], course["instructor"], course["classroom"], course["day"], course["time"]) == tuple(course_values):
                self.schedule_data.remove(course)
                break
        self.load_courses()

    def edit_course(self):
        selected_item = self.course_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No course selected to edit.")
            return
        item = self.course_table.item(selected_item)
        course_values = item["values"]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Course")

        tk.Label(edit_window, text="Course Name:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(edit_window, font=("Arial", 12), width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, course_values[0])

        tk.Label(edit_window, text="Course Code:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        code_entry = tk.Entry(edit_window, font=("Arial", 12), width=20)
        code_entry.grid(row=1, column=1, padx=5, pady=5)
        code_entry.insert(0, course_values[1])

        tk.Label(edit_window, text="Instructor:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        instructor_entry = tk.Entry(edit_window, font=("Arial", 12), width=20)
        instructor_entry.grid(row=2, column=1, padx=5, pady=5)
        instructor_entry.insert(0, course_values[2])

        tk.Label(edit_window, text="Classroom:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        classroom_entry = tk.Entry(edit_window, font=("Arial", 12), width=20)
        classroom_entry.grid(row=3, column=1, padx=5, pady=5)
        classroom_entry.insert(0, course_values[3])

        tk.Label(edit_window, text="Day:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5)
        day_entry = tk.Entry(edit_window, font=("Arial", 12), width=20)
        day_entry.grid(row=4, column=1, padx=5, pady=5)
        day_entry.insert(0, course_values[4])

        tk.Label(edit_window, text="Time:", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=5)
        time_entry = tk.Entry(edit_window, font=("Arial", 12), width=20)
        time_entry.grid(row=5, column=1, padx=5, pady=5)
        time_entry.insert(0, course_values[5])

        def save_changes():
            updated_course = {
                "name": name_entry.get(),
                "code": code_entry.get(),
                "instructor": instructor_entry.get(),
                "classroom": classroom_entry.get(),
                "day": day_entry.get(),
                "time": time_entry.get()
            }
            for course in self.schedule_data:
                if (course["name"], course["code"], course["instructor"], course["classroom"], course["day"], course["time"]) == tuple(course_values):
                    course.update(updated_course)
                    break
            self.load_courses()
            edit_window.destroy()

        tk.Button(edit_window, text="Save", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=save_changes).grid(row=6, columnspan=2, pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()
