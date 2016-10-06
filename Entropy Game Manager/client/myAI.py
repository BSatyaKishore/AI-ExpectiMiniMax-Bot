# myAI.py
import sys, copy
from random import random, choice

def printX(*message):
	for msg in message:
		sys.stderr.write(repr(msg) + ' ') 
	sys.stderr.write('\n') 

N = int(raw_input())
ROLE = raw_input()
board = []
for i in range(0, N):
	boardRow = []
	for j in range(0, N):
		boardRow.append('-')
	board.append(boardRow)
main_probs = [5,5,5,5,5]
# global main_sum
main_sum = 25.0

def isGameOver(node):
	for i in range(0, N):
		for j in range(0, N):
			if (node[i][j] == '-'):
				return False
	return True

def scoreHelp(row, kota):
	MAX = len(row)
	isOk = lambda x: True if x >= 0 and x < MAX else False # and row[x] != '-'
	if kota:
		isOk = lambda x: True if x >= 0 and x < MAX and row[x] != '-' else False
	score = 0 
	for ind in range(1, MAX):
		# epicenter b/w ind-1 and ind
		length = 0
		scoreX = 0
		right = ind
		left = ind - 1
		while isOk(right) and isOk(left) and row[left] == row[right]:
			scoreX += (length+2); length += 2; right += 1; left -= 1
		score += scoreX
		
		# epicenter at ind
		length = 1 
		scoreX = 0
		right = ind + 1
		left = ind - 1
		while isOk(right) and isOk(left) and row[left] == row[right]:
			scoreX += (length + 2); length += 2; right += 1; left -= 1
		score += scoreX
	return score

def Score(node):
	score = 0
	for rowList in node:
		score += scoreHelp(rowList, True) #+ 0.3*scoreHelp(rowList, False)
	
	for col in range(0, N):
		colList = []
		for row in range(0, N):
			colList.append(node[row][col])
		score += scoreHelp(colList, True) #+ 0.3*scoreHelp(colList, False)

	return score

def isGameOver(node):
	for i in range(0, N):
		for j in range(0, N):
			if (node[i][j] == '-'):
				return False
	return True

def heuristicOrder(a, b, c, d, board):
	change = 0
	board1 = copy.deepcopy(board)
	board1[c][d] = board[a][b]
	board1[a][b] = '-'
	return Score(board1)#-Score(board))

#TODO: change it to make it work as expected
def heuristicChoas(a,b,piece,board):
	change = 0
	board1 = copy.deepcopy(board)
	board1[a][b] = piece
	return 0-Score(board1)

def getOrderChild(child,node):
	my_board = copy.deepcopy(node)
	my_board[child[0]][child[1]] = '-' #node[child[2]][child[3]]
	my_board[child[2]][child[3]] = node[child[0]][child[1]]
	return my_board

def getChoasChild(child,node):
	my_board = copy.deepcopy(node)
	child1 = copy.deepcopy(child)
	my_board[child1[0]][child1[1]] = child1[2]
	return my_board

def getopensquares(node):
	openSquares=[]
	for x in range(N):
		for y in range(N):
			if node[x][y]=="-":
				openSquares.append((x,y))
	return openSquares

def getclosedsquares(node):
	closedSquares=[]
	for x in range(N):
		for y in range(N):
			if node[x][y] != "-":
				closedSquares.append((x,y))
	return closedSquares


#TODO: Add a heuristic and sort the getPossibleOrderMoves
def getPossibleOrderMoves(x, y, node):
	possibleMoves = []
	#possibleMoves.append((x,y,x,y))
	for iterator in range(x-1,-1,-1):
		if node[iterator][y]=='-':
			possibleMoves.append((x, y, iterator,y))
		else:
			break

	for iterator in range(y-1,-1,-1):
		if node[x][iterator]=='-':
			possibleMoves.append((x, y,x,iterator))
		else:
			break

	for iterator in range(x+1,N):
		if node[iterator][y]=='-':
			possibleMoves.append((x, y,iterator,y))
		else:
			break

	for iterator in range(y+1,N):
		if node[x][iterator]=='-':
			possibleMoves.append((x, y, x,iterator))
		else:
			break
	possibleMoves.append((x,y,x,y))
	return possibleMoves

def orderChildern(node):
	# write the code
	output = []
	for i in getclosedsquares(node):
		output = output + getPossibleOrderMoves(i[0],i[1], node)
	#output.sort(key=lambda tup: heuristicOrder(tup[0],tup[1],tup[2],tup[3],node))
	return output

def chaosChildern(piece, node):
	# redefine choice function so that alpha-beta pruning will be effective
	openSquares = getopensquares(node)
	output = []
	for i in openSquares:
		output.append((i[0],i[1],piece))
	# output.sort(key = lambda tup: heuristicChoas(i[0],i[1],piece,board))
	return output


output_node = (1,2,3,2)
pieces = ['A','B','C','D','E']

