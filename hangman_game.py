import tkinter as tk
from tkinter import StringVar
import random

max_attempts = 6

hangman_stages = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ========="""
]

def fetch_random_word_from_file():
    try:
        with open("1000_words.txt", "r") as file:
            words = file.readlines()
            return random.choice(words).strip().upper()
    except FileNotFoundError:
        # Eğer dosya bulunamazsa yedek kelimeler
        return random.choice(['PYTHON', 'DEVELOPER', 'ADVANCED', 'PROJECT', 'GUI']).upper()

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Hangman Game")
        self.word = fetch_random_word_from_file()
        self.attempts_left = max_attempts
        self.correct_letters = ['_' for _ in self.word]
        self.guessed_letters = set()

        self.setup_ui()

    def setup_ui(self):
        self.title_label = tk.Label(self.root, text="HANGMAN GAME", font=("Arial", 20, "bold"), fg="blue")
        self.title_label.pack(pady=10)

        self.hangman_display = StringVar()
        self.hangman_display.set(hangman_stages[0])
        self.hangman_label = tk.Label(self.root, textvariable=self.hangman_display, font=("Courier", 24), fg="black", justify="center")
        self.hangman_label.pack(pady=10, anchor="center")

        self.word_display = StringVar()
        self.word_display.set(" ".join(self.correct_letters))
        self.word_label = tk.Label(self.root, textvariable=self.word_display, font=("Arial", 24), fg="green")
        self.word_label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 18), fg='gray')
        self.entry.insert(0, "Enter a letter")
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.add_placeholder)
        self.entry.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.guess_button = tk.Button(self.button_frame, text="Guess", command=self.make_guess, font=("Arial", 14), bg="lightblue")
        self.guess_button.pack(side="left", padx=10)

        self.try_again_button = tk.Button(self.button_frame, text="Try Again", command=self.reset_game, font=("Arial", 14), bg="lightgray", state="disabled")
        self.try_again_button.pack(side="left", padx=10)

        self.button_frame.pack(pady=10)

        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {self.attempts_left}", font=("Arial", 14), fg="red")
        self.attempts_label.pack(pady=10)

        self.message_display = StringVar()
        self.message_display.set("")
        self.message_label = tk.Label(self.root, textvariable=self.message_display, font=("Arial", 12), fg="purple")
        self.message_label.pack(pady=10)

        self.signature_label = tk.Label(self.root, text="AZD", font=("Arial", 10), fg="gray")
        self.signature_label.pack(side="bottom")

    def clear_placeholder(self, event):
        if self.entry.get() == "Enter a letter":
            self.entry.delete(0, "end")
            self.entry.config(fg="black")

    def add_placeholder(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, "Enter a letter")
            self.entry.config(fg="gray")

    def make_guess(self):
        guess = self.entry.get().upper()
        self.entry.delete(0, 'end')

        if not guess.isalpha() or len(guess) != 1:
            self.message_display.set("Please enter a valid single letter.")
            return

        if guess in self.guessed_letters:
            self.message_display.set("You already guessed that letter.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            self.update_correct_letters(guess)
            if "_" not in self.correct_letters:
                self.message_display.set("Congratulations! You've won!")
                self.guess_button.config(state="disabled")
                self.try_again_button.config(state="normal")
        else:
            self.attempts_left -= 1
            self.update_hangman_drawing()
            self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
            if self.attempts_left == 0:
                self.message_display.set(f"Game Over! The word was {self.word}.")
                self.guess_button.config(state="disabled")
                self.try_again_button.config(state="normal")

        self.word_display.set(" ".join(self.correct_letters))

    def update_hangman_drawing(self):
        self.hangman_display.set(hangman_stages[max_attempts - self.attempts_left])

    def update_correct_letters(self, guess):
        for i, letter in enumerate(self.word):
            if letter == guess:
                self.correct_letters[i] = guess

    def reset_game(self):
        self.word = fetch_random_word_from_file()
        self.attempts_left = max_attempts
        self.correct_letters = ['_' for _ in self.word]
        self.guessed_letters.clear()

        self.word_display.set(" ".join(self.correct_letters))
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.hangman_display.set(hangman_stages[0])
        self.message_display.set("")
        self.guess_button.config(state="normal")
        self.try_again_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x700")
    game = HangmanGame(root)
    root.mainloop()
