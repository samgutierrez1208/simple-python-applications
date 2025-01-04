import tkinter as tk
import random

GAME_WIDTH = 600
GAME_HEIGHT = 400
SNAKE_SIZE = 20
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
TEXT_COLOR = "#FFFFFF"
BUTTON_COLOR = "#007BFF"
BUTTON_TEXT_COLOR = "#FFFFFF"
SCORE_FONT = ("Helvetica", 12)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game - AZD")
        self.difficulty = None
        self.target_score = 0

        self.main_menu()

    def main_menu(self):
        self.clear_window()

        self.menu_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.menu_frame.pack_propagate(0)
        self.menu_frame.pack()

        self.title_label = tk.Label(self.menu_frame, text="Snake Game", font=("Helvetica", 24, "bold"), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        self.title_label.pack(pady=40)

        self.easy_button = tk.Button(self.menu_frame, text="Easy", command=lambda: self.start_game("Easy"), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Helvetica", 14), padx=20, pady=10)
        self.easy_button.pack(pady=10)

        self.medium_button = tk.Button(self.menu_frame, text="Medium", command=lambda: self.start_game("Medium"), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Helvetica", 14), padx=20, pady=10)
        self.medium_button.pack(pady=10)

        self.hard_button = tk.Button(self.menu_frame, text="Hard", command=lambda: self.start_game("Hard"), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Helvetica", 14), padx=20, pady=10)
        self.hard_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self, difficulty):
        self.clear_window()
        self.difficulty = difficulty

        if difficulty == "Easy":
            self.target_score = 10
        elif difficulty == "Medium":
            self.target_score = 20
        elif difficulty == "Hard":
            self.target_score = 30

        self.frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.canvas.pack()

        self.button_frame = tk.Frame(self.frame, bg=BACKGROUND_COLOR)
        self.button_frame.pack(pady=10)

        self.restart_button = tk.Button(self.button_frame, text="Restart", command=self.restart_game, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Helvetica", 14), padx=10, pady=5)
        self.restart_button.pack(side=tk.LEFT, padx=20)

        self.menu_button = tk.Button(self.button_frame, text="Back to Menu", command=self.main_menu, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Helvetica", 14), padx=10, pady=5)
        self.menu_button.pack(side=tk.LEFT, padx=20)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.root.quit, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Helvetica", 14), padx=10, pady=5)
        self.exit_button.pack(side=tk.LEFT, padx=20)

        self.score_label = tk.Label(self.frame, text="Score: 0", font=SCORE_FONT, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        self.score_label.place(x=10, y=10)

        self.snake = None
        self.food = None
        self.score = 0
        self.direction = "Right"
        self.is_running = False
        self.end_message = None

        self.root.bind("<KeyPress>", self.change_direction)
        self.restart_game()

    def restart_game(self):
        self.canvas.delete(tk.ALL)
        if self.end_message:
            self.end_message.destroy()
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.is_running = True
        self.score = 0
        self.update_score()
        self.create_food()
        self.move_snake()

    def create_food(self):
        x = random.randint(0, (GAME_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (GAME_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        self.food = (x, y)
        self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=FOOD_COLOR)

    def change_direction(self, event):
        if event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"

    def move_snake(self):
        if not self.is_running:
            return

        head_x, head_y = self.snake[0]

        if self.direction == "Left":
            head_x -= SNAKE_SIZE
        elif self.direction == "Right":
            head_x += SNAKE_SIZE
        elif self.direction == "Up":
            head_y -= SNAKE_SIZE
        elif self.direction == "Down":
            head_y += SNAKE_SIZE

        if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
            self.end_game("You hit the wall!")
            return

        if (head_x, head_y) in self.snake:
            self.end_game("You ran into yourself!")
            return

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.create_food()
            self.score += 1
            self.update_score()

            if self.score >= self.target_score:
                self.end_game(f"Congratulations! You reached {self.target_score} points!")
                return

        self.canvas.delete(tk.ALL)
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + SNAKE_SIZE, segment[1] + SNAKE_SIZE, fill=SNAKE_COLOR)

        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + SNAKE_SIZE, self.food[1] + SNAKE_SIZE, fill=FOOD_COLOR)

        self.root.after(100, self.move_snake)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def end_game(self, message):
        self.is_running = False
        self.canvas.create_rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, fill="gray", stipple="gray12")
        self.end_message = tk.Label(self.canvas, text=message, fg="red", bg="gray", font=("Helvetica", 24, "bold"))
        self.end_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
