import curses
import random
from time import sleep

# This function sets up the board and the first square as well as the stack
def init():
	# The format of the board is a 2x2 matrix st board[y][x] = square = [visited, top wall, right, bottom, left]
	# The board is unaffected by the square skipping. We handle that on the drawing side
	board = [[ [0, 1, 1, 1, 1] for i in range(curses.COLS//2)] for j in range(curses.LINES//2)]
	stack = []
	# Start at a random point
	y, x = random.randrange(0, curses.LINES//2), random.randrange(0, curses.COLS//2)
	stack.append([y, x])
	board[y][x][0] = 1
	return board, stack


# Takes in the board and the stack at a particular point applies one iteration of the RDFS algorithm and
# returns the new board and stack
def iterationRandomDFS(board, stack):
	y, x = stack[-1]

	# Check if the current square has any unvisited neighbors
	unvisitedNeighbors = []
	if(y > 0 and board[y-1][x][0] == 0):
		unvisitedNeighbors.append([y-1, x])
	if(y < curses.LINES//2-1 and board[y+1][x][0] == 0):
		unvisitedNeighbors.append([y+1, x])
	if(x > 0 and board[y][x-1][0] == 0):
		unvisitedNeighbors.append([y, x-1])
	if(x < curses.COLS//2-1 and board[y][x+1][0] == 0):
		unvisitedNeighbors.append([y, x+1])

	flag= False
	# Choose one randomly and remove the wall between it and the current square and append the new square to the stack
	# else backtrack
	if len(unvisitedNeighbors) > 0:
		nextSquare = random.choice(unvisitedNeighbors)
		if nextSquare[0] < y:
			board[y][x][1] = 0
			board[nextSquare[0]][nextSquare[1]][3] = 0
		elif nextSquare[0] > y:
			board[y][x][3] = 0
			board[nextSquare[0]][nextSquare[1]][1] = 0
		elif nextSquare[1] < x:
			board[y][x][4] = 0
			board[nextSquare[0]][nextSquare[1]][2] = 0
		elif nextSquare[1] > x:
			board[y][x][2] = 0
			board[nextSquare[0]][nextSquare[1]][4] = 0
		# This indentation messed me up. Make sure its not part of the elif
		y, x = nextSquare
		stack.append([y, x])
		board[y][x][0] = 1
	else:
		stack.pop()
		if(len(stack)):
			op = board[stack[-1][0]][stack[-1][1]]
			op[0] += 1

	return board, stack



def ticker(stdscr):
	# Clear screen
	stdscr.clear()
	# curses.curs_set(0)

	board, stack = init()

	while len(stack) > 0:
		board, stack = iterationRandomDFS(board, stack)
		if(len(stack)):		# To deal with the case that RDFS pops the last value off the stack
			posy = 2 * stack[-1][0] + 1
			posx = 2 * stack[-1][1] + 1
			op = board[stack[-1][0]][stack[-1][1]]
			# Print the connecting lines if there is no wall between the squares
			for i in range(1, 5):
				if op[i] == 0:
					if i == 1:
						stdscr.addstr(posy-1, posx, '\u2B1C', curses.color_pair((op[0])%7))
					elif i == 2:
						stdscr.addstr(posy, posx+1, '\u2B1C', curses.color_pair((op[0])%7))
					elif i == 3:
						stdscr.addstr(posy+1, posx, '\u2B1C', curses.color_pair((op[0])%7))
					elif i == 4:
						stdscr.addstr(posy, posx-1, '\u2B1C', curses.color_pair((op[0])%7))
			if(not(posy == curses.LINES-1 and posx == curses.COLS-1)):
				stdscr.addstr(posy, posx, '\u2B1C', curses.color_pair((op[0])%7))
		stdscr.refresh()
		sleep(0.01 * random.random())


	stdscr.getkey()
	# return 1



def main(stdscr):
	# We're going to only use half the squares, we write to one square and then skip to the next
	# we start at (1,1) and then keep skipping one in each direction to get to the next one
	stdscr.border(0)

	# If color, then initialize the color pairs
	if curses.has_colors():
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
		curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLUE)
		curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)
		curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_CYAN)
		curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
		curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
		curses.init_pair(7, curses.COLOR_RED, curses.COLOR_RED)

	res = ticker(stdscr)
	# while res == 1:
	# 	res = ticker(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)