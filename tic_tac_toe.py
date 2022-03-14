from typing import NamedTuple
from copy import deepcopy

Move = NamedTuple('Move', [('row', int), ('col', int)])

X = 3
O = -3

def intToChar(val):
	if val == X:
		return 'X'
	elif val == O:
		return 'O'
	elif val == 0:
		return ' '

class Board:

	def __init__(self, player1, player2):
		self.matrix = []
		self.size = 3
		for i in range(self.size):
			self.matrix.append([0 for i in range(self.size)])
		self.players = [player1, player2]
		self.iters = 1
		
	def heuristic(self):
	
		if self.checkWinner() == X:
			return 50
		elif self.checkWinner() == O:
			return -50
			
		rowTotalHeuristic = 0
		for i in range(self.size):
			rowHeuristic = 0
			for j in range(self.size):
				if self.matrix[i][j] == rowHeuristic:
					if rowHeuristic < 0:
						rowHeuristic *= abs(self.matrix[i][j])
					else:
						rowHeuristic *= self.matrix[i][j]
				else:
					rowHeuristic += self.matrix[i][j]
			rowTotalHeuristic += rowHeuristic
				
		colTotalHeuristic = 0
		for i in range(self.size):
			colHeuristic = 0
			for j in range(self.size):
				if self.matrix[j][i] == colHeuristic:
					if colHeuristic < 0:
						colHeuristic *= abs(self.matrix[j][i])
					else:
						colHeuristic *= self.matrix[j][i]
				else:
					colHeuristic += self.matrix[j][i]
			colTotalHeuristic += colHeuristic
				
		diagonalHeuristic1 = 0
		for cell in [self.matrix[0][0], self.matrix[1][1], self.matrix[2][2]]:
			if cell == diagonalHeuristic1:
				if diagonalHeuristic1 < 0:
					diagonalHeuristic1 *= abs(cell)
				else:
					diagonalHeuristic1 *= cell
			else:
				diagonalHeuristic1 += cell
				
		diagonalHeuristic2 = 0
		for cell in [self.matrix[2][0], self.matrix[1][1], self.matrix[0][2]]:
			if cell == diagonalHeuristic2:
				if diagonalHeuristic2 < 0:
					diagonalHeuristic2 *= abs(cell)
				else:
					diagonalHeuristic2 *= cell
			else:
				diagonalHeuristic2 += cell
		
		heuristic = rowTotalHeuristic + colTotalHeuristic + diagonalHeuristic1 + diagonalHeuristic2
		return heuristic
			
	def printBoard(self):
		print('   0 1 2')
		for i, row in enumerate(self.matrix):
			print(str(i) + ': ', end='')
			for j, col in enumerate(self.matrix):
				if j == self.size - 1:
					print(intToChar(self.matrix[i][j]))
				else:
					print(intToChar(self.matrix[i][j]) + '|', end = '')
					
			if i != self.size - 1:
				print('   -+-+-')
				
	def possibleMoves(self):
		if self.checkWinner():
			return None
		moves = []
		for i, row in enumerate(self.matrix):
			for j, col in enumerate(self.matrix):
				if self.matrix[i][j] == 0:
					moves.append(Move(row=i,col=j))
		return moves	
				
	def placeMove(self, move, val):
		BoardCopy = deepcopy(self)
		BoardCopy.matrix[move.row][move.col] = val
		return BoardCopy
		
	def checkWinner(self):
		#horizontals
		for row in self.matrix:
			if row[0] == row[1] and row[1] == row[2] and row[0] != 0:
				return row[0]
				
		#verticals
		for j, col in enumerate(self.matrix):
			if self.matrix[0][j] == self.matrix[1][j] and self.matrix[1][j] ==  self.matrix[2][j] and self.matrix[0][j] != 0:
				return self.matrix[0][j]
				
		#diagonals
		if self.matrix[0][0] == self.matrix[1][1] and self.matrix[1][1] == self.matrix[2][2] and self.matrix[0][0] != 0:
			return self.matrix[0][0]
			
		if self.matrix[2][0] == self.matrix[1][1] and self.matrix[1][1] == self.matrix[0][2] and self.matrix[2][0] != 0:
			return self.matrix[2][0]
			
		#no winner
		return 0
		
	def printWinner(self, win):
		winner = intToChar(win)
		print('Player', winner, 'Wins!')
		
	def playGame(self):
		self.printBoard()
		while True:
			curPlayer = self.players[(self.iters+1) % 2]
			self = self.placeMove(curPlayer.chooseMove(self), curPlayer.val)
			print('')
			self.printBoard()
			if self.iters > 4:
				win = self.checkWinner()
				if win:
					self.printWinner(win)
					return
			if self.iters == 9:
				print("It's a draw!")
				return
			self.iters += 1
				
class HumanPlayer:

	def __init__(self, val):
		self.val = val
		
	def chooseMove(self, board):
		while True:
			row = int(input('Row: '))
			col = int(input('column: '))
			move = Move(row=row,col=col)
			if move in board.possibleMoves():
				return move
			else:
				print('Invalid move. Please try again.')
				
class MiniMaxPlayer:
	
    def __init__(self, val):
        self.val = val
        self.plies = int(input("How many plies down do you want the computer to look down the game tree (int)? "))
        
    def chooseMove(self, board):
        if self.val == X:
        	value, move = self.maxValue(board, 1)
        elif self.val == O:
        	value, move = self.minValue(board, 1)
        return move
        
    def maxValue(self, board, iteration):
    	nextMove = None
    	if iteration > self.plies or not board.possibleMoves():
    		return board.heuristic(), nextMove
    	best = float('-inf')
    	for move in board.possibleMoves():
    		curVal, curMove = self.minValue(board.placeMove(move, X), iteration + 1)
    		if curVal > best:
    			best, nextMove = curVal, move
    	return best, nextMove
    	
    def minValue(self, board, iteration):
    	nextMove = None
    	if iteration > self.plies or not board.possibleMoves():
    		return board.heuristic(), nextMove
    	best = float('inf')
    	for move in board.possibleMoves():
    		curVal, curMove = self.maxValue(board.placeMove(move, O), iteration + 1)
    		if curVal < best:
    			best, nextMove = curVal, move
    	return best, nextMove
    	
def getPlayers():
	player1, player2 = None, None
	while True:
		playerOneType = input("Should Player 'X' be human or computer controlled? Enter 'h' for computer and 'c' for computer: ")
		if playerOneType == 'h':
			player1 = HumanPlayer(X)
			break
		elif playerOneType == 'c':
			player1 = MiniMaxPlayer(X)
			break
		else:
			print("Invalid. Please try again.")
			
	while True:
		playerTwoType = input("Should Player 'O' be human or computer controlled? Enter 'h' for computer and 'c' for computer: ")
		if playerTwoType == 'h':
			player2 = HumanPlayer(O)
			break
		elif playerTwoType == 'c':
			player2 = MiniMaxPlayer(O)
			break
		else:
			print("Invalid. Please try again.")
			
	return player1, player2

def main():
	player1, player2 = getPlayers()
	board = Board(player1, player2)
	board.playGame()
	
if __name__ == '__main__':
	main()