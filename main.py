import random
import tkinter as tk
from tkinter import messagebox
import pygame  # مكتبة تشغيل الصوت

class GameChoice:
    STONE = 1
    PAPER = 2
    SCISSORS = 3

class Winner:
    PLAYER1 = 1
    COMPUTER = 2
    DRAW = 3

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock, Paper, Scissors Game")
        self.geometry("400x450")
        self.rounds = 0
        self.max_rounds = 0
        self.player1_wins = 0
        self.computer_wins = 0
        self.draws = 0
        
        pygame.mixer.init()  # تهيئة مكتبة pygame للصوت
        
        self.create_widgets()
        
    def create_widgets(self):
        self.lbl_title = tk.Label(self, text="Rock, Paper, Scissors", font=("Arial", 16, "bold"))
        self.lbl_title.pack(pady=10)

        self.lbl_rounds_input = tk.Label(self, text="Enter number of rounds (1-10):", font=("Arial", 12))
        self.lbl_rounds_input.pack(pady=5)

        self.entry_rounds = tk.Entry(self)
        self.entry_rounds.pack(pady=5)

        self.btn_start = tk.Button(self, text="Start Game", command=self.start_game)
        self.btn_start.pack(pady=5)

        self.lbl_round = tk.Label(self, text="", font=("Arial", 12))
        self.lbl_round.pack(pady=5)

        self.btn_stone = tk.Button(self, text="Stone", command=lambda: self.play_round(GameChoice.STONE), state=tk.DISABLED)
        self.btn_stone.pack(pady=5)

        self.btn_paper = tk.Button(self, text="Paper", command=lambda: self.play_round(GameChoice.PAPER), state=tk.DISABLED)
        self.btn_paper.pack(pady=5)

        self.btn_scissors = tk.Button(self, text="Scissors", command=lambda: self.play_round(GameChoice.SCISSORS), state=tk.DISABLED)
        self.btn_scissors.pack(pady=5)

        self.lbl_results = tk.Label(self, text="", font=("Arial", 12), wraplength=350)
        self.lbl_results.pack(pady=20)

        self.btn_reset = tk.Button(self, text="Reset Game", command=self.reset_game)
        self.btn_reset.pack(pady=10)

    def start_game(self):
        try:
            self.max_rounds = int(self.entry_rounds.get())
            if not 1 <= self.max_rounds <= 10:
                raise ValueError("Number out of range")
            self.lbl_round.config(text=f"Game started! Play {self.max_rounds} rounds.")
            self.enable_buttons()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 10.")
            self.entry_rounds.delete(0, tk.END)

    def enable_buttons(self):
        self.btn_stone.config(state=tk.NORMAL)
        self.btn_paper.config(state=tk.NORMAL)
        self.btn_scissors.config(state=tk.NORMAL)

    def play_round(self, player_choice):
        if self.rounds < self.max_rounds:
            computer_choice = random.randint(1, 3)
            winner = self.determine_winner(player_choice, computer_choice)
            computer_choice_name = self.get_choice_name(computer_choice)
            player_choice_name = self.get_choice_name(player_choice)

            if winner == Winner.PLAYER1:
                self.configure(bg="green")
                self.play_sound("win.mp3")  # تشغيل صوت الفوز
                self.player1_wins += 1
                result_text = f"You win! {player_choice_name} beats {computer_choice_name}."
            elif winner == Winner.COMPUTER:
                self.configure(bg="red")
                self.play_sound("lose.mp3")  # تشغيل صوت الخسارة
                self.computer_wins += 1
                result_text = f"You lose! {computer_choice_name} beats {player_choice_name}."
            else:
                self.configure(bg="yellow")
                self.draws += 1
                result_text = f"It's a draw! Both chose {player_choice_name}."

            self.rounds += 1
            self.lbl_results.config(text=f"Round {self.rounds}/{self.max_rounds}: {result_text}\n"
                                         f"Player Wins: {self.player1_wins}, Computer Wins: {self.computer_wins}, Draws: {self.draws}")
            
            if self.rounds == self.max_rounds:
                self.show_final_results()

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)  # تحميل الملف الصوتي
        pygame.mixer.music.play()  # تشغيل الملف الصوتي

    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return Winner.DRAW
        elif ((player_choice == GameChoice.STONE and computer_choice == GameChoice.SCISSORS) or
              (player_choice == GameChoice.PAPER and computer_choice == GameChoice.STONE) or
              (player_choice == GameChoice.SCISSORS and computer_choice == GameChoice.PAPER)):
            return Winner.PLAYER1
        else:
            return Winner.COMPUTER

    def get_choice_name(self, choice):
        choices = {GameChoice.STONE: "Stone", GameChoice.PAPER: "Paper", GameChoice.SCISSORS: "Scissors"}
        return choices[choice]

    def reset_game(self):
        self.rounds = 0
        self.max_rounds = 0
        self.player1_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.lbl_results.config(text="")
        self.lbl_round.config(text="")
        self.entry_rounds.delete(0, tk.END)
        self.configure(bg="SystemButtonFace")
        self.disable_buttons()
        messagebox.showinfo("Game Reset", "The game has been reset!")

    def disable_buttons(self):
        self.btn_stone.config(state=tk.DISABLED)
        self.btn_paper.config(state=tk.DISABLED)
        self.btn_scissors.config(state=tk.DISABLED)

    def show_final_results(self):
        final_winner = "Draw" if self.player1_wins == self.computer_wins else "Player" if self.player1_wins > self.computer_wins else "Computer"
        messagebox.showinfo("Game Over", f"Game Over!\n\n"
                                         f"Rounds: {self.rounds}\n"
                                         f"Player Wins: {self.player1_wins}\n"
                                         f"Computer Wins: {self.computer_wins}\n"
                                         f"Draws: {self.draws}\n"
                                         f"Final Winner: {final_winner}")
        self.reset_game()

if __name__ == "__main__":
    random.seed()
    app = GameApp()  
    app.mainloop()
