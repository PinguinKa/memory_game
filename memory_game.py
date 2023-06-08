import tkinter as tk
from tkinter import font
import random
import time
import csv


class MemoryGame:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.series = ""
        self.results = {}

        self.root = tk.Tk()
        self.root.title("Memory Game")
        self.root.geometry("300x200")
        
        font = tk.font.Font(family="Arial", size=15)
        self.label = tk.Label(self.root, font=font, text="Nickname:")
        self.label.pack()

        self.entry = tk.Entry(self.root)

        self.player_name = tk.Entry(self.root)
        self.player_name.pack()
        
        self.button = tk.Button(self.root, text="Start", command=self.start_game)
        self.button.pack()
        
        self.button2 = tk.Button(self.root, text="Check", command=self.check_answer)
        

        self.root.mainloop()

    def generate_numbers(self, num_digits):
        if self.level == 1:
            numbers = [str(random.randint(0, 9)) for _ in range(num_digits)]
        else:
            min_number = int('1'+'0'*(self.level-1))
            max_number = int('9'*self.level)
            numbers = [str(random.randint(min_number, max_number)) for _ in range(num_digits)]
        self.series = " ".join(numbers)
        return self.series

    def display_numbers(self, num_digits, numbers):
        self.label.configure(text=numbers)
        self.entry.pack_forget()
        self.button2.pack_forget()
        self.root.update()
        
        time.sleep(1 * num_digits)
        
       
        self.entry.pack()  
        self.button2.pack()
        
        self.label.configure(text="")
        self.root.update()

    def start_game(self):
        self.button.pack_forget()
        self.name = self.player_name.get()
        self.player_name.pack_forget()
        self.entry.pack()
      
        self.button2.pack()

        num_digits = self.score + 1
        numbers = self.generate_numbers(num_digits)
        self.display_numbers(num_digits, numbers)
    
    def check_answer(self):
        player_input = self.entry.get()
        numbers = self.series
        if player_input == numbers:
            self.score += 1
            self.label.configure(text='Correct')
        else:   
            self.results[self.name] = [self.level, self.score]
            self.label.configure(text=f'Incorrect \nPlayer: {self.name}\nLevel: {self.level}\nScore: {self.score}\n\nNickname:')
            self.level = 1
            self.score = 0
            self.player_name.pack()
            self.save_results()

        self.entry.delete(0, tk.END)
        self.button.configure(state=tk.NORMAL)

        self.display_results()
        self.new_level()

    def display_results(self):
        self.button2.pack_forget()
        self.button.pack()
        self.entry.pack_forget()
        self.root.update()
        
    def new_level(self):
        if self.score == 5:
            self.level += 1
            self.score = 0

    def save_results(self):
        filename = "results.csv"
        with open(filename, mode="a", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Player", "Level", "Score"])
            print(self.results.items())
            for name, result in self.results.items():
                writer.writerow([name, result[0], result[1]])
            self.results = {}