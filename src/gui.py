import random as _random
import random
from game_logic import TicTacToe
from tkinter import messagebox, simpledialog
import tkinter as tk


class MainMenu:
    def start_ttt(self):
        self.frame.destroy()
        TicTacToeGUI(self.root, show_menu=True)

    def start_snake(self):
        import tkinter.simpledialog as sd
        self.frame.destroy()
        level = sd.askstring(
            "Snake Level", "Choose level: Easy, Medium, Hard", initialvalue="Easy")
        if not level:
            level = "Easy"
        level = level.lower()
        if level not in ["easy", "medium", "hard"]:
            level = "easy"
        SnakeGame(self.root, show_menu=True, level=level)

    def __init__(self, root):
        self.root = root
        self.root.title("Game Menu")
        self.root.configure(bg="#181f2a")
        self.root.geometry("900x900")
        self.frame = tk.Frame(self.root, bg="#181f2a")
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        title = tk.Label(self.frame, text="🎮 Welcome! Choose a Game", font=(
            "Arial Rounded MT Bold", 38, "bold"), bg="#181f2a", fg="#00e0ff", pady=30)
        title.pack(pady=(60, 40))
        btn_style = dict(font=("Arial Rounded MT Bold", 28, "bold"), bg="#00e0ff", fg="#181f2a", width=20,
                         height=2, bd=0, relief=tk.RAISED, cursor='hand2', activebackground="#00b8d9", activeforeground="#fff")
        ttt_btn = tk.Button(self.frame, text="Tic-Tac-Toe",
                            command=self.start_ttt, **btn_style)
        ttt_btn.pack(pady=20)
        snake_btn = tk.Button(self.frame, text="Snake 🐍",
                              command=self.start_snake, **btn_style)
        snake_btn.pack(pady=20)
        quit_btn = tk.Button(self.frame, text="Quit", font=("Arial Rounded MT Bold", 22), bg="#232b38", fg="#eeeeee", width=12,
                             height=1, command=self.root.quit, cursor='hand2', activebackground="#393e46", activeforeground="#00e0ff", bd=0)
        quit_btn.pack(pady=(60, 30))


"""
Tic-Tac-Toe GUI using Tkinter.
Handles user interaction, game mode selection, and rendering.
"""


