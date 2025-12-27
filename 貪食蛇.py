import tkinter as tk
import random

WIDTH = 400
HEIGHT = 400
GRID = 20

SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BG_COLOR = "black"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("貪食蛇 (Tkinter)")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        self.restart_button = None   # 先預留按鈕

        self.start_game()

        self.root.bind("<KeyPress>", self.change_direction)

    # -----------------
    # 初始化 / 重新開始
    # -----------------
    def start_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.game_running = True
        self.canvas.delete("all")

        # 如果有舊的按鈕就移除
        if self.restart_button:
            self.restart_button.destroy()
            self.restart_button = None

        self.update()

    def create_food(self):
        while True:
            x = random.randrange(0, WIDTH, GRID)
            y = random.randrange(0, HEIGHT, GRID)
            if (x, y) not in self.snake:
                return (x, y)

    def draw(self):
        self.canvas.delete("all")

        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + GRID, y + GRID,
                fill=SNAKE_COLOR
            )

        fx, fy = self.food
        self.canvas.create_oval(
            fx, fy, fx + GRID, fy + GRID,
            fill=FOOD_COLOR
        )

    def change_direction(self, event):
        key = event.keysym
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

        if key in opposites and opposites[key] != self.direction:
            self.direction = key

    def move(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= GRID
        elif self.direction == "Down":
            head_y += GRID
        elif self.direction == "Left":
            head_x -= GRID
        elif self.direction == "Right":
            head_x += GRID

        new_head = (head_x, head_y)

        # 撞牆
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            self.game_over()
            return

        # 撞到自己
        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.create_food()
        else:
            self.snake.pop()

    def update(self):
        if self.game_running:
            self.move()
            self.draw()
            self.root.after(120, self.update)

    # -----------------
    # Game Over + 重新開始按鈕
    # -----------------
    def game_over(self):
        self.game_running = False

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 20,
            text="Game Over",
            fill="white",
            font=("Helvetica", 24)
        )

        # 建立重新開始按鈕
        self.restart_button = tk.Button(
            self.root,
            text="重新開始",
            command=self.start_game
        )
        self.restart_button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
