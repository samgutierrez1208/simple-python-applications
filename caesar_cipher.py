import tkinter as tk
from tkinter import ttk

# Function to encrypt a message using Caesar Cipher
def encrypt_message(message, shift):
    encrypted = ""
    for char in message:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - start + shift) % 26 + start)
        else:
            encrypted += char
    return encrypted

# Function to decrypt a message using Caesar Cipher
def decrypt_message(message, shift):
    return encrypt_message(message, -shift)

# Function to clear all input and output fields
def clear_fields():
    input_text.set("")
    shift_value.set(0)
    output_label.config(text="")
    feedback_label.config(text="")

# Function to exit the application
def exit_app():
    root.destroy()

# Function to process input text (encrypt/decrypt)
def process_text(action):
    try:
        message = input_text.get()
        shift = shift_value.get()
        if not message:
            feedback_label.config(text="Error: Input text is empty.", fg="red")
            return
        if action == "encrypt":
            result = encrypt_message(message, shift)
        elif action == "decrypt":
            result = decrypt_message(message, shift)
        output_label.config(text=result)
        feedback_label.config(text="Success: Text processed.", fg="green")
    except Exception as e:
        feedback_label.config(text=f"Error: {str(e)}", fg="red")

# Function to copy output text to clipboard
def copy_to_clipboard(event):
    output_text = output_label.cget("text")
    if output_text:
        root.clipboard_clear()
        root.clipboard_append(output_text)
        root.update()
        feedback_label.config(text="Output copied to clipboard!", fg="green")

# Setting up the main GUI window
root = tk.Tk()
root.title("Caesar Cipher Tool")
root.geometry("500x450")
root.resizable(False, False)
root.config(bg="#222831")

# Input text field
input_text = tk.StringVar()
tk.Label(root, text="Input Text:", font=("Arial", 12), fg="white", bg="#222831").pack(pady=(20, 5))
input_entry = tk.Entry(root, textvariable=input_text, font=("Arial", 12), width=40)
input_entry.pack(pady=5)

# Shift value field
shift_value = tk.IntVar(value=0)
tk.Label(root, text="Shift Value:", font=("Arial", 12), fg="white", bg="#222831").pack(pady=(10, 5))
shift_spinbox = ttk.Spinbox(root, from_=-26, to=26, textvariable=shift_value, font=("Arial", 12), width=5)
shift_spinbox.pack(pady=5)

# Buttons for encryption, decryption, clear, and exit
button_frame = tk.Frame(root, bg="#222831")
button_frame.pack(pady=(20, 10))

tk.Button(button_frame, text="Encrypt", command=lambda: process_text("encrypt"), font=("Arial", 12), bg="#393E46", fg="white", width=10).grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Decrypt", command=lambda: process_text("decrypt"), font=("Arial", 12), bg="#393E46", fg="white", width=10).grid(row=1, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Clear", command=clear_fields, font=("Arial", 12), bg="#393E46", fg="white", width=10).grid(row=0, column=1, padx=10, pady=5)
tk.Button(button_frame, text="Exit", command=exit_app, font=("Arial", 12), bg="#393E46", fg="white", width=10).grid(row=1, column=1, padx=10, pady=5)

# Output text label
tk.Label(root, text="Output:", font=("Arial", 12), fg="white", bg="#222831").pack(pady=(20, 5))
output_label = tk.Label(root, text="", font=("Arial", 12), fg="#FFD369", bg="#222831", wraplength=450, justify="center")
output_label.pack(pady=5)
output_label.bind("<Button-1>", copy_to_clipboard)

# Feedback label for errors or status
feedback_label = tk.Label(root, text="", font=("Arial", 10), fg="white", bg="#222831")
feedback_label.pack(pady=(10, 5))

# Footer
footer = tk.Label(root, text="AZD", font=("Arial", 10, "italic"), fg="#FFD369", bg="#222831")
footer.pack(pady=(20, 10))

# Start the main event loop
root.mainloop()
