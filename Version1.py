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

F = open(args.inputFile)

#keeps track of the number of variable assignments
stepNumber = 0

#setup empty board
board=[[0 for i in range(10)] for j in range(10)]

#import board as stirng
i=0
for line in F:
  board[i] = line.split()
  i+=1
  if i==10:
  	break;

F.close()

class cell():
	value = 0

#convert board to a series of cells
for i in range(9):
	for j in range(9):
		newcell = cell()
		newcell.value = ord(board[i][j]) - 48
		board[i][j] = newcell

def printBoard(board):
	for i in range(9):
		for j in range(9):
			print(board[i][j].value, end=' ')
		print()

#This checks if the move of val at i,j on the board would be legal
#if any conflict is found, return false, otherwise return true
def isLegal(val,i,j,board):
	#looks for a vertical conflict
	for ci in range(9):
		if i != ci and board[ci][j].value == val:
			return False
	#looks for a horizontal conflict
	for cj in range(9):
		if j != cj and board[i][cj].value == val:
			return False
	#determines the sub-square that i,j is in
	seci = int(i/3)
	secj = int(j/3)
	#determines sub-square conflicts
	for subi in range(seci*3,seci*3+3):
		for subj in range(secj*3,secj*3+3):
			if not(i==subi and j==subi) and board[subi][subj].value == val:
				return False
	return True


#Recursive function that traverses the search space
#returns true if a legal filled version of the board has been found
def compute(board,depth):
	global stepNumber
	stepNumber += 1
	if stepNumber == 10000:
		print("10,000 steps...quiting")
		sys.exit()
	#makes the copy of the board to work with
	newboard = deepcopy(board)
	fail = True
	#traverse the board until the first empty cell is found
	for i in range(9):
		for j in range(9):
			if newboard[i][j].value == 0:
				#try all values on the cell
				for k in range(1,10):
					#if the move is legal, the move is made and we compute on the coresponding board
					if isLegal(k,i,j,newboard):
						newboard[i][j].value = k
						tempboard, fail = compute(newboard,depth + 1)
						if fail == False:
							#apparenly a valid configuration was found in thie branch, pass it up to the parent
							return tempboard, fail
				#all values were tested, none of which led to a valid configuration
				#we are therefore in the wrong branch
				return newboard, fail
	#the board is filled!  we have found a valid configuration
	return board, False


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
