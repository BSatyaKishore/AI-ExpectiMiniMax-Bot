# myAI.py
import sys, copy
from random import random, choice

def printX(*message):
	for msg in message:
		sys.stderr.write(repr(msg) + ' ') 
	sys.stderr.write('\n') 

is_chaos = False
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
	isOk = lambda x: True if x >= 0 and x < MAX  else False # and row[x] != '-'
	if kota:
		isOk = lambda x: True if x >= 0 and x < MAX  and row[x] != '-' else False
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

def best_1(x,y,is_horizontal,color,node):
	isOk = lambda x: True if x >= 0 and x < N  else False
	output = 0
	if is_horizontal:
		for i in range(y,N):
			if node[x][i] != '-':
				if node[x][i] == color:
					output = output+1
				else:
					break
		for i in range(1,y+1):
			if node[x][y-i] != '-':
				if node[x][y-i] == color:
					output = output+1
				else:
					break
		return output
	else:
		for i in range(x,N):
			if node[i][y] != '-':
				if node[i][y] == color:
					output = output+1
				else:
					break
		for i in range(1,x+1):
			if node[x-i][y] != '-':
				if node[x-i][y] == color:
					output = output+1
				else:
					break
		return output






def best_2(x,y,is_horizontal,color,node):
	isOk = lambda x: True if x >= 0 and x < N  else False
	if is_horizontal:
		i = x
		j = y+1
		output = 0
		while ( isOk(j) and node[i][j] == '-'):
			k = i
			while (node[k][j] == '-' and isOk(k+1)):
				if node[k+1][j] == color:
					output = output+1
				k = k+1
			k = i
			while (node[k][j] == '-' and isOk(k-1)):
				if node[k-1][j] == color:
					output = output+1
				k = k-1
			j = j+1
		j = y-1
		while (isOk(j) and node[i][j] == '-'):
			k = i
			while (node[k][j] == '-' and isOk(k+1)):
				if node[k+1][j] == color:
					output = output+1
				k = k+1
			k = i
			while (node[k][j] == '-' and isOk(k-1)):
				if node[k-1][j] == color:
					output = output+1
				k = k-1
			j = j-1	
		return output
	else:
		j = y
		i = x+1
		output = 0
		while (isOk(i) and node[i][j] == '-'):
			k = j
			while (isOk(k+1) and node[i][k] == '-'):
				if node[i][k+1] == color:
					output = output+1
				k = k+1
			k = j
			while (node[i][k] == '-' and isOk(k-1)):
				if node[i][k-1] == color:
					output = output+1
				k = k-1
			i = i+1
		i = x-1
		while (isOk(i) and node[i][j] == '-'):
			k = j
			while (node[i][k] == '-' and isOk(k+1)):
				if node[i][k+1] == color:
					output = output+1
				k = k+1
			k = j
			while (node[i][k] == '-' and isOk(k-1)):
				if node[i][k-1] == color:
					output = output+1
				k = k-1
			i = i-1
		return output

def color_color(node):
	vertical = []
	horizontal = []
	isOk = lambda x: True if x < N  else False
	for i in range(N):
		for j in range(N):
			if isOk(j+2):
				if ((node[i][j] == node[i][j+2]) and (node[i][j+1] == '-')):
					if (node[i][j] != '-'):
						vertical.append((i,j+1,node[i][j]))
			if isOk(i+2):
				if ((node[i][j] == node[i+2][j]) and (node[i+1][j] == '-')):
					if (node[i][j] != '-'):
						horizontal.append((i+1,j,node[i][j]))
	return (vertical,horizontal)

def main_best_2(node):
	co_co = color_color(node)
	main_output = 0
	for sa in co_co[0]:
		main_output = best_2(sa[0],sa[1],False,sa[2],node)
	for sa in co_co[1]:
		main_output = best_2(sa[0],sa[1],True,sa[2],node)
	return main_output

def main_best_1(node):
	co_co = color_color(node)
	main_output = 0
	for sa in co_co[0]:
		main_output = best_1(sa[0],sa[1],False,sa[2],node)
	for sa in co_co[1]:
		main_output = best_1(sa[0],sa[1],True,sa[2],node)
	return main_output

def Score(node):
	score = 0
	if is_chaos:
		for rowList in node:
			score += scoreHelp(rowList, True) + 0.2*main_best_2(node) + 0.4*main_best_1(node) #+ 0.25*scoreHelp(rowList, False)

		for col in range(0, N):
			colList = []
			for row in range(0, N):
				colList.append(node[row][col])
			score += scoreHelp(colList, True) + 0.2*main_best_2(node) + 0.4*main_best_1(node)#0.25*scoreHelp(colList, False)
	else:
		for rowList in node:
			score += scoreHelp(rowList, True) + 0.2*main_best_2(node) + 0.4*main_best_1(node)

		for col in range(0, N):
			colList = []
			for row in range(0, N):
				colList.append(node[row][col])
			score += scoreHelp(colList, True) + 0.2*main_best_2(node) + 0.4*main_best_1(node
)
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
	# if main_sum < 5:
	# 	alphabeta(board, 4, -10000, 10000, False, piece, 4, main_probs, main_sum)
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
	is_chaos = False
	playAsOrder()
elif(ROLE == 'CHAOS'):
	is_chaos = True
	playAsChaos()
else:
	print >> sys.stderr, 'I am not intelligent for this role: %s' %ROLE
	
printX ('--graceful exit by myAI--')

