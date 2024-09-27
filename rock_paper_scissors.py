import random
import tkinter as tk

def play_round(player_choice):
    choices = ['Rock', 'Paper', 'Scissors']
    computer_choice = random.choice(choices)
    result = determine_winner(player_choice, computer_choice)
    update_score(result)
    update_result_icon(result)
    check_for_winner()

def determine_winner(player, computer):
    if player == computer:
        return 'Draw'
    elif (player == 'Rock' and computer == 'Scissors') or \
         (player == 'Scissors' and computer == 'Paper') or \
         (player == 'Paper' and computer == 'Rock'):
        return 'Player'
    else:
        return 'Computer'

def update_score(result):
    global player_score, computer_score
    if result == 'Player':
        player_score += 1
    elif result == 'Computer':
        computer_score += 1
    update_score_labels()

def update_score_labels():
    player_score_label.config(text=f"Player Score: {player_score}")
    computer_score_label.config(text=f"Computer Score: {computer_score}")

def update_result_icon(result):
    if result == 'Player':
        result_label.config(text="✓", fg="green", font=('Arial', 18))
    elif result == 'Computer':
        result_label.config(text="✗", fg="red", font=('Arial', 18))
    else:
        result_label.config(text="-", fg="orange", font=('Arial', 18))

def check_for_winner():
    if player_score == 10:
        result_label.config(text="Well done!", fg="green")
        hide_game_buttons()
        show_end_buttons()
    elif computer_score == 10:
        result_label.config(text="Hadi try again!", fg="red")
        hide_game_buttons()
        show_end_buttons()
    else:
        return

def hide_game_buttons():
    rock_button.grid_remove()
    paper_button.grid_remove()
    scissors_button.grid_remove()

def show_end_buttons():
    play_again_button.grid(row=0, column=0, padx=5)
    exit_button.grid(row=0, column=1, padx=5)

def reset_game():
    global player_score, computer_score
    player_score, computer_score = 0, 0
    update_score_labels()
    result_label.config(text="Hadi!", font=('Arial', 18), fg="darkblue")
    play_again_button.grid_remove()
    exit_button.grid_remove()
    show_game_buttons()

def show_game_buttons():
    rock_button.grid(row=0, column=0, padx=5)
    paper_button.grid(row=0, column=1, padx=5)
    scissors_button.grid(row=0, column=2, padx=5)

def exit_game():
    root.quit()

root = tk.Tk()
root.title("Rock-Paper-Scissors Game")
root.geometry("400x315") 
root.config(bg="lightblue")

player_score = 0
computer_score = 0

title_label = tk.Label(root, text="Rock-Paper-Scissors", font=('Arial', 20, 'bold'), bg="lightblue")
title_label.pack(pady=10)

player_score_label = tk.Label(root, text="Player Score: 0", font=('Arial', 14), bg="lightblue")
player_score_label.pack(pady=5)

computer_score_label = tk.Label(root, text="Computer Score: 0", font=('Arial', 14), bg="lightblue")
computer_score_label.pack(pady=5)

result_label = tk.Label(root, text="Hadi!", font=('Arial', 18, 'bold'), bg="lightblue", fg="darkblue")
result_label.pack(pady=10)

button_frame = tk.Frame(root, bg="lightblue")
button_frame.pack(pady=25)

rock_button = tk.Button(button_frame, text="Rock", font=('Arial', 14), bg="lightgray", width=10,
                        command=lambda: play_round('Rock'))
rock_button.grid(row=0, column=0, padx=5)

paper_button = tk.Button(button_frame, text="Paper", font=('Arial', 14), bg="lightgray", width=10,
                         command=lambda: play_round('Paper'))
paper_button.grid(row=0, column=1, padx=5)

scissors_button = tk.Button(button_frame, text="Scissors", font=('Arial', 14), bg="lightgray", width=10,
                            command=lambda: play_round('Scissors'))
scissors_button.grid(row=0, column=2, padx=5)

azd_label = tk.Label(button_frame, text="AZD", font=('Arial', 10, 'bold'), bg="lightblue")
azd_label.grid(row=1, column=1, padx=5, pady=10)

end_button_frame = tk.Frame(root, bg="lightblue")
end_button_frame.pack(pady=10)

play_again_button = tk.Button(end_button_frame, text="Play Again", font=('Arial', 14), bg="green", fg="white", command=reset_game)
exit_button = tk.Button(end_button_frame, text="Exit", font=('Arial', 14), bg="black", fg="white", command=exit_game)

root.mainloop()
