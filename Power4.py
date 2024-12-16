import pygame

# ------------------------
# PYGAME

pygame.init()

# On initialise la fenetre pygame
SCREEN_DIMENSION = (800, 750)
screen = pygame.display.set_mode(SCREEN_DIMENSION)

clock = pygame.time.Clock()

# ------------------------

# La grille de jeu et ses dimensions
grid_dim = (15, 12)
# La grille va contenir que des 0 pour définir un vide
# Et le numéro du player en fonction de la couleur du token
grid: list[list[int]] = [[0 for _ in range(grid_dim[0])] for _ in range(grid_dim[1])]


# Le numéro du joueur qui joue
# Pour l'instant le player est le 2 pour que ce soit le 1 qui commence
turn: int = 2


# Image variable
# redtoken_img = pygame.transform.scale2x(pygame.image.load("Assets/RedToken.png").convert())
# bluetoken_img = pygame.transform.scale2x(pygame.image.load("Assets/BlueToken.png").convert())
# gridsquare_img = pygame.transform.scale2x(pygame.image.load("Assets/GridSquare.png").convert())
BLUE = (0,0,255)
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

# -----------------------
# GRAPHICS

token_radius = 20

# La taille des "blocks" qui vont contenir les cercles blancs
blockSize = 50

# L'offset de la grid
grid_x_offset = int((SCREEN_DIMENSION[0] - grid_dim[0]*blockSize) / 2)
grid_y_offset = SCREEN_DIMENSION[1] - grid_dim[1]*blockSize 
	
# L'offset du cercle par rapport au block
circle_offset = (blockSize - token_radius) / 2

def draw_grid():
	screen.fill((255,255,255))

	rect = pygame.Rect(grid_x_offset-5, grid_y_offset-5, blockSize*grid_dim[0]+10, blockSize*grid_dim[1]+10)
	pygame.draw.rect(screen, BLACK, rect)

	for x in range(grid_dim[0]):
		for y in range(grid_dim[1]):
			circle_coords = calculate_real_coords((x,y))
			pygame.draw.circle(screen, WHITE, circle_coords, token_radius)


	pygame.display.flip()

# Une fonction qui va dessiner un token qui a été posé
def draw_token(coords, color):
	if color == 1:
		pygame.draw.circle(screen, RED, coords, token_radius)
	else:
		pygame.draw.circle(screen, BLUE, coords, token_radius)

	pygame.display.flip()

def draw_cursor(x, previous_x, color):
	# On efface l'ancien curseur
	previous_coords = calculate_real_coords((previous_x,-1.5))
	pygame.draw.circle(screen, WHITE, previous_coords, token_radius)

	# On dessine le nouveau
	coords = calculate_real_coords((x,-1.5))

	if color == 1:
		pygame.draw.circle(screen, RED, coords, token_radius)
	else:
		pygame.draw.circle(screen, BLUE, coords, token_radius)
	
	pygame.display.flip()


# -----------------------

# Un fonction qui va calculer les coordonnées d'un point sur le screen
# En fonction des coordonnées d'un jeton dans la grille
def calculate_real_coords(coords):
	# Les coordonnées du 
	x = coords[0] * blockSize + grid_x_offset + circle_offset + token_radius/2
	y = coords[1] * blockSize + grid_y_offset + circle_offset + token_radius/2
	return((x,y))



# Une fonction qui va déterminer la position du token laché
# En fonction de la grid, il va la modifier en conséquence
# Puis dessiner le token
def add_token(x) -> bool:
	# Si la derniere ligne est prise
	if grid[0][x] != 0:
		return False

	# On commence par déterminer à quelle y le token va s'arréter
	for y in range(len(grid)):
		# Si il y a un token, c'est que le token s'arrête sur la ligne d'avant
		if grid[y][x] != 0:
			y -= 1 # On revient donc une ligne en arrière
			break

	grid[y][x] = turn

	token_real_coords = calculate_real_coords((x,y))
	draw_token(token_real_coords, turn)

	return True


# On change de joueur qui joue
def change_turn():
	global turn
	if turn == 1: turn = 2
	else: turn = 1




# La fonction qui fait toute les action nécessaire quand on pose un jeton
def game_turn(cursor_x):
	# On ajoute le jeton
	add_token_worked =  add_token(cursor_x)

	# Si on n'a pas pu ajouter le token
	if add_token_worked == False:
		# On aborte le tour
		return

	change_turn()
	draw_cursor(cursor_x, cursor_x, turn)

	# On envoie les données de notre tour ici je suppose



# Main game loop
def main():
	running = True
	cursor_x = 0

	draw_grid()
	draw_cursor(cursor_x, 0, turn)

	while running:
		# On regarde tout les event
		for event in pygame.event.get():
			# Si on veut fermer la fenêtre, on quitte
			if event.type == pygame.QUIT:
				running = False
			
			# Si une touche est pressée
			if event.type == pygame.KEYDOWN:
				# On modifie la position du curseur
				if event.key == pygame.K_RIGHT and cursor_x < grid_dim[0]-1:
					cursor_x += 1
					draw_cursor(cursor_x, cursor_x-1, turn)
				if event.key == pygame.K_LEFT and cursor_x > 0:
					cursor_x -= 1
					draw_cursor(cursor_x, cursor_x+1, turn)
				# On ajoute un token
				if event.key == pygame.K_RETURN:
					game_turn(cursor_x)
				
		

		clock.tick(60)  # limits FPS to 60


	pygame.quit()



main()