'''Tic-Tac-Toe

Created for HIT3046 AI for Games, Lab 02,
By Clinton Woodward cwoodward@swin.edu.au

Notes:
* This simple function based implementation does not use an OO design. 
* Each function has a description string -- read to know more.
* Overall game flow follows a standard game loop trinity: 
    - process_input() # from the current player (human/AI)
    - update_mode()   # check the players input, then update the game world.
    - render_board()  # draw the current game board.
* Global variable (oh no!) are used to store and share game related data.

If you want to create your own AI it is suggested that you:
* Copy the get_ai_move function and rename it.
* Write you own new fancy AI thinking code.
* Update the "process_input" function to call your new "get_ai_move" code.

Want OO? There's another version of this code. Same functions, nice class.
'''

from random import randrange
# Possible win states.
# static game data - doesn't change (hence immutable tuple data type).
WIN_SET = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), 
           (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

# global variables for game data.
board = [' '] * 9
current_player = ''
# 'x' or 'o' for first and second player.
players = {'x': 'Human', 'o': 'Super AI'}
winner = None
move = None
# aesthetics...
HR = '-' * 40

#==============================================================================
# Game model functions.
    
def check_move():
    '''This function will return True if ``move`` is valid (in the board range 
    and free cell), or print an error message and return False if not valid. 
    ``move`` is an int board position [0..8].'''
    global move
    try:
        move = int(move)
        if board[move] == ' ':
            return True
        else:
            print (">> Sorry - that position is already taken!")
            return False
    except:
        print (">> %s is not a valid position! Must be int between 0 and 8.") % move
        return False
       
def check_for_result():
    '''Checks the current board to see if there is a winner, tie or not.
    Returns a 'x' or 'o' to indicate a winner, 'tie' for a stale-mate game, or
    simply False if the game is still going.
    '''
    for row in WIN_SET:
        if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
            return board[row[0]]
	    # return an 'x' or 'o' to indicate winner.

    if ' ' not in board:
        return 'tie'

    return None

#==============================================================================
# agent (human or AI) functions.

def get_human_move():
    '''Get a human players raw input. Returns None if a number is not entered.'''
    return input('[0-8] >> ')

# def get_ai_move_Default():
#     '''Get the AI's next move'''
#     # A simple dumb random move - valid or NOT!
#     # Note: It is the models responsibility to check for valid moves...
#     # [0..8]
#     # AI behaviour needs to suit the situation
#     # on the board instead of choosing random numbers
#     return randrange(9)

def get_ai_move_2():
#   '''Get the AI's 2 next move'''
# check the current results.
    if check_for_result():
    # return result.
        return check_for_result()
    # Check what moves have been made.
    elif check_move():
    # return move.
        return check_move()
    # return random if nothing else works.
    else:
        return randrange(9)

def get_ai_move():
    '''Get the AI's next move'''
    # Check the possibilities of winning
    for row in WIN_SET:
    # if certain spaces in each row the ai will return a result
        if board[row[0]] == board[row[1]] and board[row[2]] == ' ':
            return row[2]
        elif board[row[1]] == board[row[2]] and board[row[0]] == ' ':
            return row[0]
        elif board[row[0]] == board[row[2]] and board[row[1]] == ' ':
            return row[1]

    return randrange(9)

#==============================================================================
# Standard trinity of game loop methods (functions).

def process_input():
    '''Get the current players next move.'''
    # save the next move into a global variable.
    global move
    if current_player == 'x':
      move = get_human_move()
      # move = get_ai_move()
    else:
        move = get_ai_move()
       # move = get_ai_move_2

def update_model():
    '''If the current players input is a valid move, update the board and check 
    the game model for a winning player. If the game is still going, change the
    current player and continue. If the input was not valid, let the player
    have another go.'''
    global winner, current_player
    
    if check_move():
        # do the new move (which is stored in the global 'move' variable).
        board[move] = current_player
        # check board for winner (now that it's been updated).
        winner = check_for_result()
        # change the current player (regardless of the outcome).
        if current_player == 'x':
            current_player = 'o'
        else:
            current_player = 'x'
    else:
        print ("Try again")
    
def render_board():
    '''Display the current game board to screen.'''
    print ("%s | %s | %s " % tuple(board[:3]))
    print ("-----------")
    print ("%s | %s | %s " % tuple(board[3:6]))
    print ("-----------")
    print ("%s | %s | %s " % tuple(board[6:]))
    
    # pretty print the current player name.
    if winner is None:
        print ("The current player is: %s" % players[current_player])

#==============================================================================
 
def show_human_help():
    '''Show the player help/instructions.'''
    tmp = '''
To make a move enter a number between 0 - 8 and press enter.  
The number corresponds to a board position as illustrated:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    '''
    print (tmp)
    print (HR)

#==============================================================================
# Separate the running of the game using a __name__ test. Allows the use of this
# file as an imported module.
#==============================================================================

if __name__ == '__main__':
    # Welcome ...
    print ("Welcome to the amazing+awesome tic-tac-toe!")
    show_human_help()
    
    # by default the human player starts. This could be random or a choice.
    current_player = "x"
    
    # show the initial board and the current player's move.
    render_board()
    
    # Standard game loop structure.
    while winner is None:
        process_input()
        update_model()
        render_board()

    # Some pretty messages for the result.
    print (HR)
    if winner == ("tie"):
        print ("TIE!")
    elif winner in players:
        print ("%s is the WINNER!!!" % players[winner])
    print (HR)    
    print ("Game over. Goodbye")
