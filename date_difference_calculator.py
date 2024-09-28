import tkinter as tk
from tkinter import ttk
from datetime import datetime

def validate_input(char):
    return char.isdigit()

def calculate_date_difference(start_day, start_month, start_year, end_day, end_month, end_year, result_panel, reset_btn):
    try:
        start_date = f"{int(start_day):02d}-{int(start_month):02d}-{int(start_year)}"
        end_date = f"{int(end_day):02d}-{int(end_month):02d}-{int(end_year)}"
        
        start = datetime.strptime(start_date, '%d-%m-%Y')
        end = datetime.strptime(end_date, '%d-%m-%Y')
        
        delta = end - start
        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30
        total_months = (years * 12) + months

        result_panel.config(state=tk.NORMAL)
        result_panel.delete(1.0, tk.END)
        result_panel.insert(tk.END, f"Difference: {years} years, {months} months, and {days} days\n")
        result_panel.insert(tk.END, f"Total days: {delta.days} days\n")
        result_panel.insert(tk.END, f"Total months: {total_months} months\n")
        result_panel.config(state=tk.DISABLED)

        reset_btn.config(state=tk.NORMAL)
    except ValueError:
        result_panel.config(state=tk.NORMAL)
        result_panel.delete(1.0, tk.END)
        result_panel.insert(tk.END, "Error: Please enter valid dates in the format DD-MM-YYYY.\n")
        result_panel.config(state=tk.DISABLED)

def reset_fields(start_day, start_month, start_year, end_day, end_month, end_year, result_panel, reset_btn):
    start_day.delete(0, tk.END)
    start_month.delete(0, tk.END)
    start_year.delete(0, tk.END)
    end_day.delete(0, tk.END)
    end_month.delete(0, tk.END)
    end_year.delete(0, tk.END)
    result_panel.config(state=tk.NORMAL)
    result_panel.delete(1.0, tk.END)
    result_panel.config(state=tk.DISABLED)
    reset_btn.config(state=tk.DISABLED)

def on_input_change(reset_btn):
    reset_btn.config(state=tk.NORMAL)

def create_gui():
    root = tk.Tk()
    root.title("Date Difference Calculator")
    
    root.geometry("450x480")
    root.configure(bg='#F0F8FF')

    title_font = ("Arial", 28, 'bold')
    label_font = ("Arial", 14, 'bold')
    small_font = ("Arial", 9)
    result_font = ("Courier", 12)
    
    title = tk.Label(root, text="Calculate the Difference\nBetween Two Dates", bg='#F0F8FF', font=title_font)
    title.pack(pady=20)

    format_label = tk.Label(root, text="(Format: DD-MM-YYYY)", bg='#F0F8FF', font=small_font, fg="#555")
    format_label.pack()

    date_frame = tk.Frame(root, bg='#F0F8FF')
    date_frame.pack(pady=10)

    start_label = tk.Label(date_frame, text="Start Date:", bg='#F0F8FF', font=label_font)
    start_label.grid(row=0, column=0, padx=10, pady=5)

    start_day = ttk.Entry(date_frame, width=3, validate="key", font=label_font)
    start_day['validatecommand'] = (start_day.register(validate_input), '%S')
    start_day.grid(row=0, column=1, padx=5)
    
    start_month = ttk.Entry(date_frame, width=3, validate="key", font=label_font)
    start_month['validatecommand'] = (start_month.register(validate_input), '%S')
    start_month.grid(row=0, column=2, padx=5)
    
    start_year = ttk.Entry(date_frame, width=5, validate="key", font=label_font)
    start_year['validatecommand'] = (start_year.register(validate_input), '%S')
    start_year.grid(row=0, column=3, padx=5)

    end_label = tk.Label(date_frame, text="End Date:", bg='#F0F8FF', font=label_font)
    end_label.grid(row=1, column=0, padx=10, pady=5)

    end_day = ttk.Entry(date_frame, width=3, validate="key", font=label_font)
    end_day['validatecommand'] = (end_day.register(validate_input), '%S')
    end_day.grid(row=1, column=1, padx=5)
    
    end_month = ttk.Entry(date_frame, width=3, validate="key", font=label_font)
    end_month['validatecommand'] = (end_month.register(validate_input), '%S')
    end_month.grid(row=1, column=2, padx=5)
    
    end_year = ttk.Entry(date_frame, width=5, validate="key", font=label_font)
    end_year['validatecommand'] = (end_year.register(validate_input), '%S')
    end_year.grid(row=1, column=3, padx=5)

    result_panel = tk.Text(root, height=6, width=45, state=tk.DISABLED, bg='#E6E6FA', font=result_font, fg="#4B0082")
    result_panel.pack(pady=10)

    button_frame = tk.Frame(root, bg='#F0F8FF')
    button_frame.pack(pady=10)

    calculate_btn = ttk.Button(button_frame, text="Calculate", command=lambda: calculate_date_difference(
        start_day.get(), start_month.get(), start_year.get(), end_day.get(), end_month.get(), end_year.get(), result_panel, reset_btn))
    calculate_btn.grid(row=0, column=0, padx=5)

    reset_btn = ttk.Button(button_frame, text="X", command=lambda: reset_fields(start_day, start_month, start_year, end_day, end_month, end_year, result_panel, reset_btn))
    reset_btn.grid(row=0, column=1, padx=5)
    reset_btn.config(state=tk.DISABLED)

    for widget in [start_day, start_month, start_year, end_day, end_month, end_year]:
        widget.bind("<KeyRelease>", lambda event: on_input_change(reset_btn))

    azd_label = tk.Label(root, text="AZD", bg='#F0F8FF', font=("Arial", 12, "bold"))
    azd_label.pack(side=tk.BOTTOM, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
