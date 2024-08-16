import tkinter as tk
from tkinter import messagebox
import random
import time

class Minesweeper:
    def __init__(self, master, size=10, mines=10):
        self.master = master
        self.size = size
        self.mines = mines
        self.buttons = {}
        self.grid = []
        self.is_game_over = False
        self.start_time = None
        self.timer_label = None

        self.create_widgets()
        self.place_mines()
        self.calculate_numbers()
        self.update_timer()

    def create_widgets(self):
        top_frame = tk.Frame(self.master)
        top_frame.pack()

        self.timer_label = tk.Label(top_frame, text="Time: 0")
        self.timer_label.pack(side=tk.LEFT)

        restart_button = tk.Button(top_frame, text="重新开始", command=self.restart_game)
        restart_button.pack(side=tk.RIGHT)

        difficulty_frame = tk.Frame(top_frame)
        difficulty_frame.pack(side=tk.RIGHT)

        self.difficulty = tk.IntVar(value=10)
        tk.Radiobutton(difficulty_frame, text="简单", variable=self.difficulty, value=10).pack(side=tk.LEFT)
        tk.Radiobutton(difficulty_frame, text="普通", variable=self.difficulty, value=20).pack(side=tk.LEFT)
        tk.Radiobutton(difficulty_frame, text="困难", variable=self.difficulty, value=30).pack(side=tk.LEFT)

        grid_frame = tk.Frame(self.master)
        grid_frame.pack()

        for x in range(self.size):
            row = []
            for y in range(self.size):
                btn = tk.Button(grid_frame, width=2, command=lambda x=x, y=y: self.on_click(x, y))
                btn.bind('<Button-3>', lambda event, x=x, y=y: self.on_right_click(x, y))
                btn.grid(row=x, column=y)
                row.append(btn)
                self.buttons[(x, y)] = btn
            self.grid.append(row)

    def place_mines(self):
        count = 0
        while count < self.mines:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.grid[x][y] != 'M':
                self.grid[x][y] = 'M'
                count += 1

    def calculate_numbers(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] != 'M':
                    self.grid[x][y] = self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x, y):
        count = 0
        for i in range(max(0, x-1), min(self.size, x+2)):
            for j in range(max(0, y-1), min(self.size, y+2)):
                if self.grid[i][j] == 'M':
                    count += 1
        return count

    def on_click(self, x, y):
        if self.is_game_over or self.buttons[(x, y)]['text'] == 'F':
            return
        if self.start_time is None:
            self.start_time = time.time()

        if self.grid[x][y] == 'M':
            self.buttons[(x, y)]['text'] = 'M'
            self.buttons[(x, y)]['bg'] = 'red'
            self.game_over(False)
        elif self.grid[x][y] == 0:
            self.reveal_blank(x, y)
        else:
            self.buttons[(x, y)]['text'] = self.grid[x][y]
            self.buttons[(x, y)]['state'] = 'disabled'
        self.check_win()

    def on_right_click(self, x, y):
        if self.is_game_over or self.buttons[(x, y)]['state'] == 'disabled':
            return
        current_text = self.buttons[(x, y)]['text']
        if current_text == '':
            self.buttons[(x, y)]['text'] = 'F'
        elif current_text == 'F':
            self.buttons[(x, y)]['text'] = ''

    def reveal_blank(self, x, y):
        if self.buttons[(x, y)]['state'] == 'disabled':
            return
        self.buttons[(x, y)]['text'] = ''
        self.buttons[(x, y)]['state'] = 'disabled'
        if self.grid[x][y] == 0:
            for i in range(max(0, x-1), min(self.size, x+2)):
                for j in range(max(0, y-1), min(self.size, y+2)):
                    if (i, j) != (x, y):
                        self.on_click(i, j)

    def check_win(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] != 'M' and self.buttons[(x, y)]['state'] != 'disabled':
                    return
        self.game_over(True)

    def game_over(self, won):
        self.is_game_over = True
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] == 'M':
                    self.buttons[(x, y)]['text'] = 'M'
                    self.buttons[(x, y)]['bg'] = 'red' if not won else 'green'
        if won:
            messagebox.showinfo("游戏结束", "恭喜你，你赢了！")
        else:
            messagebox.showinfo("游戏结束", "很遗憾，你踩到了地雷！")

    def restart_game(self):
        self.master.destroy()
        root = tk.Tk()
        size = self.difficulty.get()
        Minesweeper(root, size=size, mines=size*size//6)
        root.mainloop()

    def update_timer(self):
        if self.start_time and not self.is_game_over:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}")
        self.master.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")

    game = Minesweeper(root, size=10, mines=10)

    root.mainloop()
