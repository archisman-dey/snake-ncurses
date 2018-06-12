"""
Snake game written in Python3 using curses on linux
By Archisman Dey
"""

import curses as cp
import random
import time
import sys

#should be at least 10 and 30 to be playable
height = 20
length = 56

class Snake(object) :
	"""Defines body, direction, alive, expand of a snake"""

	def __init__(self):
		mid_x = length//2
		mid_y = height//2

		self.direction = "RIGHT"
		self.alive = True
		self.expand = False

		#body stores coordinates of the snake
		self.body = [(mid_y,mid_x-1), (mid_y,mid_x), (mid_y,mid_x+1)]

	def checkCollisions(self):
		if len(self.body) > len(set(self.body)) :
			self.alive = False

	def move(self, direction):
		"""Moves the snake UP, DOWN, RIGHT, or LEFT"""
		if direction == "RIGHT" :
			if self.body[-1][1] > length-2 :
				self.alive = False
				return
			elif self.direction == "LEFT":
				return
			else :
				self.body.append((self.body[-1][0], self.body[-1][1]+1))
				self.direction = direction
		
		elif direction == "LEFT" :
			if self.body[-1][1] < 1 :
				self.alive = False
				return
			elif self.direction == "RIGHT" :
				return
			else :
				self.body.append((self.body[-1][0], self.body[-1][1]-1))
				self.direction = direction

		elif direction == "UP" :
			if self.body[-1][0] < 1 :
				self.alive = False
				return
			elif self.direction == "DOWN" :
				return
			else :
				self.body.append((self.body[-1][0]-1, self.body[-1][1]))
				self.direction = direction

		elif direction == "DOWN" :
			if self.body[-1][0] > height-2 :
				self.alive = False
				return
			elif self.direction == "UP" :
				return
			else :
				self.body.append((self.body[-1][0]+1, self.body[-1][1]))
				self.direction = direction

		if self.expand == False :
			del(self.body[0])
		else :
			self.expand = False

class SnakeGame(object):
	"""defines score, food, snake"""
	
	def __init__(self):
		self.score = 0
		self.food = () #tuple storing coordinates and type of food
		#example : (4,5,'*')

		self.screen = cp.initscr()

		cp.noecho()
		cp.cbreak()
		cp.curs_set(False)

		self.mainScreen = cp.newwin(height, length, 1, 0)
		self.titleScreen = cp.newwin(1, length, 0, 0)
		self.mainScreen.border(0)

		self.mainScreen.keypad(True)
		self.titleScreen.keypad(True)

		self.snake = Snake()

		self.display(food = True)

		self.main()

	def main(self) :
		self.titleScreen.addstr(0, length//2-3, " SNAKE ")
		self.titleScreen.addstr(0, length-10 , "Q TO EXIT")
		self.titleScreen.addstr(0, 1, "SCORE : " + str(self.score))
		self.titleScreen.refresh()

		cp.flushinp()

		#controls the speed of the snake
		self.mainScreen.timeout(150 - len(self.snake.body))
		key = 261	#right arrow key

		while key != 113 and key != 811 : #113 : q and 811 : Q
			
			if key == 261 : 			#261 : right arrow key
				self.snake.move("RIGHT")
			elif key == 260 :			#left arrow
				self.snake.move("LEFT")
			elif key == 259 :			#up arrow
				self.snake.move("UP")
			elif key ==  258:			#down arrow
				self.snake.move("DOWN")
			else :
				self.snake.move(self.snake.direction)

			self.snake.checkCollisions()

			if self.snake.alive == False :
				time.sleep(0.5)
				self.gameover()

			key = self.mainScreen.getch()

			if self.food[0:2] in self.snake.body :
				if self.food[2] == '*': 
					self.score += 5
				else :
					self.score += 10

				self.snake.expand = True
				self.titleScreen.addstr(0, 1, "SCORE : " + str(self.score))
				self.titleScreen.refresh()
				self.display(food = True)
			else :
				self.display()

		self.gameover()


	def display(self, food = False):
		self.mainScreen.erase()
		self.mainScreen.border(0)

		if food == True :
			y = random.randint(1, height-2)
			x = random.randint(1, length-2)
			randomType = random.randint(1,100)
			foodType = '*'
			if (randomType > 80):
				foodType = '@'

			self.food = (y,x, foodType)

			while self.food in self.snake.body :
				y = random.randint(1, height-2)
				x = random.randint(1, length-2)
				self.food = (y,x, foodType)

		self.mainScreen.addstr(self.food[0], self.food[1], self.food[2])

		for points in self.snake.body :
			self.mainScreen.addstr(points[0], points[1], '$')

		self.mainScreen.refresh()

	def gameover(self):
		self.mainScreen.erase()
		self.mainScreen.border(0)

		self.mainScreen.addstr(height//2, length//2-4, "GAME OVER")
		self.mainScreen.refresh()
		time.sleep(3)	#delay of 3 seconds after gameover until game exits
		self.close()

	def close(self):
		"""closing curses"""
		cp.curs_set(True)
		self.mainScreen.keypad(False)
		cp.nocbreak()
		self.titleScreen.keypad(False)
		cp.echo()
		cp.endwin()
		print("SCORE : " + str(self.score))
		sys.exit(0)

print("There are two kinds of food : * and @ :\n\t* brings you 5 points\n\t@ brings you 10 points\nNavigate the snake using the arrow keys and avoid hitting itself or the walls!\nEnjoy!")
time.sleep(2)

SnakeGame()