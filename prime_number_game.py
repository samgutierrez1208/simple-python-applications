import tkinter as tk
import random

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_question():
    options = []
    prime_number = random.randint(2, 100)
    while not is_prime(prime_number):
        prime_number = random.randint(2, 100)
    
    options.append(prime_number)
    while len(options) < 5:
        num = random.randint(2, 100)
        if num not in options:
            options.append(num)
    
    random.shuffle(options)
    return prime_number, options

class PrimeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Prime Number Finding Game")
        self.root.geometry("700x330")
        self.root.configure(bg="#f0f0f0")
        
        self.score = 0
        self.rounds = 0
        self.max_rounds = 10
        
        self.question_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.question_frame.pack(pady=20)
        
        self.question_label = tk.Label(self.question_frame, text="Find the Prime Number", font=("Helvetica", 16), bg="#f0f0f0")
        self.question_label.pack(pady=10)

        self.azd_label = tk.Label(self.question_frame, text="AZD", font=("Helvetica", 10, "bold"), bg="#f0f0f0")
        self.azd_label.pack()

        self.buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.buttons_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(5):
            btn = tk.Button(self.buttons_frame, text="", width=10, height=2, bg="#d1d1e0", 
                            fg="#000000", font=("Helvetica", 14), 
                            command=lambda idx=i: self.check_answer(idx))
            btn.grid(row=0, column=i, padx=5)
            self.buttons.append(btn)
        
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f0f0f0")
        self.result_label.pack(pady=10)

        self.status_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.status_frame.pack(pady=5)

        self.score_label = tk.Label(self.status_frame, text=f"Score: {self.score}", font=("Helvetica", 14), bg="#f0f0f0")
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.round_label = tk.Label(self.status_frame, text=f"Remaining Rounds: {self.max_rounds - self.rounds}", font=("Helvetica", 14), bg="#f0f0f0")
        self.round_label.pack(side=tk.LEFT, padx=10)
        
        self.action_frame = tk.Frame(self.root, bg="#f0f0f0")  
        self.reset_button = tk.Button(self.action_frame, text="Play Again", command=self.reset_game, state=tk.DISABLED, bg="#90EE90", width=15, height=2)
        self.exit_button = tk.Button(self.action_frame, text="Exit", command=self.root.quit, state=tk.DISABLED, bg="#FF6347", width=15, height=2)
        
        self.correct_prime = None
        self.start_game()

    def start_game(self):
        self.score = 0
        self.rounds = 0
        self.result_label.config(text="")
        self.update_status()
        self.status_frame.pack(pady=5)
        self.reset_button.pack_forget()
        self.exit_button.pack_forget()
        self.next_question()
        
    def next_question(self):
        self.rounds += 1
        if self.rounds > self.max_rounds:
            self.end_game()
            return
        
        self.correct_prime, options = generate_question()
        
        for i, btn in enumerate(self.buttons):
            btn.config(text=str(options[i]), state=tk.NORMAL)
        
        self.result_label.config(text="")
        self.update_status()
    
    def check_answer(self, idx):
        selected_number = int(self.buttons[idx].cget("text"))
        if selected_number == self.correct_prime:
            self.result_label.config(text="Correct!", fg="green")
            self.score += 1
        else:
            self.result_label.config(text=f"Wrong! Correct answer: {self.correct_prime}", fg="red")
        
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        
        if self.rounds < self.max_rounds:
            self.root.after(1000, self.next_question)
        else:
            self.end_game()
    
    def update_status(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.round_label.config(text=f"Remaining Rounds: {self.max_rounds - self.rounds}")
    
    def end_game(self):
        result_text = f"Game Over! Your score: {self.score} / {self.max_rounds}"
        self.result_label.config(text=result_text, fg="blue")
        self.status_frame.pack_forget()
        self.reset_button.pack(side=tk.LEFT, padx=20, pady=10)
        self.exit_button.pack(side=tk.RIGHT, padx=20, pady=10)
        self.reset_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)
        self.action_frame.pack(pady=10)
    
    def reset_game(self):
        self.action_frame.pack_forget()
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = PrimeGame(root)
    root.mainloop()
