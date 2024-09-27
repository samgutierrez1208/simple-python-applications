import tkinter as tk
import random

score = 0
attempts = 10
game_active = True

def start_game():
    global random_number, game_active
    random_number = random.randint(1, 100)
    number_label.config(text=str(random_number))
    game_active = True
    even_button.config(text="Even", command=lambda: check_odd_even(True))
    odd_button.config(text="Odd", command=lambda: check_odd_even(False))

def check_odd_even(is_even_guess):
    global score, attempts, game_active
    if attempts <= 0 or not game_active:
        return
    
    is_even = random_number % 2 == 0
    if (is_even and is_even_guess) or (not is_even and not is_even_guess):
        score += 10
        feedback_label.config(text="Correct guess! +10 points", fg="green")
    else:
        score -= 5
        feedback_label.config(text="Wrong guess! -5 points", fg="red")
    
    feedback_label.update_idletasks()
    
    attempts -= 1
    score_label.config(text=f"Score: {score}")
    attempts_label.config(text=f"Remaining Attempts: {attempts}")
    
    if attempts > 0:
        start_game()
    else:
        game_over()

def game_over():
    global game_active
    game_active = False
    if score >= 50:
        feedback_label.config(text=f"Congratulations! You won.", fg="green", font=("Helvetica", 14, "bold"))
    else:
        feedback_label.config(text=f"You lost. Try again...", fg="red", font=("Helvetica", 14, "bold"))
    
    even_button.config(text="Play Again", command=reset_game)
    odd_button.config(text="Exit", command=root.quit)

def reset_game():
    global score, attempts
    score = 0
    attempts = 10
    score_label.config(text=f"Score: {score}")
    attempts_label.config(text=f"Remaining Attempts: {attempts}")
    feedback_label.config(text="Is it Odd or Even? Make a guess!", fg="yellow")  # Reset feedback message
    start_game()

root = tk.Tk()
root.title("Odd-Even Guessing Game")
root.geometry("450x380")
root.resizable(False, False)
root.config(bg="#1e1e1e")

title_label = tk.Label(root, text="Odd or Even? Make a Guess!", font=("Helvetica", 20, "bold"), fg="white", bg="#1e1e1e")
title_label.pack(pady=10)

number_label = tk.Label(root, text="?", font=("Helvetica", 50), fg="white", bg="#1e1e1e")
number_label.pack(pady=10)

feedback_label = tk.Label(root, text="Is it Odd or Even? Make a guess!", font=("Helvetica", 14), fg="yellow", bg="#1e1e1e")  # Yellow color initially
feedback_label.pack(pady=10)

score_label = tk.Label(root, text=f"Score: {score}", font=("Helvetica", 14), fg="white", bg="#1e1e1e")
score_label.pack(pady=5)

attempts_label = tk.Label(root, text=f"Remaining Attempts: {attempts}", font=("Helvetica", 14), fg="white", bg="#1e1e1e")
attempts_label.pack(pady=5)

azd_label = tk.Label(root, text=f"AZD", font=("Helvetica", 10, "bold"), fg="yellow", bg="#1e1e1e")
azd_label.pack(pady=3)

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

even_button = tk.Button(button_frame, text="Even", font=("Helvetica", 14), command=lambda: check_odd_even(True), bg="#007acc", fg="white", width=12)
even_button.grid(row=0, column=0, padx=10)

odd_button = tk.Button(button_frame, text="Odd", font=("Helvetica", 14), command=lambda: check_odd_even(False), bg="#d9534f", fg="white", width=12)
odd_button.grid(row=0, column=1, padx=10)

start_game()

root.mainloop()
