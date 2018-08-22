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


class option():
	value = 0
	constrains = 20

def dom_reduce_contraint(domain,i):
	for dom in domain:
		if dom.value == i.value:
			dom.constrains -= 1
			return

def dom_remove(domain,i):
	for dom in domain:
		if dom.value == i.value:
			domain.remove(dom)
			return

class cell():
	value = 0
	#This keeps track of how many values this cell is constraining, 
	#so that we can use that as a seccondary key when sorting
	constrains = 20
	i = -1
	j = -1
	def __init__(self):
		#The domain for this cell
		self.domain = []
		for d in range(1,10):
			newOption = option()
			newOption.value = d
			self.domain.append(newOption)
	#removes option from possible options this cell could take
	#returns false if we have removed its last legal domain option, 
	#implying that whatever path led to the removal of the domain option is invalid
	def rem(self, i):
		dom_remove(self.domain,i)

		if self.value != 0 or len(self.domain) > 0:
			return True
		else:
			return False

def clearConstraining(k,i,j,board):
	dom_reduce_contraint(board[i][j].domain,k)
	#if board[i][j].domain.count(k) > 0:
	#	board[i][j].domain[board[i][j].domain.index(k)].constrains -= 1


def printBoard(board):
	for i in range(9):
		for j in range(9):
			print(board[i][j].value, end=' ')
		print()

def superPrint(board):
	for i in range(9):
		for j in range(9):
			print(board[i][j].constrains, end=' ')
		print()



#This is almost the same as Version B
#it is implied that placing k in cell i,j is legal, 
#it then forward checks all of its constraining cells (vertical, horizontal, sub-square)
#Since cell i,j is no longer empty, it is no longer constrined by any other empty cells
#We therefore update (-1) the #of constraints on all cells that had constrained i,j

#If any cell is not arc consistant, and the last domain option would be removed, this 
#returns false, otherwise, if everyhtin is arc consistant, this returns true
def set(k,i,j,board):
	#set the value
	board[i][j].value = k.value
	#set domain of vertical constraints
	for ci in range(9):
		if board[ci][j].value == 0 and board[ci][j].i != i:
			#update #of constraints
			board[ci][j].constrains -= 1
			clearConstraining(k,ci,j,board)
			if not board[ci][j].rem(k):
				return False
	#set domain of horizontal constraints
	for cj in range(9):
		if board[i][cj].value == 0 and  board[i][cj].j != j:
			#update #of constraints
			clearConstraining(k,i,cj,board)
			board[i][cj].constrains -= 1
			if not board[i][cj].rem(k):
				return False
	#set domain of sub-square constraints
	seci = int(i/3)
	secj = int(j/3)
	for subi in range(seci*3,seci*3+3):
		for subj in range(secj*3,secj*3+3):
			if subi != i and subj != j and board[subi][subj].value == 0:
				#update #of constraints
				clearConstraining(k,subi,subj,board)
				board[subi][subj].constrains -= 1
				if not board[subi][subj].rem(k):
					return False
	#all checks passed
	#superPrint(board)
	#print()
	return True


#These assist the sort function
def secKey(cell):
	return cell.constrains

def priKey(cell):
	return len(cell.domain)

#Converts the 2 dimentional board into a 1 dimentional list of cells
#This list will be sorted to make educated choices about what to chooose next
#only adds empty cells, so if no empty cells are found, this will return an empty list
def makeList(board):
	fullList = []
	for i in range(9):
		for j in range(9):
			if board[i][j].value == 0:
				fullList.append(board[i][j])
	return fullList


#Recursive function that traverses the search space
#returns true if a legal filled version of the board has been found
def compute(board, depth):
	global stepNumber
	stepNumber += 1
	if stepNumber == 10000:
		print("10,000 steps...quiting")
		sys.exit()
	fail = True

	#assemble the 1D list
	fullList = makeList(board)
	#If this is an empty list, all cells are filled and we have found a valid solution
	if len(fullList) == 0:
		return board, False

	#sorts the list by most constrained and then most constraining option
	fullList.sort(key = secKey, reverse = True)
	fullList.sort(key = priKey)
	#for a in fullList:
	#	print(a.constrains, end=' ')
	#print()
	#print()

	#traverse through the sorted list.  The most constrined values will now be chosen first
	for cell in fullList:
		#tries options in the domain, sorted by least constraining
		cell.domain.sort(key = secKey)
		for k in cell.domain:
			#if the option does not lead to arc-inconsistancy, 
					#we recompute with the resulting board
			newboard = deepcopy(board)
			if set(k,cell.i,cell.j,newboard):
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
		newcell.i = i
		newcell.j = j
		board[i][j] = newcell


#Sets the domain for all empty cells
for i in range(9):
	for j in range(9):
		if board[i][j].value != 0:
			for d in board[i][j].domain:
				if d.value == board[i][j].value:
					set(d,i,j,board)
			board[i][j].domain = []
		

#superPrint(board)
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
