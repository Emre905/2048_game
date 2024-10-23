import numpy as np 
import random 
from math import log2
from tabulate import tabulate 
from IPython.display import clear_output 
import re 

set_num=np.array([2**i for i in range(1,20)])

# Generate a new random number at a randomly choosen place amongst all squares that is 0
def random_generate(board):
    # Getting the max element at board to see what values we can generate (ideally not much bigger or smaller than max element)
    max_element = np.max(board)
    
    # locating the 0's on board
    set = np.argwhere(board == 0)
    
    #defining upper and lower bounds for possible generations
    lower = max(0 , int(log2(max_element)-4))
    upper = max(1 , int(log2(max_element)-1))
    set_border = set_num[lower:upper]
    
    # If there's at least one 0 left on the board (meaning there's at least one move left)
    if len(set)>0:
        # This part is optional, we're giving bigger probabilities to smaller numbers to make it fair
        if len(set_border) == 1:
            weights = [1]
        if len(set_border) == 2:
            weights = [0.7, 0.3]
        if len(set_border) == 3:
            weights = [0.5, 0.3, 0.2]
        
        # Choosing a number and location and putting in board
        ran_loc = np.random.randint(0,len(set))
        ran_num = np.random.choice(set_border, p=weights)
        row,col = set[ran_loc]
        board[row,col] = ran_num

        return board
    else:      
        return False
    
#Formats a number to 'k' for thousands and 'm' for millions.
def format_number(n):
    if n >= 1_000_000:
        return f"{n // 1_000_000}m"
    elif n >= 1_000:
        return f"{n // 1_000}k"
    else:
        return str(n)

# Print the board after each move    
def board_print(board):

    # Create a copy of the board as strings, format big number
    temp_board = np.vectorize(format_number)(board)  # format big numbers

    # Use tabulate to display the board
    table = tabulate(temp_board, tablefmt="fancy_grid", numalign='center')
    table = re.sub(r'\b0\b', ' ', table)  # \b0\b matches a whole word '0'
    print(table)


# Shift all 0's to the end of their corresponding column
def shift_zeros(board):
    for _ in range(3):
        for row in range(3):
            for col in range(4):
                if board[row][col] == 0:
                    board[row][col],board[row+1][col] = board[row+1][col],board[row][col]
    return board

# Define how the numbers will add up when "w" is given as input
def move_up(board):
    board=shift_zeros(board)
    for row in np.arange(3):
        for col in np.arange(4):
            if board[row][col]==board[row+1][col] and board[row][col]!=0:                   
                board[row][col] = 2*board[row][col]
                if row==0:
                    board[row+1][col],board[row+2][col]=board[row+2][col],board[row+3][col]
                    board[row+3][col]=0
                if row==1:
                    board[row+1][col]=board[row+2][col]
                    board[row+2][col]=0
                if row==2:
                    board[row+1][col]=0
    return board

# Define other 3 moves with the help of move_up function
def move_down(board):
    board=np.flip(board, 0)
    board=move_up(board)
    board=np.flip(board, 0)
    return board

def move_left(board):
    board=np.transpose(board)
    board=move_up(board)
    board=np.transpose(board)
    return board

def move_right(board):
    board=np.transpose(board)
    board=move_down(board)
    board=np.transpose(board)
    return board


# Set the board and give instructions 
def game_start():
    #setting the board
    board = np.array([[0 for _ in range(4)] for _ in range(4)])
    
    ran=random.randint(0,15) # select a random square
    row , col = divmod(ran,4)
    board[row,col]=2 # set the initial value on selected square
    
    instructions="""Commands are as follows : 
      'W' or 'w' : Move Up
      'S' or 's' : Move Down
      'A' or 'a' : Move Left
      'D' or 'd' : Move Right
      'quit'     : quit"""
      
    print(instructions)
    board_print(board)
    return board

# This function takes the user move and matches it with the corresponding move
def game_2048(board):
    move=input('make your move: ')
    if move in ['w','s','a','d']:
        if move.lower() == "w":
            move_up(board)
        if move.lower() == "s":
            move_down(board)
        if move.lower() == "a":
            move_left(board)
        if move.lower() == "d":
            move_right(board)
        return board
    
    elif move=='quit':
        board[0,0]=1
        return board
    
    else:
        print('enter a valid move')
        board_print(board)
        game_2048(board)       
        return board

# This is the main function that runs other functions in order to play the game
def game():
    board = game_start()
    while True:
        clear_output(wait=True) # This line is for deleting the previous board and may not work on all interpreters
        board = game_2048(board)
        board = random_generate(board)
            
        if board is False or (board==1).any():
            print('End of game! ')
            again = input("Would you like to play again? (y/n): ")
            if again.lower() == 'y':
                board = game_start()
            else:
                print('Thanks for playing')
                break
                
        elif board is not False:
            board_print(board)
        
game()
