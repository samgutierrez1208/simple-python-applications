import tkinter as tk
from tkinter import messagebox
import random

class FibonacciGame:
    def __init__(self, master):
        self.master = master
        master.title("Fibonacci Sorting Game")
        master.geometry("500x250")
        master.configure(bg="lightblue")

        self.fib_sequence = self.generate_fibonacci(50)
        self.start, self.end = self.get_fibonacci_range()
        self.target_sequence = self.get_fibonacci_in_range(self.start, self.end)

        self.create_widgets()

    def generate_fibonacci(self, n):
        fib_sequence = [0, 1]
        for i in range(2, n):
            next_fib = fib_sequence[-1] + fib_sequence[-2]
            fib_sequence.append(next_fib)
        return fib_sequence

    def get_fibonacci_range(self):
        while True:
            start_index = random.randint(0, len(self.fib_sequence) - 7)
            start_fib = self.fib_sequence[start_index]
            end_fib = self.fib_sequence[start_index + 6]

            if len(self.get_fibonacci_in_range(start_fib, end_fib)) == 5:
                return start_fib, end_fib

    def get_fibonacci_in_range(self, start, end):
        return [num for num in self.fib_sequence if start < num < end]

    def create_widgets(self):
        self.instruction_text = f"Sort the Fibonacci numbers between\n{self.start} and {self.end}!"
        self.instruction_label = tk.Label(
            self.master, text=self.instruction_text,
            font=("Helvetica", 14), bg="lightblue", justify="center", fg="black"
        )
        self.instruction_label.pack(pady=10)

        self.entry_frame = tk.Frame(self.master, bg="lightblue")
        self.entry_frame.pack(pady=10)

        self.entries = []
        for i in range(len(self.target_sequence)):
            entry = tk.Entry(self.entry_frame, width=5, font=("Helvetica", 14), justify="center")
            entry.pack(side="left", padx=5)
            self.entries.append(entry)
            entry.bind("<KeyRelease>", self.check_entries_filled)

        self.button_frame = tk.Frame(self.master, bg="lightblue")
        self.button_frame.pack(pady=10)

        self.submit_button = tk.Button(
            self.button_frame, text="Submit", command=self.check_sequence, font=("Helvetica", 12), bg="white", state="disabled"
        )
        self.submit_button.grid(row=0, column=1, padx=10)

        self.change_range_button = tk.Button(
            self.button_frame, text="Change Range", command=self.change_range, font=("Helvetica", 12), bg="yellow"
        )
        self.change_range_button.grid(row=0, column=0, padx=10)

        self.restart_button = tk.Button(
            self.button_frame, text="Play Again", command=self.reset_game, font=("Helvetica", 12), bg="blue", fg="white"
        )
        self.exit_button = tk.Button(
            self.button_frame, text="Exit", command=self.master.quit, font=("Helvetica", 12), bg="red", fg="white"
        )

        self.azd_label = tk.Label(
            self.master, text="AZD", font=("Helvetica", 16, "bold"), bg="lightblue"
        )
        self.azd_label.pack(pady=10)

    def check_entries_filled(self, event=None):
        all_filled = all(entry.get() for entry in self.entries)
        if all_filled:
            self.submit_button.config(state="normal")
        else:
            self.submit_button.config(state="disabled")

    def check_sequence(self):
        user_input = []
        for entry in self.entries:
            try:
                user_input.append(int(entry.get()))
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")
                return

        if user_input == sorted(self.target_sequence):
            self.show_result("✓", "green")
        else:
            self.show_result("✗", "red")
        self.end_game()

    def show_result(self, symbol, color):
        new_text = f"Sort the Fibonacci numbers between\n{self.start} and {self.end}! {symbol}"
        self.instruction_label.config(text=new_text, fg=color)

    def change_range(self):
        self.start, self.end = self.get_fibonacci_range()
        self.target_sequence = self.get_fibonacci_in_range(self.start, self.end)

        self.instruction_label.config(
            text=f"Sort the Fibonacci numbers between\n{self.start} and {self.end}!", fg="black"  # Reset to default color
        )
        self.reset_game(reset_entries=False)

    def end_game(self):
        self.submit_button.grid_forget()
        self.change_range_button.grid_forget()

        self.restart_button.grid(row=0, column=0, padx=10)
        self.exit_button.grid(row=0, column=1, padx=10)

    def reset_game(self, reset_entries=True):
        if reset_entries:
            for entry in self.entries:
                entry.delete(0, tk.END)

        self.restart_button.grid_forget()
        self.exit_button.grid_forget()

        self.submit_button.grid(row=0, column=1, padx=10)
        self.change_range_button.grid(row=0, column=0, padx=10)

        self.submit_button.config(state="disabled")

        self.start, self.end = self.get_fibonacci_range()
        self.target_sequence = self.get_fibonacci_in_range(self.start, self.end)

        self.instruction_label.config(
            text=f"Sort the Fibonacci numbers between\n{self.start} and {self.end}!", fg="black"  # Reset text color
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = FibonacciGame(root)
    root.mainloop()
    