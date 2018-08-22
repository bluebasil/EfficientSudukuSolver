import argparse
from copy import deepcopy
import sys

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputFile',
                   help='the Suduku file to import.  Should be 9 rows, 9 colums each seperated by spaces.  0 represents a blank space.')
#This is for easy exporting to excel to create the plots
parser.add_argument('-r','--raw', action="store_true",
                   help='only outputs the number of steps')

args = parser.parse_args()
#print(args)

F = open(args.inputFile)

#keeps track of the number of variable assignments
stepNumber = 0

board=[[0 for i in range(10)] for j in range(10)]

i=0
for line in F:
  board[i] = line.split()
  i+=1
  if i==10:
  	break;

F.close()

#our cell object is more complex than version 1
#now we store the valid options this cell may take
#we later remove these options as they are no longer legal
class cell():
	value = 0
	def __init__(self):
		#The domain for this cell
		self.options = [1,2,3,4,5,6,7,8,9]
	#removes option from possible options this cell could take
	#returns false if we have removed its last legal domain option, 
	#implying that whatever path led to the removal of the domain option is invalid
	def rem(self, i):
		if self.options.count(i) > 0:
			self.options.remove(i)
		if self.value != 0 or len(self.options) > 0:
			return True
		else:
			return False


def printBoard(board):
	for i in range(9):
		for j in range(9):
			print(board[i][j].value, end=' ')
		print()

#we have replaced the isLegal check in version1 with this set function
#it is implied that placing k in cell i,j is legal, 
#it then forward checks all of its constraining cells (vertical, horizontal, sub-square)
#If any cell is not arc consistant, and the last domain option would be removed, this 
#returns false, otherwise, if everyhtin is arc consistant, this returns true
def set(k,i,j,board):
	#set the value
	board[i][j].value = k
	#set domain of vertical constraints
	for ci in range(9):
		if board[ci][j].value == 0:
			if not board[ci][j].rem(k):
				return False
	#set domain of horizontal constraints
	for cj in range(9):
		if board[i][cj].value == 0:
			if not board[i][cj].rem(k):
				return False
	#set domain of sub-square constraints
	seci = int(i/3)
	secj = int(j/3)
	for subi in range(seci*3,seci*3+3):
		for subj in range(secj*3,secj*3+3):
			if board[subi][subj].value == 0:
				if not board[subi][subj].rem(k):
					return False
	#all checks passed
	return True

#Recursive function that traverses the search space
#returns true if a legal filled version of the board has been found
def compute(board,depth):
	global stepNumber
	stepNumber += 1
	if stepNumber == 10000:
		print("10,000 steps...quiting")
		sys.exit()
	fail = True
	#traverse the board until the first empty cell is found
	for i in range(9):
		for j in range(9):
			if board[i][j].value == 0:
				#tries all options in the domain
				for k in board[i][j].options:
					newboard = deepcopy(board)
					#if the option does not lead to arc-inconsistancy, 
					#we recompute with the resulting board
					if set(k,i,j,newboard):
						tempboard, fail = compute(newboard,depth + 1)
						#apparenly a valid configuration was found in thie branch, pass it up to the parent
						if fail == False:
							return tempboard, fail
				#no options in the domain led to a valid configuration, 
				#we tried the wrong optiosn to get to this point
				return board, fail
	#the board is filled!  we have found a valid configuration
	return board, False

#convert board to a series of cells
for i in range(9):
	for j in range(9):
		newcell = deepcopy(cell())
		newcell.value = ord(board[i][j]) - 48
		board[i][j] = newcell


def superPrint(board):
	for i in range(9):
		for j in range(9):
			print(board[i][j].options, end=' ')
		print()

#Sets the domain for all empty cells
for i in range(9):
	for j in range(9):
		if board[i][j].value != 0:
			board[i][j].options = []
		set(board[i][j].value,i,j,board)

#start recursion
board, fail = compute(board,0)

#output findings
if args.raw:
	if fail:
		print("err")
	else:
		print(str(stepNumber))
else:
	if fail:
		print("No valid configurations (" + str(stepNumber) + " steps)")
	else:
		printBoard(board)
		print(str(stepNumber) + " steps")