import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

def generate_password():
    length = length_var.get()

    if length == 0:
        warning_label.config(text="Please select a password length!", fg="red")
        return
    else:
        warning_label.config(text="")

    allowed_symbols = "*+-/"

    all_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + allowed_symbols

    while True:
        password = ''.join(random.choice(all_characters) for _ in range(length))
        if password[0] == '0':
            continue
        if not any(char.isupper() for char in password):
            continue
        if not any(char.islower() for char in password):
            continue
        if not any(char.isdigit() for char in password):
            continue
        if not any(char in allowed_symbols for char in password):
            continue
        break

    password_var.set(password)
    reset_buttons()
    generate_button.config(state="disabled")
    copy_status_label.config(text="")

def copy_to_clipboard():
    password = password_var.get()
    if password:
        pyperclip.copy(password)
        copy_status_label.config(text="✓", fg='green')
    else:
        copy_status_label.config(text="X", fg='red')

    root.after(2000, lambda: copy_status_label.config(text=""))

def select_length():
    selected_length = length_var.get()
    if selected_length == 8:
        button_8.config(bg='#2ecc71')
        button_12.config(bg='#ecf0f1')
    elif selected_length == 12:
        button_12.config(bg='#2ecc71')
        button_8.config(bg='#ecf0f1')

    warning_label.config(text="")
    generate_button.config(state="normal")
    copy_button.config(state="disabled")

def reset_buttons():
    button_8.config(bg='#ecf0f1')
    button_12.config(bg='#ecf0f1')

def enable_copy_button():
    copy_button.config(state="normal")

root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("550x450")
root.config(bg="#2b3e50")

title_label = tk.Label(root, text="Random Password Generator", font=('Arial', 20, 'bold'), bg='#2b3e50', fg='white')
title_label.pack(pady=20)

length_var = tk.IntVar(value=0)

length_frame = tk.Frame(root, bg='#2b3e50')
length_label = tk.Label(length_frame, text="Select Password Length:", bg='#2b3e50', fg='white', font=('Arial', 16))
length_label.pack()

button_8 = tk.Button(length_frame, text="8 Characters", command=lambda: [length_var.set(8), select_length()], font=('Arial', 14), fg='black', bg='#ecf0f1', width=15)
button_12 = tk.Button(length_frame, text="12 Characters", command=lambda: [length_var.set(12), select_length()], font=('Arial', 14), fg='black', bg='#ecf0f1', width=15)

button_8.pack(side="left", padx=10, pady=10)
button_12.pack(side="left", padx=10, pady=10)
length_frame.pack(pady=10)

password_var = tk.StringVar()
password_entry = ttk.Entry(root, textvariable=password_var, font=('Arial', 18), width=25, state='readonly')
password_entry.pack(pady=20)

button_frame = tk.Frame(root, bg='#2b3e50')
generate_button = tk.Button(button_frame, text="Generate Password", command=lambda: [generate_password(), enable_copy_button()], bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'), state="disabled")
copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg='#f39c12', fg='white', font=('Arial', 14, 'bold'), state="disabled")

generate_button.pack(side="left", padx=10)
copy_button.pack(side="left", padx=10)
button_frame.pack(pady=20)

copy_status_label = tk.Label(root, text="", font=('Arial', 14), bg='#2b3e50')
copy_status_label.pack()

warning_label = tk.Label(root, text="", font=('Arial', 12), bg='#2b3e50')
warning_label.pack(pady=5)

azd_label = tk.Label(root, text="AZD", font=('Arial', 12, 'bold'), bg='#2b3e50', fg='white')
azd_label.pack(pady=10)

root.mainloop()