class TicTacToeGUI:
    def __init__(self, root, show_menu=False):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.game = TicTacToe()
        self.mode = '2P'  # '2P' or 'AI'
        self.ai_starts = False
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.score_labels = {}
        self.create_menu()
        self.create_widgets()
        self.choose_mode()
        self.update_status()
        self.show_menu = show_menu

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = self.game.board[i][j]
                self.buttons[i][j]['fg'] = '#eeeeee'
                self.buttons[i][j]['bg'] = '#393e46'
        if hasattr(self.game, 'winner') and self.game.winner:
            combo = self.game.get_winning_combination(self.game.winner)
            if combo:
                for (i, j) in combo:
                    self.buttons[i][j]['bg'] = '#00ffb0'
                    self.buttons[i][j]['fg'] = '#222831'

    def cell_clicked(self, row, col):
        if hasattr(self.game, 'game_over') and self.game.game_over or self.buttons[row][col]['text']:
            return
        if self.mode == 'AI' and getattr(self.game, 'current_player', None) == 'O':
            return
        moved = self.game.make_move(row, col)
        if moved:
            if hasattr(self, 'animate_button'):
                self.animate_button(row, col)
            self.update_board()
            if hasattr(self, 'update_status'):
                self.update_status()
            if self.mode == 'AI' and not getattr(self.game, 'game_over', False):
                self.root.after(300, self.ai_move)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Restart", command=self.restart)
        game_menu.add_command(label="Choose Mode", command=self.choose_mode)
        game_menu.add_separator()
        game_menu.add_command(label="Main Menu", command=self.back_to_menu)
        game_menu.add_command(label="Quit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        self.root.configure(bg="#181f2a")
        frame = tk.Frame(self.root, bg="#181f2a")
        frame.pack(pady=30)
        btn_style = {
            'font': ('Arial Rounded MT Bold', 40, 'bold'),
            'width': 5,
            'height': 2,
            'bg': '#232b38',
            'fg': '#00e0ff',
            'activebackground': '#00e0ff',
            'activeforeground': '#232b38',
            'relief': tk.RAISED,
            'bd': 0,
            'cursor': 'hand2',
        }
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text='', command=lambda r=i,
                                c=j: self.cell_clicked(r, c), **btn_style)
                btn.grid(row=i, column=j, padx=10, pady=10, sticky='nsew')
                self.buttons[i][j] = btn
        for i in range(3):
            frame.grid_rowconfigure(i, weight=1)
            frame.grid_columnconfigure(i, weight=1)
        self.status_label = tk.Label(self.root, text='', font=(
            'Arial Rounded MT Bold', 24, 'bold'), bg="#181f2a", fg="#00e0ff")
        self.status_label.pack(pady=10)
        score_frame = tk.Frame(self.root, bg="#181f2a")
        score_frame.pack()
        self.score_labels['X'] = tk.Label(score_frame, text='X: 0', font=(
            'Arial Rounded MT Bold', 16, 'bold'), bg="#181f2a", fg="#eeeeee")
        self.score_labels['X'].pack(side=tk.LEFT, padx=16)
        self.score_labels['O'] = tk.Label(score_frame, text='O: 0', font=(
            'Arial Rounded MT Bold', 16, 'bold'), bg="#181f2a", fg="#eeeeee")
        self.score_labels['O'].pack(side=tk.LEFT, padx=16)
        self.restart_btn = tk.Button(self.root, text="Restart", font=('Arial Rounded MT Bold', 16, 'bold'), bg="#00e0ff", fg="#181f2a",
                                     activebackground="#232b38", activeforeground="#00e0ff", command=self.restart, relief=tk.RAISED, bd=0, cursor='hand2')
        self.restart_btn.pack(pady=10)

    def restart(self):
        self.game.reset()
        self.update_board()
        self.update_status()
        if self.mode == 'AI' and self.game.current_player == 'O':
            self.root.after(300, self.ai_move)

    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainMenu(self.root)

    def choose_mode(self):
        mode = simpledialog.askstring("Game Mode", "Enter mode: 2P (two player) or AI (vs computer)",
                                      initialvalue=self.mode)
        if mode:
            mode = mode.upper()
            if mode in ['2P', 'AI']:
                self.mode = mode
            else:
                messagebox.showinfo(
                    "Invalid", "Mode must be '2P' or 'AI'. Defaulting to 2P.")
                self.mode = '2P'
        else:
            self.mode = '2P'
        self.choose_starting_player()
        self.restart()

    def choose_starting_player(self):
        options = ['Player (X)', 'AI (O)', 'Random'] if self.mode == 'AI' else [
            'X', 'O', 'Random']
        choice = simpledialog.askstring(
            "Who starts?", f"Who should start? {options}", initialvalue=options[0])
        if choice:
            choice = choice.lower()
            if 'random' in choice:
                starter = random.choice(['X', 'O'])
            elif 'ai' in choice or choice == 'o':
                starter = 'O'
            else:
                starter = 'X'
            self.game.set_starting_player(starter)
        else:
            self.game.set_starting_player('X')

    def update_status(self):
        # Update the status label with the current game state
        if hasattr(self, 'status_label'):
            if hasattr(self.game, 'game_over') and self.game.game_over:
                if hasattr(self.game, 'winner') and self.game.winner:
                    self.status_label.config(
                        text=f"{self.game.winner} wins! 🎉")
                else:
                    self.status_label.config(text="It's a draw! 🤝")
            else:
                if hasattr(self.game, 'current_player'):
                    self.status_label.config(
                        text=f"{self.game.current_player}'s turn")
            # Update scores if available
            if hasattr(self.game, 'scores'):
                for player, label in self.score_labels.items():
                    label.config(
                        text=f"{player}: {self.game.scores.get(player, 0)}")

# --- SNAKE GAME ---


