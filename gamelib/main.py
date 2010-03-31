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

    def update(self, player):
        self.y += self.speed
        
        if (self.x < player.basket_x + 40) and (self.x > player.basket_x - 22) and (self.y < player.basket_y) and (self.y > player.basket_y - 15) and self.catched == False:
        	self.catched = 1
        	return self.points
        
        if self.catched == False:
        	screen.blit(self.image, (self.x, self.y))
        return 0

def main():
	#starting code
	pygame.init()
	background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
	points = 0
	level = 0
	caught = 0
	p = Player()
	items = []
	items.append(Item())
	ticker = pygame.time.Clock()
	menu = True
	level_change = 1 #0 - no change in this loop, 1 - level +1, 2 - game over
	
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
		    
		    if level_change == 1:
		    	background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
		    	level += 1
		    	pygame.time.set_timer(pygame.USEREVENT+1, 5000/level)
		    	time_passed = 0
		    	level_change = 0
		    elif level_change == 2:
		    	pygame.time.wait(3000)
		    	return False
		    if event.type == pygame.USEREVENT+1:
		        items.append(Item())
		    for item in items:
		        won = item.update(p)
		        points += won
		        if won > 0:
		        	caught += 1
		        if won > 0 or item.y > 650:
		            items.remove(item)
		    mouse, garbage = pygame.mouse.get_pos()
		    p.update(mouse)
		    time_passed += ticker.get_time()
		    if time_passed >= 65000 and caught >= 9 * level:
		    	level_change = 1
		    	caught = 0
		    elif time_passed >= 65000 and caught < 9 * level:
		    	level_change = 2
		    	pygame.draw.rect(screen, (0,0,0), pygame.Rect(270, 270, 300, 60))
		    	drawtext("GAME OVER", 283, 280, 64, (255, 0, 0))		    	
		    
		    # Draw the upper info
		    pygame.draw.line(screen, (background_color[0] - 50, background_color[1] - 50, background_color[2] - 50), (0,29), (800,29), 58)
		    pygame.draw.line(screen, (155, 155, 255), (265,0), (265, 58), 1)
		    pygame.draw.line(screen, (155, 155, 255), (535,0), (535, 58), 1)
		    pygame.draw.line(screen, (155, 155, 255), (0,0), (800,0), 1)
		    pygame.draw.line(screen, (155, 155, 255), (0,59), (800,59), 1)
		    drawtext("Points: %d" % points, 15, 15, 48, (255, 255, 255))
		    drawtext("Level: %d" % level, 550, 15, 48, (255, 255, 255))
		    drawtext("ESCAPE to pause / move to the main menu", 280, 10, 18, (255, 255, 255))
		    drawtext("You caught: %s" % caught, 280, 35, 22, (255, 255, 255))
		    drawtext("To get through: %s" % (9 * level), 400, 35, 22, (255, 255, 255))
		    drawtext("%s s" % ((65000 - time_passed)/1000), 720, 15, 48, (255, 255, 255))
		    drawtext("fps: %.4s" %ticker.get_fps(), 735, 580, 18, (255, 255, 255))

		pygame.display.flip()