def alphabeta(node, depth, a, b, maximizingPlayer, random, depth_, probs, sum_):
	# check if it is leaf node
	global output_node
	if (depth == 0 or isGameOver(node)):
		#printNode(node)
		return Score(node)
	else:
		# Play
		if (maximizingPlayer):
			v = -10000
			for child in orderChildern(node):
				alpha_beta = alphabeta(getOrderChild(child,node), depth-1, a, b, False, '-', depth_, probs, sum_)
				if depth_ == depth:
					if v < alpha_beta:
						output_node = copy.deepcopy(child)
				v = max(v, alpha_beta)
				a = max(a, v)
				if (b <= a):
					break
			return v
		elif random == '-':
			v = 0
			for i in range(len(probs)):
				if (probs[i] != 0):
					probs_new = copy.deepcopy(probs)
					probs_new[i] = probs[i] - 1
					v = v + ((probs[i]/sum_) * alphabeta(node, depth, a, b, False, pieces[i], depth_, probs_new , (sum_ -1 )))
			return v
		else:
			v = 10000
			for child in chaosChildern(random, node):
				alpha_beta = alphabeta(getChoasChild(child,node), depth-1, a, b, True, '-', depth_, probs, sum_)
				if depth_ == depth:
					if v > alpha_beta:
						output_node = copy.deepcopy(child)
				v = min(v, alpha_beta)
				b = min(b, v)
				if (b <= a):
					break
			return v


TEXTCONV = {'A': 'R', 'B': 'C', 'C': 'G','D':'B', 'E':'Y', '-':'-'}

def chaosAI(piece):
	global main_probs, main_sum
	main_probs[ord(piece)-ord('A')] = main_probs[ord(piece)-ord('A')]-1
	main_sum = main_sum-1
	# if main_sum > 7:
	# 	alphabeta(board, 3, -10000, 10000, False, piece, 3, main_probs, main_sum)
	# elif main_sum > 4:
	# 	alphabeta(board, 4, -10000, 10000, False, piece, 4, main_probs, main_sum)
	# else:
	#  	alphabeta(board, 4,-1000,1000,True,'-',4, main_probs, main_sum) #'''8-main_sum'''
	alphabeta(board, 3, -10000, 10000, False, piece, 3, main_probs, main_sum)
	my_output = copy.deepcopy(output_node)
	return (my_output[0],my_output[1])

def orderAI():
	#global board,main_probs,main_sum
	#global output_node
	# initilize this
	# alphabeta(node, depth, a, b, maximizingPlayer, random, depth_, probs, sum_)
	#printX("hi", board)
	# if main_sum > 7:
	# 	alphabeta(board, 3, -10000, 10000, True, '-', 3, main_probs, main_sum)
	# elif main_sum > 4:
	# 	alphabeta(board, 4, -10000, 10000, True, '-', 4, main_probs, main_sum)
	# else:
	# 	alphabeta(board, 8-main_sum,-1000,1000,True,'-',8-main_sum, main_probs,main_sum)
	#board = getOrderChild(output_node,board)
	alphabeta(board, 3, -10000, 10000, True, '-', 3, main_probs, main_sum)
	my_output = copy.deepcopy(output_node)
	return (my_output[0],my_output[1],my_output[2],my_output[3])


## --------------------
import os, sys
sys.path.insert(0, os.path.realpath('../utils'))
from log import *

COLORS = [bcolors.OKRED, bcolors.OKCYAN, bcolors.OKGREEN, bcolors.OKBLUE, bcolors.OKYELLOW, bcolors.OKWHITE]
def color(tile): # character
	index = ord(tile) - ord('A')
	if (tile == '-'):
		index = 5
	return COLORS[index] + TEXTCONV[tile] + bcolors.ENDC

def printBoard():
	#printX("printing board")
	for x in xrange(N):
		print >>sys.stderr,  "".join( list( map( lambda x: color(x), board[x] ) ) )
	print >>sys.stderr, '\n'

def printNode(node):
	printX("Score", Score(node))
	for x in xrange(N):
		print >>sys.stderr,  "".join( list( map( lambda x: color(x), node[x] ) ) )
	print >>sys.stderr, '\n'


# returns if the move was successful or not
def makeChaosMove(x, y, color):
	global board
	if (board[x][y] != '-'):
		return False
	board[x][y] = color 
	return True
	
# returns if the move was successful or not
#TODO: check if we can move using the rules or not.
def makeOrderMove(a, b, c, d):
	global board
	if (c == a and b == d):
		return True
	board[c][d] = board[a][b]
	board[a][b] = '-'
	return True

def playAsOrder():
	global board
	printX('ORDER')
	while True:
		#printBoard()
		line = raw_input()
		# printX ('LINE:', line)
		(x, y, color) = line.split(' ')
		(x, y) = (int(x), int(y))
		board[x][y] = color
		if (isGameOver(board)):
			return
	
		(a, b, c, d) = orderAI()
		#printX((a,b,c,d))
		#printBoard()
		makeOrderMove(a, b , c, d)
		#printBoard()
		print '%d %d %d %d' % (a, b, c, d)
		sys.stdout.flush()

	
def playAsChaos():
	global board
	printX('CHAOS')
	color = raw_input()
	(x, y) = (0,0)#chaosAI(color)
	board[x][y] = color
	print '%d %d' %(x, y)
	#printBoard()

	while True:
		if (isGameOver(board)):
			return

		his_move = raw_input()
		# printX ('his move: %s'%his_move)
		(a, b, c, d) = map(lambda x: int(x), his_move.split(' '))
		makeOrderMove(a, b, c, d)
		color = raw_input()
		(x, y) = chaosAI(color)
		board[x][y] = color
		# printBoard()
		print '%d %d' %(x, y)
		sys.stdout.flush()
			

if (ROLE == 'ORDER'):
	playAsOrder()
elif(ROLE == 'CHAOS'):
	playAsChaos()
else:
	print >> sys.stderr, 'I am not intelligent for this role: %s' %ROLE
	
printX ('--graceful exit by myAI--')

