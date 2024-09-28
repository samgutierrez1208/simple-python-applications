import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, timedelta
import json

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Agenda Application")
        self.root.geometry("1000x600")
        
        self.status_panel = tk.Frame(self.root, bg="lightgray", height=30)
        self.status_panel.pack(side="bottom", fill="x")
        self.status_label = tk.Label(self.status_panel, text="Welcome! AZD", anchor="w", bg="lightgray")
        self.status_label.pack(fill="x")
        
        self.events = self.load_events()
        
        self.year = datetime.now().year
        self.month = datetime.now().month
        
        self.top_frame = tk.Frame(self.root, bg="lightgray", height=50)
        self.top_frame.pack(side="top", fill="x")
        
        self.month_var = tk.IntVar()
        self.month_combo = ttk.Combobox(self.top_frame, textvariable=self.month_var, values=list(range(1, 13)), width=5, font=("Arial", 12))
        self.month_combo.current(self.month - 1)
        self.month_combo.pack(side="left", padx=5, pady=10)
        
        self.year_var = tk.IntVar()
        self.year_spinbox = tk.Spinbox(self.top_frame, from_=2000, to=2100, textvariable=self.year_var, width=5, font=("Arial", 12))
        self.year_var.set(self.year)
        self.year_spinbox.pack(side="left", padx=5, pady=10)
        
        self.go_button = tk.Button(self.top_frame, text="Go", command=self.update_calendar)
        self.go_button.pack(side="left", padx=5)
        
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        
        self.calendar_frame = tk.Frame(self.main_frame, bg="white", width=300, height=700)
        self.calendar_frame.pack(side="left", padx=10, pady=20, fill="y", expand=False)
        
        self.controls_frame = tk.Frame(self.main_frame, bg="white", width=300)
        self.controls_frame.pack(side="right", fill="y", padx=40, pady=20)
        
        self.create_calendar()
        self.create_controls()

        self.azd_label = tk.Label(self.root, text="AZD", font=("Arial", 12), anchor="center")
        self.azd_label.pack(side="bottom", pady=5)

        self.update_status("Agenda application started.")
        
    def load_events(self):
        try:
            with open("events.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_events(self):
        with open("events.json", "w") as f:
            json.dump(self.events, f)
        
    def update_status(self, message):
        self.status_label.config(text=message)
        
    def create_calendar(self):
        self.calendar_label = tk.Label(self.calendar_frame, text="Calendar", font=("Arial", 14), bg="white")
        self.calendar_label.pack()
        
        self.calendar_table = tk.Frame(self.calendar_frame, bg="white")
        self.calendar_table.pack(fill="both")

        self.update_calendar()

    def update_calendar(self, event=None):
        for widget in self.calendar_table.winfo_children():
            widget.destroy()

        self.year = int(self.year_var.get())
        self.month = int(self.month_var.get())
        
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days_of_week):
            tk.Label(self.calendar_table, text=day, font=("Arial", 12, "bold"), bg="lightgray", width=8, height=3).grid(row=0, column=i)

        cal = calendar.monthcalendar(self.year, self.month)

        for row_idx, week in enumerate(cal, start=1):
            for col_idx, day in enumerate(week):
                if day != 0:
                    lbl = tk.Label(self.calendar_table, text=str(day), font=("Arial", 12), width=8, height=3)
                    lbl.grid(row=row_idx, column=col_idx, padx=1, pady=1)
                    lbl.bind("<Button-1>", lambda event, d=day: self.show_event_details(d))
        
        self.mark_events()
        
        self.update_status(f"Displaying calendar for {self.month}/{self.year}.")
        
    def mark_events(self):
        month_events = self.events.get(f"{self.year}-{self.month}", [])
        for event in month_events:
            day = event['day']
            desc = event['description']
            for widget in self.calendar_table.winfo_children():
                if widget.cget("text") == str(day):
                    widget.config(bg="lightblue", text=f"{day}\n{desc}")

    def validate_date_format(self, date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Correct format: dd/mm/yyyy")

    def show_event_details(self, day):
        month_key = f"{self.year}-{self.month}"
        events_for_day = [event for event in self.events.get(month_key, []) if event['day'] == day]
        
        if events_for_day:
            group_id = events_for_day[0]['group_id']
            group_events = [event for val in self.events.values() for event in val if event.get('group_id') == group_id]
            start_event = min(group_events, key=lambda x: (x['day']))
            end_event = max(group_events, key=lambda x: (x['day']))
            
            start_date = datetime(self.year, self.month, start_event['day'])
            end_date = datetime(self.year, self.month, end_event['day'])
            
            start_date_str = start_date.strftime("%d/%m/%Y")
            end_date_str = end_date.strftime("%d/%m/%Y")

            self.clear_controls()

            self.event_label = tk.Label(self.controls_frame, text=f"Event: {start_event['description']}", font=("Arial", 14), bg="white")
            self.event_label.pack(pady=10)
            
            self.date_label = tk.Label(self.controls_frame, text=f"Date: {start_date_str} - {end_date_str}", font=("Arial", 14), bg="white")
            self.date_label.pack(pady=10)

            self.remove_button = tk.Button(self.controls_frame, text="Remove Event", command=lambda: self.remove_event(group_id))
            self.remove_button.pack(pady=10)

            self.exit_button = tk.Button(self.controls_frame, text="Exit", command=self.reset_controls)
            self.exit_button.pack(pady=10)

    def clear_controls(self):
        for widget in self.controls_frame.winfo_children():
            widget.destroy()

    def reset_controls(self):
        self.clear_controls()
        self.create_controls()

    def remove_event(self, group_id):
        self.events = {key: [event for event in val if event.get('group_id') != group_id] for key, val in self.events.items()}
        self.save_events()
        self.update_calendar()
        self.update_status("Event group removed.")
        self.reset_controls()
    
    def create_controls(self):
        self.event_label = tk.Label(self.controls_frame, text="Add New Event", font=("Arial", 16), bg="white")
        self.event_label.pack(pady=10)
        
        self.event_entry = tk.Entry(self.controls_frame, font=("Arial", 14), width=40)
        self.event_entry.pack(pady=5)
        self.event_entry.insert(0, "Event Name")
        self.event_entry.bind("<FocusIn>", lambda event: self.on_entry_click(self.event_entry, "Event Name"))
        self.event_entry.bind("<FocusOut>", lambda event: self.on_focusout(self.event_entry, "Event Name"))
        
        self.date_entry = tk.Entry(self.controls_frame, font=("Arial", 14), width=40)
        self.date_entry.pack(pady=5)
        self.date_entry.insert(0, "DD/MM/YYYY (Start)")
        self.date_entry.bind("<FocusIn>", lambda event: self.on_entry_click(self.date_entry, "DD/MM/YYYY (Start)"))
        self.date_entry.bind("<FocusOut>", lambda event: self.on_focusout(self.date_entry, "DD/MM/YYYY (Start)"))
        
        self.end_date_entry = tk.Entry(self.controls_frame, font=("Arial", 14), width=40)
        self.end_date_entry.pack(pady=5)
        self.end_date_entry.insert(0, "DD/MM/YYYY (End)")
        self.end_date_entry.bind("<FocusIn>", lambda event: self.on_entry_click(self.end_date_entry, "DD/MM/YYYY (End)"))
        self.end_date_entry.bind("<FocusOut>", lambda event: self.on_focusout(self.end_date_entry, "DD/MM/YYYY (End)"))
        
        self.add_event_button = tk.Button(self.controls_frame, text="Add Event", command=self.add_event)
        self.add_event_button.pack(pady=10)
        
        self.recurring_var = tk.IntVar()
        self.recurring_check = tk.Checkbutton(self.controls_frame, text="Repeat every year", variable=self.recurring_var, bg="white")
        self.recurring_check.pack(pady=5)
        
    def on_entry_click(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")

    def on_focusout(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")
        
    def add_event(self):
        event_desc = self.event_entry.get()
        date_str = self.date_entry.get()
        end_date_str = self.end_date_entry.get()
        
        try:
            start_date = self.validate_date_format(date_str)
            end_date = self.validate_date_format(end_date_str)
            duration = (end_date - start_date).days + 1
            group_id = datetime.now().strftime("%Y%m%d%H%M%S")
            
            for i in range(duration):
                event_day = (start_date + timedelta(days=i)).day
                month_key = f"{start_date.year}-{start_date.month}"
                
                if month_key not in self.events:
                    self.events[month_key] = []
                
                self.events[month_key].append({"day": event_day, "description": event_desc, "group_id": group_id, "duration": duration})
            
            self.save_events()
            self.update_calendar()
            self.update_status(f"Event added: {event_desc} - {date_str} ({duration} days)")
            
            if self.recurring_var.get():
                for year in range(start_date.year + 1, 2101):
                    for i in range(duration):
                        event_day = (start_date + timedelta(days=i)).day
                        month_key = f"{year}-{start_date.month}"
                        if month_key not in self.events:
                            self.events[month_key] = []
                        self.events[month_key].append({"day": event_day, "description": event_desc, "group_id": group_id, "duration": duration})
                self.save_events()
                self.update_status(f"Event repeated for each year: {event_desc}")

        except ValueError as ve:
            self.update_status(str(ve))

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
