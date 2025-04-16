import tkinter as tk
from tkinter import messagebox
from game_logic import SimpleGame, GeneralGame, gameplay, humanPlayer, cpuPlayer
import random
import os

class SOSGui:
    def __init__(self, root, game_logic):
        self.root = root
        self.manual_restart = False
        self.game_logic = game_logic
        self.buttons = []
        self.create_gui()

    def create_gui(self):
        self.root.title("SOS game")

        main_frame = tk.Frame(self.root, padx=10, pady=10, bg="gray")
        main_frame.pack(expand = True, fill=tk.BOTH)

        title_label = tk.Label(main_frame, text = "SOS", font=("Arial", 20, "bold"), bg ="gray")
        title_label.pack(pady=10)

        mode_size_frame = tk.Frame(main_frame, bg= "gray")
        mode_size_frame.pack(pady=10)


        #gamemode
        tk.Label(mode_size_frame, bg="lightgray").grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value = "Simple")
        tk.Radiobutton(mode_size_frame, text="Simple Game", variable=self.mode_var, value = "Simple", bg="gray").grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(mode_size_frame, text="General Game", variable=self.mode_var, value = "General", bg="gray").grid(row=0, column=2, sticky=tk.W)

        #board size
        tk.Label(mode_size_frame, text="Board size").grid(row=0, column=3, sticky=tk.W)
        self.size_entry = tk.Entry(mode_size_frame, width = 5)
        self.size_entry.grid(row=0, column=4)

        #This should help keep the column in the middle
        game_frame = tk.Frame(main_frame, bg="gray")
        game_frame.pack(fill=tk.BOTH, expand=True)
        game_frame.columnconfigure(0, weight=1) 
        game_frame.columnconfigure(1, weight=2)
        game_frame.columnconfigure(2, weight=1)

        # Left side Blue player
        self.blue_frame = tk.Frame(game_frame, bg="gray")
        self.blue_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.create_player_options(self.blue_frame, "Blue player", "Blue")

        #Grid
        self.grid_frame = tk.Frame(game_frame, bg="lightgrey")
        self.grid_frame.pack(side=tk.LEFT, padx=30, pady=10)

        #Right side Red player
        self.red_frame = tk.Frame(game_frame, bg="gray")
        self.red_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.create_player_options(self.red_frame, "Red player", "Red")

        #Control buttons frames
        control_frame = tk.Frame(main_frame, bg="gray")
        control_frame.pack(side=tk.BOTTOM, pady=10)

        #Tells what turn it is
        self.turn_label = tk.Label(main_frame, text=f"Current turn: {self.game_logic.current_turn}", bg="gray")
        self.turn_label.pack(side=tk.BOTTOM, pady=10)

        #buttons for new game
        tk.Button(control_frame, text="New Game", command=self.gameStart).pack(side=tk.LEFT, padx=5)

        #Scoreboard
        self.scoreboard = tk.Label(main_frame, text=f"Blue: 0 Red: 0", bg="lightgray", font=("Arial", 12, "bold"))
        self.scoreboard.pack(side=tk.BOTTOM, pady= 5)

    def create_player_options(self, parent_frame, player_label, color):
        player_frame = tk.Frame(parent_frame, bg="gray")
        player_frame.pack(anchor=tk.W, pady=5)

        label = tk.Label(parent_frame, text=player_label, font=("Helvetica", 12, "bold"), bg="gray")
        label.pack(anchor=tk.W, pady=(0, 5))

        player_type_var = tk.StringVar(value="Human")
        tk.Radiobutton(player_frame, text="Human", variable=player_type_var, value="Human", bg="gray").grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(player_frame, text="Computer", variable=player_type_var, value="Computer", bg="gray").grid(row=3, column=0, sticky=tk.W)
        

        letter_var = tk.StringVar(value="S")
        tk.Radiobutton(player_frame, text="S", variable=letter_var, value="S", bg="gray").grid(row=2, column=0, sticky=tk.W, padx=20)
        tk.Radiobutton(player_frame, text="O", variable=letter_var, value="O", bg="gray").grid(row=2, column=1, sticky=tk.W)

        if color == "Blue":
            self.blue_choice = letter_var
            self.blue_type = player_type_var
        else:
            self.red_choice = letter_var
            self.red_type = player_type_var 


    def gameGrid(self, size):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for r in range(size):
            row = []
            for c in range(size):
                btn = tk.Button(self.grid_frame, text="", width=5, height=2,
                                font=("Arial", 12), command=lambda r=r, c=c: self.on_grid_click(r, c))
                btn.grid(row=r, column=c, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)
        self.grid_frame.pack()

    def on_grid_click(self, row, col):
        current_player = self.blue_player if self.game_logic.current_turn == 'Blue' else self.red_player

        if current_player.is_computer():
            return
        

        letter = current_player.choose_letter()
        winner, sosLine = self.game_logic.letterPlace(row, col, letter)
        self.buttons[row][col].config(text=letter)

        if sosLine:
            if isinstance(sosLine[0], list):
                sosLine = sosLine[0] 
            self.color_sos_letters(sosLine)

            player_color = "blue" if self.game_logic.current_turn == "Blue" else "red"

            for r, c in sosLine:
                self.buttons[r][c].config(fg=player_color, disabledforeground=player_color)
                self.root.after(200, lambda r=r, c=c: self.buttons[r][c].config(state=tk.DISABLED, disabledforeground=player_color))

        if winner:
            self.update_scoreboard
            self.end_game_dialog(f"{winner} has won!")
        if self.game_logic.is_full():
            blue_score = self.game_logic.scores["Blue"]
            red_score = self.game_logic.scores["Red"]
            if blue_score > red_score:
                self.end_game_dialog("Blue wins!")
            elif red_score > blue_score:
                self.end_game_dialog("Red wins!")
            else:
                self.end_game_dialog("It's a draw!")
        else:
            self.update_scoreboard()
            self.update_turn_label()

        self.game_logic.switch_turn()
        self.update_turn_label()
        self.update_scoreboard()

        next_player = self.blue_player if self.game_logic.current_turn == 'Blue' else self.red_player

        if next_player.is_computer():
            self.root.after(400, lambda: self.computer_turn())

    def place_move(self, row, col, letter):
        winner, sosLine = self.game_logic.letterPlace(row, col, letter)
        self.buttons[row][col].config(text=letter)

        if sosLine:
            if isinstance(sosLine[0], list):
                sosLine = sosLine[0] 
            self.color_sos_letters(sosLine)

            player_color = "blue" if self.game_logic.current_turn == "Blue" else "red"

            for r, c in sosLine:
                self.buttons[r][c].config(fg=player_color, disabledforeground=player_color)
                self.root.after(200, lambda r=r, c=c: self.buttons[r][c].config(state=tk.DISABLED, disabledforeground=player_color))

        if winner:
            self.update_scoreboard()
            self.end_game_dialog(f"{winner} has won!")
            return
        if self.game_logic.is_full():
            blue_score = self.game_logic.scores["Blue"]
            red_score = self.game_logic.scores["Red"]
            if blue_score > red_score:
                self.end_game_dialog("Blue wins!")
            elif red_score > blue_score:
                self.end_game_dialog("Red wins!")
            else:
                self.end_game_dialog("It's a draw!")
        else:
            self.update_scoreboard()
            self.update_turn_label()

        self.game_logic.switch_turn()
        self.update_turn_label()
        self.update_scoreboard()

        next_player = self.blue_player if self.game_logic.current_turn == 'Blue' else self.red_player
        if next_player.is_computer():
            self.root.after(400, lambda: self.computer_turn())

    def handleMoveResult(self, winner, sosLine):
        if winner:
            self.update_scoreboard()
            messagebox.showinfo("Game over", f"{winner} has won!")
            self.gameStart()
        elif self.game_logic.is_full():
            messagebox.showinfo("Game over", "It's a draw")
            self.gameStart()
        else:
            self.update_turn_label()
            self.update_scoreboard()
            
    def computer_turn(self):
        current_player = self.blue_player if self.game_logic.current_turn == 'Blue' else self.red_player

        row, col = current_player.choose_position(self.game_logic)
        letter = current_player.choose_letter()
        self.place_move(row, col, letter)

    

    def gameStart(self):
        try:
            size_input = self.size_entry.get()
            size = int(size_input)
            
            if size < 3 or size > 10:
                raise ValueError("Size must be between 3 and 10")

            game_mode = self.mode_var.get()
            if game_mode == "Simple":
                self.game_logic = SimpleGame(size)
            else:
                self.game_logic = GeneralGame(size)

            

            if self.blue_type.get() == "Human":
                self.blue_player = humanPlayer("Blue", lambda: self.blue_choice.get())
            else:
                self.blue_player = cpuPlayer("Blue")

            
            if self.red_type.get() == "Human":
                self.red_player = humanPlayer("Red", lambda: self.red_choice.get())
            else:
                self.red_player = cpuPlayer("Red")
            self.gameGrid(size)
            self.update_turn_label()

            if hasattr(self, "scoreboard"):
                self.scoreboard.destroy()

            self.scoreboard = tk.Label(self.root, text="Blue: 0 Red: 0", bg="lightgray", font=("Arial", 12, "bold"))
            self.scoreboard.pack(side=tk.BOTTOM, pady=5)

            starting_player = self.blue_player if self.game_logic.current_turn == 'Blue' else self.red_player
            if starting_player.is_computer():
                self.root.after(400, self.computer_turn)

        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

    def update_turn_label(self):
        self.turn_label.config(text=f"Current turn: {self.game_logic.current_turn}")

    def update_scoreboard(self):
        scores = self.game_logic.scores
        self.scoreboard.config(text=f"Blue: {scores['Blue']} Red: {scores['Red']}")

    def end_game_dialog(self, message):
        result = messagebox.askyesno("Game over", f"{message}\n\nWould you want to start a new game with new inputs?")
        if result:
            self.manual_restart = True
            return
        else:
            print("Game over. Exiting program!")
            self.root.quit()
    
    def color_sos_letters(self, sosLine):
        if len(sosLine) == 1 and isinstance(sosLine[0], list):
            sosLine = sosLine[0]
        
        player_color = "blue" if self.game_logic.current_turn == "Blue" else "red"

        for r, c in sosLine:
            self.buttons[r][c].config(state=tk.NORMAL, foreground=player_color)
            self.root.after(200, lambda r=r, c=c: self.buttons[r][c].config(state=tk.DISABLED))

        
if __name__ == "__main__":
    root = tk.Tk()
    game_logic = gameplay(3, "Simple")
    app = SOSGui(root, game_logic)
    root.mainloop()
        
