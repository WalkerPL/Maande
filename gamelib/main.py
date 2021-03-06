'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import pygame
from random import randint, choice
from math import fabs

def drawtext(message, x, y, fontsize, color=(0,0,0)):
	# draws text on the screen. little wrapper for the font functions of pygame
	font = pygame.font.Font(None, fontsize)
	fontsurface = font.render(message, 1, color)
	screen.blit(fontsurface, (x, y))

class Player:
	# Player class is the basket and cart.
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
			# minor bugfix, you could move the basket 50px right without moving the cart, so now it's possible both ways
			self.cart_x += 1
		# next 4 lines prevent the basket from moving too far from the cart
		if (self.basket_x - self.cart_x) > 100:
			self.basket_x = self.cart_x + 100
		if (self.basket_x - self.cart_x) < -100:
			self.basket_x = self.cart_x - 100
		self.basket_y = 425 + (fabs(self.basket_x - self.cart_x) / 1.5)
		pygame.draw.line(screen, (0,0,0), ((self.basket_x + 25), (self.basket_y + 25)), ((self.cart_x + 25), (self.cart_y + 5)), 12)
		screen.blit(self.cart_image, (self.cart_x, self.cart_y))
		screen.blit(self.basket_image, (self.basket_x, self.basket_y))
						

class Item:

    def __init__(self):
        items_list = ({"name": "obj0", "points": 20, "speed": 2}, \
                      {"name": "obj1", "points": 5, "speed": 1}, \
                      {"name": "obj2", "points": 50, "speed": 4}, \
                      {"name": "obj3", "points": 50, "speed": 4}, \
                      {"name": "obj4", "points": 30, "speed": 3}, \
                      {"name": "obj5", "points": 15, "speed": 2}, \
                      {"name": "obj6", "points": -100, "speed": 4}, \
                      {"name": "obj7", "points": 25, "speed": 3})

        item = choice(items_list)        
        self.x = randint(20, 780)
        self.y = randint(0, 3)
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

screen = pygame.display.set_mode((800, 600))

