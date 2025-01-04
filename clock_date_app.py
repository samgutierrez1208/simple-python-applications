import tkinter as tk
from datetime import datetime
import tzlocal

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock")
        self.root.geometry("500x340")
        self.is_dark_mode = True

        self.local_timezone = tzlocal.get_localzone()

        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        self.lightbulb_button = tk.Button(self.root, text="\u2600", font=("Helvetica", 20), bg="#ffffff", fg="#000000", bd=0, command=self.toggle_theme)
        self.lightbulb_button.place(x=20, y=20)

        self.time_label = tk.Label(self.root, text="", font=("Helvetica", 60), fg="#000000")
        self.time_label.pack(pady=60)

        self.date_label = tk.Label(self.root, text="", font=("Helvetica", 24), fg="#000000")
        self.date_label.pack(pady=10)

        self.azd_label = tk.Label(self.root, text="AZD", font=("Helvetica", 12, 'bold'), fg="#000000")
        self.azd_label.pack(pady=10)

        self.set_light_mode()

    def update_clock(self):
        local_time = datetime.now(self.local_timezone)
        current_time = local_time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)

        current_date = local_time.strftime("%d %B %Y, %A")
        self.date_label.config(text=current_date)

        self.root.after(1000, self.update_clock)

    def toggle_theme(self):
        if self.is_dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def set_light_mode(self):
        self.root.configure(bg='#ffffff')
        self.time_label.config(fg="#000000", bg='#ffffff')
        self.date_label.config(fg="#000000", bg='#ffffff')
        self.lightbulb_button.config(bg='#ffffff', fg="#000000")
        self.azd_label.config(fg="#000000", bg='#ffffff')
        self.is_dark_mode = False

    def set_dark_mode(self):
        self.root.configure(bg='#1c1c1e')
        self.time_label.config(fg="#ffffff", bg='#1c1c1e')
        self.date_label.config(fg="#ffffff", bg='#1c1c1e')
        self.lightbulb_button.config(bg='#1c1c1e', fg="#FFD700")
        self.azd_label.config(fg="#ffffff", bg='#1c1c1e')
        self.is_dark_mode = True

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()
