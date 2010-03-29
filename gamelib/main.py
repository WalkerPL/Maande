'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import pygame
import random
import math

screen = pygame.display.set_mode((800, 600))

def drawtext(message, x, y, fontsize, color=(0,0,0)):
	#draws text on the screen. little wrapper for the font functions of pygame
	font = pygame.font.Font(None, fontsize)
	fontsurface = font.render(message, 0, color)
	screen.blit(fontsurface, (x, y))

class Player:
	#Player class is the basket and cart.
	def __init__(self):
		self.cart_x = 375
		self.cart_y = 555
		self.basket_x = 375
		self.basket_y = 405
		self.cart_image = pygame.image.load("./data/cart.png")
		self.basket_image = pygame.image.load("./data/basket.png")
		
	def update(self, mouse):
		self.basket_x += ((mouse - self.basket_x) / 2) - 13
		self.cart_x += (self.basket_x - self.cart_x) / 10
		if (self.basket_x - self.cart_x) < 50 & (self.basket_x - self.cart_x) > 0:
			#minor bugfix, you could move the basket 50px right without moving the cart, so now it's possible both ways
			self.cart_x += 1
		self.basket_y = 375 + (math.fabs(self.basket_x - self.cart_x) / 1.5)
		pygame.draw.line(screen, (0,0,0), ((self.basket_x + 25), (self.basket_y + 25)), ((self.cart_x + 25), (self.cart_y + 5)), 12)
		screen.blit(self.cart_image, (self.cart_x, self.cart_y))
		screen.blit(self.basket_image, (self.basket_x, self.basket_y))

def main():
	#starting code
	pygame.init()
	background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
	points = 0
	p = Player()
	ticker = pygame.time.Clock()
	
	while True:
		ticker.tick(40)
		screen.fill(background_color)
		event = pygame.event.poll() #check user input
		if event.type == pygame.QUIT:
			return False #end a game when clicking on x
		mouse, garbage = pygame.mouse.get_pos()
		p.update(mouse)
		pygame.display.flip()