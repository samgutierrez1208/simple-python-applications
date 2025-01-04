import tkinter as tk
import random

# File containing city-country data
DATA_FILE = "cities_and_countries.txt"

# Load city-country data from file
def load_city_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = [line.strip().split(", ") for line in file.readlines() if line.strip()]
            return data
    except FileNotFoundError:
        raise Exception(f"Data file '{DATA_FILE}' not found.")

# Load city data
city_data = load_city_data()

# Ensure city_data is not empty
if len(city_data) < 1:
    raise ValueError("City data is empty. Ensure the data file is correctly formatted.")

# Game variables
score = 0
questions = []
current_question_index = 0
num_questions = 10

# Initialize questions
def initialize_questions():
    global questions
    if num_questions > len(city_data):
        raise ValueError("Number of questions exceeds available city data.")
    questions = random.sample(city_data, num_questions)

# GUI setup
def start_game():
    global score, current_question_index
    if not city_data:
        status_label.config(text="No city data available. Check the data file.")
        for btn in answer_buttons:
            btn.config(state="disabled")
        return
    score = 0
    current_question_index = 0
    initialize_questions()
    status_label.config(text="")  # Clear status label on game start
    load_question()

def load_question():
    global current_question_index
    if current_question_index >= len(questions):
        status_label.config(text=f"Game Over! Final Score: {score}/{num_questions}")
        for btn in answer_buttons:
            btn.config(state="disabled")
        return

    city, correct_country = questions[current_question_index]
    question_label.config(text=f"Which country does {city} belong to?")

    other_countries = list({c for _, c in city_data if c != correct_country})
    options = [correct_country] + random.sample(other_countries, min(3, len(other_countries)))
    random.shuffle(options)

    for i, btn in enumerate(answer_buttons):
        btn.config(text=options[i], command=lambda c=options[i]: check_answer(c), state="normal")

def check_answer(selected_country):
    global score, current_question_index

    city, correct_country = questions[current_question_index]

    if selected_country == correct_country:
        score += 1
        status_label.config(text=f"Correct! Score: {score}/{num_questions}")
    else:
        status_label.config(text=f"Wrong! {city} belongs to {correct_country}. Score: {score}/{num_questions}")

    current_question_index += 1
    load_question()

def reset_game():
    global score, current_question_index, questions
    score = 0
    current_question_index = 0
    questions = []
    status_label.config(text="")  # Clear the status label
    start_game()

def quit_game():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("City-Country Quiz")
root.geometry("600x400")
root.config(bg="#f0f8ff")

# Title Label
title_label = tk.Label(root, text="City-Country Quiz", font=("Arial", 24, "bold"), bg="#f0f8ff", fg="#4682b4")
title_label.pack(pady=10)

# Question Label
question_label = tk.Label(root, text="", font=("Arial", 18), bg="#f0f8ff", fg="#333")
question_label.pack(pady=20)

# Answer Buttons
answer_buttons = []
answers_frame = tk.Frame(root, bg="#f0f8ff")
answers_frame.pack()

for i in range(2):
    row_frame = tk.Frame(answers_frame, bg="#f0f8ff")
    row_frame.pack(side="top", pady=5)
    for _ in range(2):
        btn = tk.Button(row_frame, text="", font=("Arial", 16), bg="#e0ffff", fg="#000", width=15)
        btn.pack(side="left", padx=10)
        answer_buttons.append(btn)

# Status Label
status_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f8ff", fg="#333")
status_label.pack(pady=10)

# Footer Frame
footer_frame = tk.Frame(root, bg="#f0f8ff")
footer_frame.pack(side="bottom", pady=10)

reset_button = tk.Button(footer_frame, text="Reset", font=("Arial", 12), bg="#90ee90", command=reset_game)
reset_button.pack(side="left", padx=10)

quit_button = tk.Button(footer_frame, text="Quit", font=("Arial", 12), bg="#ff6347", command=quit_game)
quit_button.pack(side="left", padx=10)

footer_label = tk.Label(footer_frame, text="AZD", font=("Arial", 10), bg="#f0f8ff", fg="#4682b4")
footer_label.pack(side="right", padx=10)

# Start the game
start_game()

# Main loop
root.mainloop()