def main():
	pygame.mixer.pre_init(44100, -16, 2, 2048) # gets rid of delay in hearing sounds
	pygame.init()

	background_color = (randint(50, 255), randint(50, 255), randint(50, 255))
	points = level = caught = 0
	items = []
	menu = True
	level_change = 1 #0 - no change in this loop, 1 - level +1, 2 - game over

	pygame.mixer.init()
	pygame.display.set_caption("Maande")
	pygame.display.set_icon(pygame.image.load("./data/basket.png").convert_alpha())
	music = pygame.mixer.Sound("./data/tune.ogg")
	music.play(-1)
	pip = pygame.mixer.Sound("./data/pip.ogg")
	
	p = Player()
	items.append(Item())
	ticker = pygame.time.Clock()
	pygame.event.set_allowed(None)
	pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.USEREVENT, pygame.MOUSEMOTION])

	while True:
		screen.fill(background_color)

		if menu:
		    pygame.draw.rect(screen, (background_color[0] - 50, background_color[1] - 50, background_color[2] - 50), pygame.Rect(225, 50, 335, 80))		    
		    drawtext("MAANDE", 245, 60, 96, (255, 255, 255))
		    
		    pygame.draw.rect(screen, (background_color[0] - 40, background_color[1] - 40, background_color[2] - 40), pygame.Rect(50, 170, 390, 300))
		    drawtext("If you want to play", 90, 180, 48, (255, 255, 255))
		    drawtext("press ENTER.", 118, 220, 48, (255,255,255))
		    drawtext("Don't want to?", 130, 300, 48, (255,255,255))
		    drawtext("then BURN!", 125, 340, 60, (255,0,0))
		    drawtext("...or simply press ESC.", 70, 400, 48, (255, 255, 255))
		    
		    pygame.draw.rect(screen, (background_color[0] - 30, background_color[1] - 30, background_color[2] - 30), pygame.Rect(480, 170, 270, 400))
		    drawtext("How to play?", 510, 185, 48, (255,255,255))
		    drawtext("Use your mouse to move the basket.", 490, 235, 22, (255, 255, 255))
		    drawtext("This is a basket.", 490, 255, 22, (255, 255, 255))
		    drawtext("It wobbles a bit.", 490, 275, 22, (255, 255, 255))
		    pygame.draw.rect(screen, (background_color[0] - 10, background_color[1] - 10, background_color[2] - 10), pygame.Rect(645, 255, 60, 40))
		    screen.blit(pygame.image.load("./data/basket.png"), (650, 260))
		    drawtext("Catch the falling objects.", 490, 305, 24, (255, 255, 255))
		    drawtext("Some of them are shown below.", 490, 330, 24, (255, 255, 255))
		    drawtext("Their point values are:", 490, 355, 24, (255, 255, 255))
		    screen.blit(pygame.image.load("./data/items/obj4.png"), (490, 380))
		    drawtext("+30 pts", 540, 390, 24, (255, 255, 255))
		    screen.blit(pygame.image.load("./data/items/obj7.png"), (610, 380))
		    drawtext("+25 pts", 660, 390, 24, (255, 255, 255))
		    screen.blit(pygame.image.load("./data/items/obj0.png"), (490, 430))
		    drawtext("+20 pts", 540, 440, 24, (255, 255, 255))
		    screen.blit(pygame.image.load("./data/items/obj5.png"), (610, 430))
		    drawtext("+15 pts", 660, 440, 24, (255, 255, 255))
		    screen.blit(pygame.image.load("./data/items/obj1.png"), (490, 480))
		    drawtext("+5 pt", 540, 490, 24, (255, 255, 255))
		    screen.blit(pygame.image.load("./data/items/obj6.png"), (610, 480))
		    drawtext("-100 pts", 660, 490, 24, (255, 0, 0))
		    drawtext("You have to catch enough of them", 490, 530, 22, (255, 255, 255))
		    drawtext("into the basket to pass the level.", 490, 550, 22, (255, 255, 255))
		    
		    pygame.draw.rect(screen, (background_color[0] - 20, background_color[1] - 20, background_color[2] - 20), pygame.Rect(50, 490, 280, 80))
		    drawtext("CREDITS:", 70, 492, 16, (255,255,255))
		    drawtext("- Marcin 'Walker' Pospiech - coding", 70, 512, 15, (255,255,255))
		    drawtext("- Mateusz 'mmkay' Kulewicz - coding, art, music", 70, 532, 15, (255,255,255))
		    drawtext("- Monika Maciejewska - art", 70, 552, 15, (255,255,255))
		    
		    ticker.tick(5) # we don't need 35 fps in menu
		    

		else:
		    
		    if level_change == 1:
	        	background_color = (randint(50, 255), randint(50, 255), randint(50, 255))
	        	level += 1
	        	pygame.time.set_timer(pygame.USEREVENT+1, 5000/level)
	        	time_passed = 0
	        	level_change = 0
		    elif level_change == 2:
	        	pygame.time.wait(3000)
	        	return False

		    for item in items:
		        won = item.update(p)
		        points += won
		        if won != 0:
		            pip.play(0)
		            caught += 1
		        if won != 0 or item.y > 650:
		            items.remove(item)

		    mouse = pygame.mouse.get_pos()[0]
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
		    drawtext("fps: %.4s" % ticker.get_fps(), 735, 580, 18, (255, 255, 255))
		    
		    ticker.tick(35)

		for event in pygame.event.get():
		    if event.type == pygame.QUIT:
			    return False #end a game when clicking on x
		    elif event.type == pygame.KEYDOWN:
			    if event.key == pygame.K_RETURN:
			        if menu:
			            menu = False
			    if event.key == pygame.K_ESCAPE:
			        if menu:
			            return False # close the game
			        else:
			            menu = True
		    elif event.type == pygame.USEREVENT+1:
			    items.append(Item())

		pygame.display.flip()
