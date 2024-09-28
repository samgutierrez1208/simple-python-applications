import tkinter as tk
from tkinter import ttk, filedialog
import docx

def count_text(text):
    spaces = text.count(' ')
    words = text.split()
    sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
    total_letters = sum(len(word) for word in words)
    
    space_count.set(f"Spaces: {spaces}")
    word_count.set(f"Words: {len(words)}")
    sentence_count.set(f"Sentences: {len(sentences)}")
    letter_count.set(f"Letters: {total_letters}")

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("Word documents", "*.docx")]
    )
    
    if not file_path:
        set_status_message("No file selected.", clear_after=2000)  # 2 seconds delay
        return
    
    try:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            set_status_message("Invalid file type. Please select a .txt or .docx file.", clear_after=2000)
            return
        
        text_input.delete(1.0, tk.END)
        text_input.insert(tk.END, text)
        count_text(text)
        upload_button.config(state="disabled")
        clear_button.config(state="normal")
        set_status_message("File loaded successfully.", clear_after=2000)
    except Exception as e:
        set_status_message(f"Error loading file: {str(e)}", clear_after=2000)

def clear_text():
    text_input.delete(1.0, tk.END)
    space_count.set("")
    word_count.set("")
    sentence_count.set("")
    letter_count.set("")
    upload_button.config(state="normal")
    clear_button.config(state="disabled")
    set_status_message("Cleared all text.", clear_after=2000)

def on_text_change(event=None):
    text = text_input.get("1.0", tk.END).strip()
    if text:
        upload_button.config(state="disabled")
        clear_button.config(state="normal")
    else:
        upload_button.config(state="normal")
        clear_button.config(state="disabled")
    count_text(text)

def set_status_message(message, clear_after=None):
    status_message.set(message)
    if clear_after:
        root.after(clear_after, lambda: status_message.set(""))  # Clear message after a delay

root = tk.Tk()
root.title("Advanced Word Counter")
root.geometry("600x400")
root.config(bg="#2b3e50")

title_label = tk.Label(root, text="Advanced Word Counter", font=('Arial', 22, 'bold'), bg='#2b3e50', fg='white')
title_label.pack(pady=10)

text_input = tk.Text(root, height=5, font=('Arial', 14), wrap='word')
text_input.pack(pady=10)
text_input.bind("<KeyRelease>", on_text_change)

button_frame = tk.Frame(root, bg="#2b3e50")
button_frame.pack(pady=10)

upload_button = tk.Button(button_frame, text="Upload .txt or .docx", command=open_file, bg='#3498db', fg='white', font=('Arial', 16, 'bold'))
upload_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text="X", command=clear_text, bg='#e74c3c', fg='white', font=('Arial', 16, 'bold'), state="disabled")
clear_button.grid(row=0, column=1, padx=10)

summary_frame = tk.Frame(root, bg='#2b3e50')
summary_frame.pack(pady=10)

space_count = tk.StringVar()
word_count = tk.StringVar()
sentence_count = tk.StringVar()
letter_count = tk.StringVar()

space_label = tk.Label(summary_frame, textvariable=space_count, font=('Arial', 16), bg='#2b3e50', fg='white')
word_label = tk.Label(summary_frame, textvariable=word_count, font=('Arial', 16), bg='#2b3e50', fg='white')
sentence_label = tk.Label(summary_frame, textvariable=sentence_count, font=('Arial', 16), bg='#2b3e50', fg='white')
letter_label = tk.Label(summary_frame, textvariable=letter_count, font=('Arial', 16), bg='#2b3e50', fg='white')

space_label.grid(row=0, column=0, padx=10)
word_label.grid(row=0, column=1, padx=10)
sentence_label.grid(row=0, column=2, padx=10)
letter_label.grid(row=0, column=3, padx=10)

status_message = tk.StringVar()
status_label = tk.Label(root, textvariable=status_message, font=('Arial', 14), bg='#2b3e50', fg='yellow')
status_label.pack(pady=10)

azd_label = tk.Label(root, text="AZD", font=('Arial', 12, 'bold'), bg='#2b3e50', fg='white')
azd_label.pack(pady=10)

root.mainloop()