class SnakeGame:
    def __init__(self, root, show_menu=False, level="easy"):
        self.root = root
        self.root.title("Snake Game 🐍")
        self.show_menu = show_menu
        self.level = level
        self.running = True
        self.paused = False
        self.score = 0
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.root.geometry("900x900")
        self.cell_size = 22
        self.width = 30
        self.height = 30
        self.snake = [(18, 14), (17, 14), (16, 14)]
        self.walls = self.generate_walls() if self.level in [
            "medium", "hard"] else []
        self.food = self.place_food()
        self.create_snake_widgets()
        self.root.bind('<Key>', self.on_key)
        self.move_snake()

    def create_snake_widgets(self):
        # Window size is set in __init__
        self.frame = tk.Frame(self.root, bg="#181f2a")
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.canvas = tk.Canvas(self.frame, width=self.width*self.cell_size, height=self.height *
                                self.cell_size, bg="#232b38", highlightthickness=12, highlightbackground="#00e0ff")
        self.canvas.pack(pady=60)
        self.score_label = tk.Label(self.frame, text=f"Score: {self.score}", font=(
            "Arial Rounded MT Bold", 22, "bold"), bg="#181f2a", fg="#00e0ff")
        self.score_label.pack(pady=10)
        btn_frame = tk.Frame(self.frame, bg="#181f2a")
        btn_frame.pack(pady=18)
        self.pause_btn = tk.Button(btn_frame, text="Pause", font=("Arial Rounded MT Bold", 18, "bold"), bg="#00e0ff", fg="#181f2a",
                                   width=12, height=2, command=self.toggle_pause, cursor='hand2', bd=0, activebackground="#00b8d9", activeforeground="#fff")
        self.pause_btn.pack(side=tk.LEFT, padx=16)
        restart_btn = tk.Button(btn_frame, text="Restart", font=("Arial Rounded MT Bold", 18, "bold"), bg="#00e0ff", fg="#181f2a",
                                width=12, height=2, command=self.snake_restart, cursor='hand2', bd=0, activebackground="#00b8d9", activeforeground="#fff")
        restart_btn.pack(side=tk.LEFT, padx=16)
        menu_btn = tk.Button(btn_frame, text="Main Menu", font=("Arial Rounded MT Bold", 18), bg="#232b38", fg="#eeeeee", width=12,
                             height=2, command=self.back_to_menu, cursor='hand2', bd=0, activebackground="#393e46", activeforeground="#00e0ff")
        menu_btn.pack(side=tk.LEFT, padx=16)

    def generate_walls(self):
        import random
        walls = set()
        if self.level == "medium":
            for _ in range(20):
                while True:
                    wx, wy = random.randint(
                        0, self.width-1), random.randint(0, self.height-1)
                    if (wx, wy) not in self.snake and (wx, wy) != self.food:
                        walls.add((wx, wy))
                        break
        elif self.level == "hard":
            # Add border walls
            for x in range(self.width):
                walls.add((x, 0))
                walls.add((x, self.height-1))
            for y in range(self.height):
                walls.add((0, y))
                walls.add((self.width-1, y))
        return list(walls)

    def place_food(self):
        while True:
            pos = (_random.randint(0, self.width-1),
                   _random.randint(0, self.height-1))
            if pos not in self.snake and pos not in self.walls:
                return pos

    def move_snake(self):
        if not self.running or self.paused:
            return
        self.direction = self.next_direction
        head = self.snake[0]
        dx, dy = {'Left': (-1, 0), 'Right': (1, 0),
                  'Up': (0, -1), 'Down': (0, 1)}[self.direction]
        new_head = (head[0]+dx, head[1]+dy)
        # Wrapping for easy/medium
        if self.level in ["easy", "medium"]:
            new_head = (new_head[0] % self.width, new_head[1] % self.height)
        # Check collision
        if (new_head in self.snake) or (self.level == "hard" and (not (0 <= new_head[0] < self.width) or not (0 <= new_head[1] < self.height))) or (new_head in self.walls):
            self.game_over()
            return
        self.snake = [new_head] + self.snake
        if new_head == self.food:
            self.score += 1
            self.food = self.place_food()
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.snake.pop()
        self.draw()
        self.root.after(100, self.move_snake)

    def draw(self):
        self.canvas.delete("all")
        # Draw walls
        for wx, wy in self.walls:
            self.canvas.create_rectangle(wx*self.cell_size, wy*self.cell_size, (wx+1)*self.cell_size,
                                         (wy+1)*self.cell_size, fill="#181f2a", outline="#ff1744", width=3)
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = "#00e0ff" if i == 0 else "#00adb5"
            self.canvas.create_rectangle(x*self.cell_size+2, y*self.cell_size+2, (x+1) *
                                         self.cell_size-2, (y+1)*self.cell_size-2, fill=color, outline="#181f2a", width=2)
        # Draw food
        fx, fy = self.food
        self.canvas.create_oval(fx*self.cell_size+6, fy*self.cell_size+6, (fx+1)*self.cell_size-6,
                                (fy+1)*self.cell_size-6, fill="#ff5722", outline="#fff", width=2)

    def snake_restart(self):
        self.running = True
        self.paused = False
        self.score = 0
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.walls = self.generate_walls() if self.level in [
            "medium", "hard"] else []
        self.food = self.place_food()
        self.score_label.config(text=f"Score: {self.score}")
        self.draw()
        self.move_snake()

    def on_key(self, event):
        key = event.keysym
        opposites = {'Left': 'Right', 'Right': 'Left',
                     'Up': 'Down', 'Down': 'Up'}
        if key in ['Left', 'Right', 'Up', 'Down'] and opposites[key] != self.direction:
            self.next_direction = key
        elif key.lower() == 'p':
            self.toggle_pause()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")
        if not self.paused:
            self.move_snake()

    def game_over(self):
        self.running = False
        self.canvas.create_text(self.width*self.cell_size//2, self.height*self.cell_size//2,
                                text="Game Over", fill="#ff1744", font=("Arial Rounded MT Bold", 48, "bold"), anchor="center")
        self.canvas.create_text(self.width*self.cell_size//2, self.height*self.cell_size//2+60,
                                text=f"Score: {self.score}", fill="#00e0ff", font=("Arial Rounded MT Bold", 32), anchor="center")

    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainMenu(self.root)

    def ai_move(self):
        move = self.game.ai_move()
        if move:
            row, col = move
            self.animate_button(row, col)
            self.update_board()
            self.update_status()

    def animate_button(self, row, col):
        btn = self.buttons[row][col]
        btn.config(bg='#00adb5', fg='#222831')
        self.root.after(200, lambda: btn.config(bg='#393e46', fg='#eeeeee'))


if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()
