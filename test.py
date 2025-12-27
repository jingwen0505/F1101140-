import tkinter as tk
import random

# 視窗大小
WIDTH = 400
HEIGHT = 400
GRID = 20   # 每一格大小

# 顏色
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BG_COLOR = "black"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("貪食蛇 (Tkinter)")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        # 初始蛇
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"

        # 產生食物
        self.food = self.create_food()

        # 綁定鍵盤
        self.root.bind("<KeyPress>", self.change_direction)

        # 遊戲開始
        self.game_running = True
        self.update()

    def draw(self):
        self.canvas.delete("all")

        # 畫蛇
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + GRID, y + GRID,
                fill=SNAKE_COLOR
            )

        # 畫食物
        fx, fy = self.food
        self.canvas.create_oval(
            fx, fy, fx + GRID, fy + GRID,
            fill=FOOD_COLOR
        )

    def create_food(self):
        while True:
            x = random.randrange(0, WIDTH, GRID)
            y = random.randrange(0, HEIGHT, GRID)
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, event):
        key = event.keysym

        # 防止直接 180 度轉彎
        opposites = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }

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
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT
        ):
            self.game_over()
            return

        # 撞到自己
        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # 吃到食物
        if new_head == self.food:
            self.food = self.create_food()
        else:
            self.snake.pop()

    def update(self):
        if self.game_running:
            self.move()
            self.draw()
            self.root.after(120, self.update)

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="Game Over",
            fill="white",
            font=("Helvetica", 24)
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
