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
		#next 4 lines prevent the basket from moving too far from the cart
		if (self.basket_x - self.cart_x) > 100:
			self.basket_x = self.cart_x + 100
		if (self.basket_x - self.cart_x) < -100:
			self.basket_x = self.cart_x - 100
		self.basket_y = 425 + (math.fabs(self.basket_x - self.cart_x) / 1.5)
		pygame.draw.line(screen, (0,0,0), ((self.basket_x + 25), (self.basket_y + 25)), ((self.cart_x + 25), (self.cart_y + 5)), 12)
		screen.blit(self.cart_image, (self.cart_x, self.cart_y))
		screen.blit(self.basket_image, (self.basket_x, self.basket_y))
						

class Item:

    def __init__(self):
        items_list = ({"name": "obj0", "points": 10, "speed": 2}, {"name": "obj1", "points": 10, "speed": 2})

        item = random.choice(items_list)        
        self.x = random.randint(20, 780)
        self.y = random.randint(0, 3)
        self.image = pygame.image.load("./data/items/%s.png" % item["name"])
        self.points = item["points"]
        self.speed = item["speed"]
        self.catched = False

    def update(self, points, player):
        self.y += self.speed
        if (self.x < player.basket_x + 40) and (self.x > player.basket_x - 22) and (self.y < player.basket_y) and (self.y > player.basket_y - 15) and self.catched == False:
        	self.catched = 1
        	points += self.points
        	print "Points: %s \n" %points
        if self.catched == False:
        	screen.blit(self.image, (self.x, self.y))

def main():
	#starting code
	pygame.init()
	background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
	points = 0
	p = Player()
	item = Item()
	ticker = pygame.time.Clock()
	menu = True
	
	while True:
		ticker.tick(40)
		screen.fill(background_color)
		event = pygame.event.poll() #check user input
		if event.type == pygame.QUIT:
			return False #end a game when clicking on x

		if menu:
		    drawtext("Do you want to enter the game?", 100, 100, 30, (255, 255, 255))
		    drawtext("Press ENTER or ESCAPE", 100, 200, 40, (255, 255, 255))
		    if event.type == pygame.KEYDOWN:
		        if event.key == pygame.K_RETURN:
		            menu = False
		        elif event.key == pygame.K_ESCAPE:
		            return False

		elif not menu and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
		    menu = True

		else:
		    item.update(points, p)
		    mouse, garbage = pygame.mouse.get_pos()
		    p.update(mouse)

		pygame.display.flip()
