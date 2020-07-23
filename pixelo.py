import math
import pygame
import random

WIDTH = 800
HEIGHT = 600
OFFSET_X = 350
OFFSET_Y = 150
BLOCK_SPACE = 400
ROW = 20
BLOCK_SIZE = math.floor(BLOCK_SPACE / ROW)


pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])

class Block:
	def __init__(self):
		self.bomb = False
		self.mark = False
		self.guess = False
		self.pos = [0,0]

grid = [[Block() for n in range(ROW)] for n in range(ROW)]
cursor = Block()

# Place each block on the grid space evenly and randomly place bombs
def createGrid():
	for i in range(ROW):
		for j in range(ROW):
			grid[j][i].pos[0] = OFFSET_X + j * BLOCK_SIZE
			grid[j][i].pos[1] = OFFSET_Y + i * BLOCK_SIZE

			if (random.randint(0, 2)) == 2:
				grid[j][i].bomb = True

def moveCursor(Input):
	print(Input)
	if(Input == 276): # left
		cursor.pos[1] -= 1

		if(cursor.pos[1] < 0):
			cursor.pos[1] = ROW - 1
	elif(Input == 273): # Up
		cursor.pos[0] -= 1

		if(cursor.pos[0] < 0):
			cursor.pos[0] = ROW - 1
	elif(Input == 275): # Right
		cursor.pos[1] += 1

		if(cursor.pos[1] > ROW - 1):
			cursor.pos[1] = 0
	elif(Input == 274): # Down
		cursor.pos[0] += 1

		if(cursor.pos[0] > ROW - 1):
			cursor.pos[0] = 0
	elif(Input == 32): # Space
		grid[cursor.pos[1]][cursor.pos[0]].guess = True

# Sees if the mouse click hit a block, then return it's x and y pos.
# If no hit, return (-1, -1).
def checkClick(mousePos):
	# print(mousePos)
	if(mousePos[0] > OFFSET_X and mousePos[1] > OFFSET_Y):
		for i in range(ROW):
			for j in range(ROW):
				difX = mousePos[0] - grid[j][i].pos[0]

				if difX > 0 and difX < BLOCK_SIZE:
					difY = mousePos[1] - grid[j][i].pos[1]

					if difY > 0 and difY < BLOCK_SIZE:
						# grid[j][i].bomb = True
						# grid[j][i].guess = True
						return (i, j)

	return (-1, -1)

def draw():
	"""
	for i in range(ROW):
		for j in range(ROW):
			print(grid[j][i].pos)
	print("DONE")
	"""

	# Background of the blocks
	pygame.draw.rect(screen, (50, 50, 50), (OFFSET_X, OFFSET_Y, BLOCK_SPACE, BLOCK_SPACE))

	incX = OFFSET_X
	incY = OFFSET_Y

	# Blocks
	for i in range(ROW):
		incX = OFFSET_X
		for j in range(ROW):
			if grid[j][i].mark: # if block is marked as not a bomb
				pygame.draw.rect(screen, (100, 100, 100), (incX, incY, BLOCK_SIZE, BLOCK_SIZE))
			elif grid[j][i].bomb and grid[j][i].guess: # if block is a bomb and is guessed
				pygame.draw.rect(screen, (255, 100, 100), (incX, incY, BLOCK_SIZE, BLOCK_SIZE))
			elif not grid[j][i].bomb and grid[j][i].guess: # if block is not a bomb and is guessed
				pygame.draw.rect(screen, (0, 0, 0), (incX, incY, BLOCK_SIZE, BLOCK_SIZE))
			else: # if block is not guessed yet and not marked
				pygame.draw.rect(screen, (255, 255, 255), (incX, incY, BLOCK_SIZE, BLOCK_SIZE))

			# Drawing the outlines for each block: Top and Left. I draw very bottom and right after loops
			pygame.draw.rect(screen, (200, 200, 200), (incX, incY, BLOCK_SIZE, 1)) # top and bottom grey outline
			pygame.draw.rect(screen, (200, 200, 200), (incX, incY, 1, BLOCK_SIZE)) # left and right grey outline

			incX += BLOCK_SIZE
		incY += BLOCK_SIZE

	pygame.draw.rect(screen, (200, 200, 200), (incX - BLOCK_SPACE, incY, BLOCK_SPACE, 1)) # bottom most line
	pygame.draw.rect(screen, (200, 200, 200), (incX, incY - BLOCK_SPACE, 1, BLOCK_SPACE)) # right most line

	# Cursor
	pygame.draw.rect(screen, (0, 200, 0), (cursor.pos[1] * BLOCK_SIZE + OFFSET_X, cursor.pos[0] * BLOCK_SIZE + OFFSET_Y, BLOCK_SIZE, 3)) # top most line
	pygame.draw.rect(screen, (0, 200, 0), (cursor.pos[1] * BLOCK_SIZE + OFFSET_X, cursor.pos[0] * BLOCK_SIZE + OFFSET_Y + BLOCK_SIZE - 2, BLOCK_SIZE, 3)) # bottom most line
	pygame.draw.rect(screen, (0, 200, 0), (cursor.pos[1] * BLOCK_SIZE + OFFSET_X, cursor.pos[0] * BLOCK_SIZE + OFFSET_Y, 3, BLOCK_SIZE)) # left most line
	pygame.draw.rect(screen, (0, 200, 0), (cursor.pos[1] * BLOCK_SIZE + OFFSET_X + BLOCK_SIZE - 2, cursor.pos[0] * BLOCK_SIZE + OFFSET_Y, 3, BLOCK_SIZE)) # right most line


	pygame.display.update()

def main():
	createGrid()

	running = True
	while running:
		# Keyboard and Mouse event handling
		for event in pygame.event.get():
			# Mouse events
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # left click
				mouseTup = checkClick(pygame.mouse.get_pos())

				if(mouseTup[0] > -1): # Block was clicked
					if(grid[mouseTup[1]][mouseTup[0]].mark): # Unmark if marked already
						grid[mouseTup[1]][mouseTup[0]].mark = False
					else:
						grid[mouseTup[1]][mouseTup[0]].guess = True
				else: # Nothing was clicked. Do nothing
					print("Nothing was clicked")
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: # right click
				mouseTup = checkClick(pygame.mouse.get_pos())

				if(mouseTup[0] > -1): # Block was clicked
					if(grid[mouseTup[1]][mouseTup[0]].guess): # Block already guessed
						pass
					else:
						grid[mouseTup[1]][mouseTup[0]].mark = True
				else: # Nothing was clicked. Do nothing
					print("Nothing was clicked")

			# Keyboard events
			if event.type == pygame.KEYDOWN:
				moveCursor(event.key)



		""" fill screen with black before drawing """
		screen.fill((0, 0, 0))

		""" drawing everything """
		draw()

		""" flip the display as is needed """
		pygame.display.flip()
		pygame.time.wait(50)

main()
pygame.quit()
