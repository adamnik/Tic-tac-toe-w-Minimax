Minimax Search Algorithm in Tic-Tac-Toe Game


        python3 tic_tac_toe.py [OPTIONAL] -ab=true


Optional ‘ab’ arg determines whether or not alpha-beta pruning will be used with the game’s minimax controlled players.


Program gives user the option to choose whether Players ‘X’ and ‘O’ are controlled by human players or minimax search algorithm. With each minimax player, the program will also prompt the user to input an integer that corresponds to the ply value, which is the number of game tree levels the minimax player will look down each turn (for a full game tree search, choose a ply value of 9). 


If both players are controlled by minimax, then the program will print the duration of the game in seconds when the game terminates. We did this to test for the effectiveness of using alpha-beta pruning; for a full game search of plies levels of 9 for both players, alpha-beta pruning was able to complete the game in 2-3 secs, whereas normal minimax took about 40-50 seconds each time.


Board Heuristic:


We needed a heuristic function to quantify how a given non-terminal state stands in reference to being in favor of either Player X or O. The heuristic allows minimax to still be effective in determining the next best move of a player even when we are not looking down the entire depth of the game tree. 


The board is stored as a matrix of 3’s (X’s), -3’s (O’s), and 0’s (empty spaces). We do this to simplify this process of calculating the heuristic.


To begin, for terminal states, we assign a value of +50 to Player X wins and -50 to Player O wins. These values are more extreme than the possible heuristic values of any non-terminal boards.
 
For non-terminal boards, for each line of 3 values (each row, column, and diagonal), we have a sum associated with it, which we initialize at 0. For each value we see, if the value is != to that sum, then we add the value to the sum. If the value is == to the sum (when there are two pieces of the same type in a line and thus one move away from a win), we multiply value * sum (maintaining the negative sign when we have two O’s in the same line). This results in the heuristic assigning more extreme values to boards that are closer to wins by either player. The final heuristic for any given board is the summation of values from every row, column, and diagonal in the board.

Examples:

X |  |   -> +3

X | X |   -> +9

O |  |   -> -3

X | O |   -> 0