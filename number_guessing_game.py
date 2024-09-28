import tkinter as tk
import random

class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("500x300")
        self.root.config(bg="lightblue")

        self.secret_number = None
        self.tries_left = None
        self.difficulty_selected = False

        self.title_label = tk.Label(root, text="Number Guessing Game", font=("Helvetica", 26, "bold"), bg="lightblue", fg="black")
        self.title_label.pack(pady=10)

        # Create a fixed size frame for status text to prevent layout changes
        self.status_frame = tk.Frame(root, bg="lightblue")
        self.status_frame.pack(pady=5)
        self.info_panel = tk.Label(self.status_frame, text="Select a difficulty to start!", font=("Helvetica", 14), bg="lightblue", fg="black", width=50)
        self.info_panel.pack()

        self.entry_frame = tk.Frame(root, bg="lightblue")
        self.entry_frame.pack(pady=10)

        self.guess_entry = tk.Entry(self.entry_frame, font=("Helvetica", 16), width=5)
        self.guess_entry.grid(row=0, column=0, padx=5)

        self.guess_button = tk.Button(self.entry_frame, text="Guess", font=("Helvetica", 14), command=self.make_guess, state=tk.DISABLED)
        self.guess_button.grid(row=0, column=1, padx=5)

        self.tries_label = tk.Label(root, text="", font=("Helvetica", 14), bg="lightblue", fg="black")
        self.tries_label.pack(pady=5)

        self.difficulty_frame = tk.Frame(root, bg="lightblue")
        self.difficulty_frame.pack(pady=10)

        self.easy_button = tk.Button(self.difficulty_frame, text="Easy (1-10)", font=("Helvetica", 14), bg="white", fg="black", 
                                     command=lambda: self.start_game(10, 5, self.easy_button))
        self.easy_button.grid(row=0, column=0, padx=10)

        self.medium_button = tk.Button(self.difficulty_frame, text="Medium (1-50)", font=("Helvetica", 14), bg="white", fg="black", 
                                       command=lambda: self.start_game(50, 7, self.medium_button))
        self.medium_button.grid(row=0, column=1, padx=10)

        self.hard_button = tk.Button(self.difficulty_frame, text="Hard (1-100)", font=("Helvetica", 14), bg="white", fg="black", 
                                     command=lambda: self.start_game(100, 10, self.hard_button))
        self.hard_button.grid(row=0, column=2, padx=10)

        self.reset_button = tk.Button(self.difficulty_frame, text="✘", font=("Helvetica", 16), bg="red", fg="white", command=self.reset_game, state=tk.DISABLED)
        self.reset_button.grid(row=0, column=3, padx=10)

        self.footer_label = tk.Label(root, text="AZD", font=("Helvetica", 12, "bold"), bg="lightblue", fg="black")
        self.footer_label.pack(pady=5)

    def start_game(self, max_number, tries, selected_button):
        if not self.difficulty_selected:
            self.secret_number = random.randint(1, max_number)
            self.tries_left = tries
            self.difficulty_selected = True

            selected_button.config(bg="lightgreen", state=tk.DISABLED)
            self.easy_button.config(state=tk.DISABLED)
            self.medium_button.config(state=tk.DISABLED)
            self.hard_button.config(state=tk.DISABLED)

            self.info_panel.config(text=f"Number between 1 and {max_number}. Good Luck!!!")
            self.update_tries_label()

            self.guess_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

    def make_guess(self):
        if self.secret_number is None:
            self.info_panel.config(text="Select a difficulty level first!", fg="red")
            return

        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.info_panel.config(text="Please enter a valid number!", fg="red")
            return

        if guess == self.secret_number:
            self.info_panel.config(text=f"You won! Correct: {guess}.", fg="green")
            self.end_game("You won!")
        elif guess < self.secret_number:
            self.info_panel.config(text="Too low! Try again.", fg="orange")
        else:
            self.info_panel.config(text="Too high! Try again.", fg="orange")

        self.tries_left -= 1
        self.update_tries_label()

        if self.tries_left == 0:
            self.info_panel.config(text=f"Game over! Correct: {self.secret_number}.", fg="red")
            self.end_game("You lost!")

    def update_tries_label(self):
        self.tries_label.config(text=f"Tries left: {self.tries_left}")

    def reset_game(self):
        self.secret_number = None
        self.tries_left = None
        self.difficulty_selected = False
        self.guess_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.info_panel.config(text="Select a difficulty for a new game!", fg="black")
        self.tries_label.config(text="")
        self.guess_entry.delete(0, tk.END)

        self.easy_button.config(bg="white", state=tk.NORMAL)
        self.medium_button.config(bg="white", state=tk.NORMAL)
        self.hard_button.config(bg="white", state=tk.NORMAL)

    def end_game(self, result_message):
        self.guess_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.info_panel.config(text=result_message, fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGame(root)
    root.mainloop()
