#-*- encoding: utf-8 -*-
import sys, pygame, time, random, math

TILE_SZ = 16

pygame.init()
pygame.font.init()

class Vec:
	x = 0
	y = 0

	def __init__(this, x, y):
		this.x = x
		this.y = y

	def __add__(a, b):
		return Vec(a.x + b.x, a.y + b.y)

	def __sub__(a, b):
		return Vec(a.x - b.x, a.y - b.y)	

	def __eq__(a, b):
		return a.x == b.x and a.y == b.y

	def __ne__(a, b):
		return not(a == b)

	def toTile(this):
		global TILE_SZ
		return pygame.Rect(this.x * TILE_SZ, this.y * TILE_SZ, TILE_SZ, TILE_SZ)

def randVec(w, h):
	return Vec(random.randint(0, w-1), random.randint(0, h-1))

def newApple(w, h, snake):
	apple = randVec(w,h)
	while apple in snake:
		apple = randVec(w,h)
	return apple


text_font = pygame.font.Font("lucon.ttf", 16)

black = 0, 0, 0
white = 255, 255, 255
blue= 0, 0,255
green = 0, 255, 0
yellow = 255, 255, 0
red = 255, 0, 0

apple_color = green

background = pygame.image.load("background.jpg")

apple_red = pygame.image.load("apple_red.bmp")
apple_red.set_colorkey((255,255,255))
apple_yellow = pygame.image.load("apple_yellow.bmp")
apple_yellow.set_colorkey((255,255,255))
apple_green = pygame.image.load("apple_green.bmp")
apple_green.set_colorkey((255,255,255))

body = pygame.image.load("body.bmp")
body.set_colorkey((255,255,255))

head =  pygame.image.load("head.bmp")
head.set_colorkey((255,255,255))
tail =  pygame.image.load("tail.bmp")
tail.set_colorkey((255,255,255))
tail.set_colorkey((255,255,255))

size = Vec(32,32)
screen = pygame.display.set_mode((size.x*TILE_SZ,size.y*TILE_SZ))
random.seed(time.time())

snake = [ Vec(16,15), Vec(15,15), Vec(14,15) ]
direction = Vec(1,0)
phys_dir = Vec(1, 0)


apple_delay = 50
apple_tick = 0
apple = newApple(size.x, size.y, snake)
latent_apple = Vec(-1, -1)

score = 0

exit = False

fps = 10
t = 0
#Boucle principale

while not exit:
	for event in pygame.event.get():

		#Requête de fermeture de fenêtre

		if event.type == pygame.QUIT:

			exit = True
			break

		#Gestion des touches

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_LEFT:

				phys_dir = Vec(-1, 0)

			elif event.key == pygame.K_RIGHT:

				phys_dir = Vec(1, 0)

			elif event.key == pygame.K_UP:

				phys_dir = Vec(0, -1)

			elif event.key == pygame.K_DOWN:

				phys_dir = Vec(0, 1)

	#Mise à jour du temps

	t = time.clock()
	apple_tick += 1

	#Mise à jour de la direction
	
	if phys_dir == Vec(-1, 0) and direction.x != 1:		

		direction = Vec(-1, 0)
					
	elif phys_dir == Vec(1, 0) and direction.x != -1:

		direction = Vec(1, 0)
		
	elif phys_dir == Vec(0, -1) and direction.y != 1:

		direction = Vec(0, -1)
		
	elif phys_dir == Vec(0, 1) and direction.y != -1:

		direction = Vec(0, 1)
		
	
	#Vérification de la transformation d'une pomme

	grow = False
	if latent_apple != Vec(-1,-1) and latent_apple == snake[-1]:
		grow = True

	#Mise à jour de la position du snake

	for k in range(len(snake)-1, 0, -1):
		snake[k] = snake[k-1]
	snake[0] = direction + snake[0]
	if snake[0].x >= size.x:
		snake[0].x = 0

	elif snake[0].x < 0:
		snake[0].x = size.x-1

	if snake[0].y >= size.y:
		snake[0].y = 0

	elif snake[0].y < 0:
		snake[0].y = size.y-1

	tail_dir = snake[-2] - snake[-1]

	#Agrandissement du snake

	if grow:
		snake.append(latent_apple)
		latent_apple = Vec(-1, -1)

		fps += .5

	#Mord la queue?

	if snake[0] in snake[1:]:
		print "PERDU", score 
		exit = True

	#Mange une pomme?

	if snake[0] == apple:
		latent_apple = apple

		apple_tick = 0
		apple_color = green
		apple = newApple(size.x, size.y, snake)

		if apple_color == red: score += 3

		elif apple_color == yellow : score += 2

		else : score +=1

	#Couleur & génération de pommes


	if apple_tick > apple_delay:

		apple_tick = 0
		apple = newApple(size.x, size.y, snake)
	elif apple_tick > 3*apple_delay/4:

		apple_color = red
		apple_image = apple_red 

	elif apple_tick > apple_delay/2:

		apple_color = yellow
		apple_image = apple_yellow
	else : 

		apple_color = green 
		apple_image = apple_green


	#Dessin

	screen.fill(black)
	screen.blit(background ,(0,0))
	for element in snake[1:len(snake)-1]:
		screen.blit(body,element.toTile())
		
	head_angle = math.atan2(direction.y,direction.x)*180/math.pi
	head_temp = pygame.transform.rotate(head,-head_angle)	
	screen.blit(head_temp,snake[0].toTile())

	tail_angle = math.atan2(tail_dir.y,tail_dir.x)*180/math.pi
	tail_temp = pygame.transform.rotate(tail,-tail_angle)
	screen.blit(tail_temp,snake[-1].toTile())
	screen.blit(apple_image, apple.toTile())
	screen.blit(text_font.render(str(score), 1, (255, 0, 0)), (0, 0))

	#Mettre à jour l'affichage

	pygame.display.flip()

	#On attend 1/60 de seconde moins le temps déjà écoulé cette frame

	time.sleep(1.0/fps - (time.clock() - t))

pygame.font.quit()
pygame.quit()