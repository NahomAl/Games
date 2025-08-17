import tkinter as tk
import random


class Tetris:
    HIGHSCORE_FILE = "tetris_highscore.txt"
    ROWS = 20
    COLS = 10
    CELL = 30
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[0, 1, 0], [1, 1, 1]],  # T
        [[1, 1, 0], [0, 1, 1]],  # S
        [[0, 1, 1], [1, 1, 0]],  # Z
        [[1, 0, 0], [1, 1, 1]],  # J
        [[0, 0, 1], [1, 1, 1]],  # L
    ]
    COLORS = ["#00e0ff", "#ffcc00", "#ff0055",
              "#00ffb0", "#b388ff", "#ffb300", "#00b8d9"]

    def __init__(self, root, show_menu=False):
        self.root = root
        self.root.title("Tetris")
        self.frame = tk.Frame(self.root, bg="#181f2a")
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.score = 0
        self.highscore = self.load_highscore()
        self.root.geometry(f"700x700")
        self.root.configure(bg="#181f2a")
        self.frame.pack_propagate(False)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Main horizontal layout
        self.main_area = tk.Frame(self.frame, bg="#181f2a")
        self.main_area.pack(expand=True)
        # Board on the left
        self.board_area = tk.Frame(self.main_area, bg="#181f2a")
        self.board_area.pack(side=tk.LEFT, padx=(30, 10), pady=30)
        self.canvas = tk.Canvas(
            self.board_area, width=self.COLS*self.CELL, height=self.ROWS*self.CELL, bg="#232b38",
            highlightthickness=3, highlightbackground="#eeeeee")
        self.canvas.pack()
        # Side area on the right
        self.side_area = tk.Frame(self.main_area, bg="#181f2a")
        self.side_area.pack(side=tk.LEFT, padx=(10, 30), pady=30, anchor="n")
        self.score_label = tk.Label(self.side_area, text=f"Score: {self.score}", font=(
            "Arial Rounded MT Bold", 22, "bold"), bg="#181f2a", fg="#00e0ff")
        self.score_label.pack(pady=(0, 8))
        self.highscore_label = tk.Label(self.side_area, text=f"High Score: {self.highscore}", font=(
            "Arial Rounded MT Bold", 16, "bold"), bg="#181f2a", fg="#ffcc00")
        self.highscore_label.pack(pady=(0, 18))
        self.next_label = tk.Label(self.side_area, text="Next:", font=(
            "Arial Rounded MT Bold", 16, "bold"), bg="#181f2a", fg="#00e0ff")
        self.next_label.pack()
        self.next_canvas = tk.Canvas(self.side_area, width=6*self.CELL, height=4*self.CELL,
                                     bg="#232b38", highlightthickness=2, highlightbackground="#00e0ff")
        self.next_canvas.pack(pady=8)

        # Add Pause, Restart, and Main Menu buttons
        btn_frame = tk.Frame(self.frame, bg="#181f2a")
        btn_frame.pack(pady=(10, 30))
        pause_btn = tk.Button(btn_frame, text="Pause", font=("Arial Rounded MT Bold", 18, "bold"), bg="#ffcc00", fg="#181f2a",
                              width=10, height=2, command=self.toggle_pause, cursor='hand2', bd=0, activebackground="#ffe066", activeforeground="#181f2a", relief=tk.FLAT)
        pause_btn.pack(side=tk.LEFT, padx=12)
        restart_btn = tk.Button(btn_frame, text="Restart", font=("Arial Rounded MT Bold", 18, "bold"), bg="#00e0ff", fg="#181f2a",
                                width=10, height=2, command=self.restart, cursor='hand2', bd=0, activebackground="#00b8d9", activeforeground="#fff", relief=tk.FLAT)
        restart_btn.pack(side=tk.LEFT, padx=12)
        menu_btn = tk.Button(btn_frame, text="Main Menu", font=("Arial Rounded MT Bold", 18, "bold"), bg="#232b38", fg="#eeeeee",
                             width=10, height=2, command=self.back_to_menu, cursor='hand2', bd=0, activebackground="#393e46", activeforeground="#00e0ff", relief=tk.FLAT)
        menu_btn.pack(side=tk.LEFT, padx=12)

        self.board = [[0]*self.COLS for _ in range(self.ROWS)]
        self.shape = None
        self.color = None
        self.x = 0
        self.y = 0
        self.next_shape = random.choice(self.SHAPES)
        self.next_color = random.choice(self.COLORS)
        self.new_piece()
        self.root.bind('<Key>', self.on_key)
        self.running = True

    def toggle_pause(self):
        if not hasattr(self, 'paused'):
            self.paused = False
        self.paused = not getattr(self, 'paused', False)
        if self.paused:
            self.running_before_pause = self.running
            self.running = False
            self.canvas.create_text(self.COLS*self.CELL//2, self.ROWS*self.CELL//2, text="Paused",
                                    fill="#ffcc00", font=("Arial Rounded MT Bold", 32, "bold"), anchor="center")
        else:
            self.running = getattr(self, 'running_before_pause', True)
            self.draw()

        self.drop()

    def restart(self):
        self.frame.destroy()
        Tetris(self.root, show_menu=True)

    def back_to_menu(self):
        self.frame.destroy()
        from gui import MainMenu
        MainMenu(self.root)

    def new_piece(self):
        self.shape = self.next_shape
        self.color = self.next_color
        self.next_shape = random.choice(self.SHAPES)
        self.next_color = random.choice(self.COLORS)
        self.x = self.COLS // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.draw_next()
        if self.collision(self.x, self.y, self.shape):
            self.running = False
            self.canvas.create_text(self.COLS*self.CELL//2, self.ROWS*self.CELL//2, text="Game Over",
                                    fill="#ff1744", font=("Arial Rounded MT Bold", 32, "bold"), anchor="center")
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore(self.highscore)
                self.highscore_label.config(
                    text=f"High Score: {self.highscore}")
                self.canvas.create_text(self.COLS*self.CELL//2, self.ROWS*self.CELL//2+40, text="New High Score!",
                                        fill="#ffcc00", font=("Arial Rounded MT Bold", 20, "bold"), anchor="center")

    def draw_next(self):
        self.next_canvas.delete("all")
        for i, row in enumerate(self.next_shape):
            for j, cell in enumerate(row):
                if cell:
                    self.next_canvas.create_rectangle(
                        (j+1)*self.CELL, (i+1)*self.CELL,
                        (j+2)*self.CELL, (i+2)*self.CELL,
                        fill=self.next_color, outline="#eeeeee")

    def collision(self, x, y, shape):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    nx, ny = x + j, y + i
                    if nx < 0 or nx >= self.COLS or ny >= self.ROWS or (ny >= 0 and self.board[ny][nx]):
                        return True
        return False

    def merge(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.board[self.y + i][self.x + j] = self.color

    def clear_lines(self):
        new_board = [row for row in self.board if any(
            cell == 0 for cell in row)]
        lines_cleared = self.ROWS - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0]*self.COLS)
        self.board = new_board
        if lines_cleared > 0:
            self.score += lines_cleared * 100
            self.score_label.config(text=f"Score: {self.score}")
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore(self.highscore)
                self.highscore_label.config(
                    text=f"High Score: {self.highscore}")

    def load_highscore(self):
        try:
            with open(self.HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_highscore(self, score):
        try:
            with open(self.HIGHSCORE_FILE, "w") as f:
                f.write(str(score))
        except Exception:
            pass

    def rotate(self):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        if not self.collision(self.x, self.y, rotated):
            self.shape = rotated

    def move(self, dx):
        if not self.collision(self.x + dx, self.y, self.shape):
            self.x += dx
            self.draw()

    def drop(self):
        if not self.running:
            return
        if not self.collision(self.x, self.y + 1, self.shape):
            self.y += 1
        else:
            self.merge()
            self.clear_lines()
            self.new_piece()
        self.draw()
        if self.running:
            self.root.after(300, self.drop)

    def on_key(self, event):
        # Pause/Resume with P or Escape
        if event.keysym.lower() in ['p', 'escape']:
            self.toggle_pause()
            return
        if not self.running or getattr(self, 'paused', False):
            return
        if event.keysym == 'Left':
            self.move(-1)
        elif event.keysym == 'Right':
            self.move(1)
        elif event.keysym == 'Down':
            if not self.collision(self.x, self.y + 1, self.shape):
                self.y += 1
                self.draw()
        elif event.keysym == 'Up':
            self.rotate()
            self.draw()
        elif event.keysym == 'space':
            while not self.collision(self.x, self.y + 1, self.shape):
                self.y += 1
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        # Draw board
        for i in range(self.ROWS):
            for j in range(self.COLS):
                color = self.board[i][j]
                if color:
                    self.canvas.create_rectangle(
                        j*self.CELL, i*self.CELL,
                        (j+1)*self.CELL, (i+1)*self.CELL,
                        fill=color, outline="#222831")
        # Draw current piece
        if self.running:
            for i, row in enumerate(self.shape):
                for j, cell in enumerate(row):
                    if cell:
                        self.canvas.create_rectangle(
                            (self.x+j)*self.CELL, (self.y+i)*self.CELL,
                            (self.x+j+1)*self.CELL, (self.y+i+1)*self.CELL,
                            fill=self.color, outline="#eeeeee")
        else:
            self.canvas.create_text(self.COLS*self.CELL//2, self.ROWS*self.CELL//2, text="Game Over",
                                    fill="#ff1744", font=("Arial Rounded MT Bold", 32, "bold"), anchor="center")
            if self.score >= self.highscore:
                self.canvas.create_text(self.COLS*self.CELL//2, self.ROWS*self.CELL//2+40, text="New High Score!",
                                        fill="#ffcc00", font=("Arial Rounded MT Bold", 20, "bold"), anchor="center")
