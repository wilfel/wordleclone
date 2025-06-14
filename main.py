"""
CSCI 203 Final Project: Wordle at home
Author: Will Feldscher
Date: January 30, 2024
CSCI 203, Spring 2024
"""

import matplotlib.pyplot as pyplot
import random
import tkinter as tk
from tkinter import ttk

# Some sources used for help with tkinter:
# First ~20 minutes of this video: https://www.youtube.com/watch?v=mop6g-c5HEY
# This documentation on tkinter: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html

# Github source for word text files: https://gist.github.com/slushman/34e60d6bc479ac8fc698df8c226e4264

def getAnswer():
    """Randomly generates answer from answerlist.txt
    
    Parameters:
        None
        
    Return value:
        answer: a string, answer to the game hidden from the player
    """
    word_list_file = open('answerlist.txt', 'r')
    words = word_list_file.read()
    word_list_file.close()
    word_list = words.split() # Split words separated by a line break
    answer = word_list[random.randrange(len(word_list))] # Randomly select an item number as a word
    return answer

def getWordList():
    """Creates a list of words from wordlist.txt containing 5 letter words
    
    Parameters:
        None
        
    Return value:
        valid_list: a list, containing all 5 letter words
    """
    valid_list_file = open('wordlist.txt', 'r')
    valids = valid_list_file.read()
    valid_list_file.close()
    valid_list = valids.split() # Split words separated by a line break
    return valid_list

def clear(entry):
    """Clears the text box where users enter an answer
    
    Parameters:
        entry: an entry widget (from tkinter), a text box
        
    Return value:
        None
    """
    entry.delete(0,tk.END) # Clears the text box from first character to end

def storeResults(guess_num):
    """Writes the number of guesses the player took to a text file
    
    Parameters:
        guess_num: an integer, the number of guesses the player took to win
        
    Return value:
        None
    """
    results_file = open('wordleresults.txt','a') # Opens file to append
    results_file.write(guess_num) # Adds # of guesses it took to win to a string
    results_file.close()

def displayResults(file):
    """Graphs the guess distribution of the player from the text file
    containing the number of guesses across multiple games
    
    Parameters:
        file: a text file, the stored guesses across multiple games
        
    Return value:
        None
    """
    results_file = open(file, 'r')
    data = results_file.read()
    guess_dict = {}
    for key in range(1,7): # Creates keys of guess numbers
        guess_dict[key] = 0
    for char in data: # Records the frequency of each guess length in the dictionary
        for key in guess_dict:
            if int(key) == int(char):
                guess_dict[key] += 1
    counts = guess_dict.keys() # bins for bar graph
    totals = guess_dict.values() # y variable for graph
    pyplot.bar(counts, totals) # Makes bar graph
    pyplot.xlabel('Number of Guesses')
    pyplot.ylabel('Frequency')
    pyplot.title('Guess Distribution')
    pyplot.show()
    
def checkGuess(answer, guess):
    """Checks the user's guess against the answer and list of possible words
    
    Parameters:
        entry: a string, the answer to the game
        guess: a string, the player's guess
        
    Return value:
        None
    """
    # Colors from: https://www.color-hex.com/color-palette/1012607
    try:
        placeholder = valid_list.index(guess) # Checks if user guess is in the word list
    except: # If it's not a valid word
        error = tk.Toplevel(window) # Creates a popup window
        error.geometry('200x100')
        tk.Label(error, text = "User guess not \n in world list",
                 font = ('Neue Helvetica', '20')).pack()
    else: # If it is a valid word
        score = 0 # Starts a 'score' variable for each correct letter (ie score = 5 = win)
        global guess_num # Lets guess number variable be continually changed in/outside function
        
        for guess_char in range(len(guess)):
            if guess[guess_char] == answer[guess_char]: # If right letter in right spot, green box
                color = '#6ca965'
                score += 1
            else:
                for answer_char in range(len(answer)): # If right letter in wrong spot, yellow box
                    if guess[guess_char] == answer[answer_char]:
                        color = '#c8b653'
                        break
                    else: # If nothing, gray box
                        color = '#787c7f'
                    
            char = tk.Label(master=shape_list[guess_num][guess_char], text=guess[guess_char].upper(), bg=color,
                            fg = 'white',font = ('Neue Helvetica','60', 'bold')) # Makes letter as a label widget
            char.pack(expand=True, fill='both', side = 'top') # Packs character into box
            shape_list[guess_num][guess_char].config(width = 100, height = 100) 
        guess_num += 1 # Next guess number
        if score == 5:
            storeResults(str(guess_num)) # Win condition
            displayResults('wordleresults.txt')
        elif guess_num == 6: # Lose condition
            lose = tk.Toplevel(window) # Creates a popup window
            lose.geometry('200x100')
            tk.Label(lose, text = "The word was\n"+str(answer),
                 font = ('Neue Helvetica', '20')).pack()

# Main stuff here

answer = getAnswer() # Generates answer
window = tk.Tk() # Opens main window
window.title('Wordle')
title_label = ttk.Label(master=window, text='Wordle')
guess_num = 0
valid_list = getWordList()

# To make UI (used some sources to get tkinter information, shown above):

guess_list = [[], [], [], [], [], []] # Empty array to hold 6 possible guesses
shape_list = guess_list # Mirrors guess array to hold information to display on the UI

for row in range(len(shape_list)): # Iterates over the 5 characters in each of the 6 possible guesses
    for char in range(5): 
        shape = tk.Frame(master=window, height=100, width=100, borderwidth=2, bg='black', relief='sunken')
        shape_list[row].append(shape) # Adds a black square for each character in each guess
        shape_list[row][char].grid(row=row, column=char, sticky='nsew') # Places black square in a grid
        shape_list[row][char].grid_columnconfigure(0, weight=1) # Adjustments to ensure shape fills correctly
        shape_list[row][char].grid_rowconfigure(0, weight=1) 

input_frame = ttk.Frame(master=window) # Create input frame
user_input = tk.StringVar()
entry = ttk.Entry(master=input_frame, textvariable=user_input) # User text box entry
button = ttk.Button(master=input_frame, text='Guess', command = lambda: [checkGuess(answer, user_input.get()), clear(entry)])
# Runs checkGuess and clear functions on button press

entry.grid(row=0, column=0) # Places stuff on grid
button.grid(row=0, column=1)
input_frame.grid(row=7, column=0, columnspan=5)


