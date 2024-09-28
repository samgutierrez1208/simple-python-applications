import tkinter as tk
from tkinter import filedialog, scrolledtext
import docx
import re

def is_palindrome(word):
    word = re.sub(r'[^A-Za-z0-9]', '', word.lower())
    return word == word[::-1] and len(word) > 1

def find_palindromes(text):
    words = re.findall(r'\b\w+\b', text)
    palindromes = [word for word in words if is_palindrome(word)]
    return palindromes

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Word files", "*.docx *.doc")])
    if file_path:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                text_input.delete(1.0, tk.END)
                text_input.insert(tk.END, file.read())
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            text_input.delete(1.0, tk.END)
            text_input.insert(tk.END, '\n'.join([para.text for para in doc.paragraphs]))
        reset_button.config(state=tk.NORMAL)
        update_palindrome_count()

def reset_input():
    text_input.delete(1.0, tk.END)
    result_label.config(text="Palindrome count: 0")
    reset_button.config(state=tk.DISABLED)
    list_palindromes_button.config(state=tk.DISABLED)
    palindromes_listbox.place_forget()

def update_palindrome_count(event=None):
    text = text_input.get(1.0, tk.END).strip()
    palindromes = find_palindromes(text)
    result_label.config(text=f"Palindrome count: {len(palindromes)}")
    
    if len(text) > 0:
        reset_button.config(state=tk.NORMAL)
        list_palindromes_button.config(state=tk.NORMAL)
    else:
        reset_button.config(state=tk.DISABLED)
        list_palindromes_button.config(state=tk.DISABLED)

def display_palindromes():
    palindromes = find_palindromes(text_input.get(1.0, tk.END).strip())
    if palindromes:
        hide_elements()
        palindromes_listbox.delete(0, tk.END)
        for palindrome in palindromes:
            palindromes_listbox.insert(tk.END, palindrome)
        palindromes_listbox.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        back_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

def hide_elements():
    text_input.pack_forget()
    result_label.pack_forget()
    load_button.pack_forget()
    reset_button.pack_forget()
    list_palindromes_button.pack_forget()

def restore_main_interface():
    palindromes_listbox.place_forget()
    back_button.place_forget()
    text_input.pack()
    result_label.pack()
    button_frame.pack()

root = tk.Tk()
root.title("Palindrome Checker")
root.geometry("600x450")
root.configure(bg='#f0f0f5')

top_frame = tk.Frame(root, bg='#f0f0f5')
top_frame.pack(pady=10)


text_input = scrolledtext.ScrolledText(top_frame, height=10, width=60, bg='#ffffff', fg='#333333', font=("Arial", 12))
text_input.pack()
text_input.bind("<KeyRelease>", update_palindrome_count)

button_frame = tk.Frame(root, bg='#f0f0f5')
button_frame.pack(pady=10)

load_button = tk.Button(button_frame, text="Load File", command=load_file, bg='#4CAF50', fg='#ffffff', font=("Arial", 12, 'bold'), height=2, width=12)
load_button.grid(row=0, column=0, padx=10)

reset_button = tk.Button(button_frame, text="X", state=tk.DISABLED, command=reset_input, bg='#FF5733', fg='#ffffff', font=("Arial", 12, 'bold'), height=2, width=12)
reset_button.grid(row=0, column=1, padx=10)

list_palindromes_button = tk.Button(button_frame, text="List Palindromes", command=display_palindromes, state=tk.DISABLED, bg='#2196F3', fg='#ffffff', font=("Arial", 12, 'bold'), height=2, width=12)
list_palindromes_button.grid(row=0, column=2, padx=10)

result_label = tk.Label(root, text="Palindrome count: 0", bg='#f0f0f5', fg='#333333', font=("Arial", 14))
result_label.pack(pady=10)

palindromes_listbox = tk.Listbox(root, height=10, width=50, bg='#ffffff', fg='#333333', font=("Arial", 12))

back_button = tk.Button(root, text="Back", command=restore_main_interface, bg='#FF5733', fg='#ffffff', font=("Arial", 12, 'bold'), height=2, width=12)

footer_label = tk.Label(root, text="AZD", bg='#f0f0f5', fg='#333333', font=("Arial", 10, 'bold'))
footer_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()
