import pygame

# -----------------------
# GRAPHICS

BLUE = (0,0,255)
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

SCREEN_DIMENSION = (800, 750)
grid_dim = (15, 12)

token_radius = 20

# La taille des "blocks" qui vont contenir les cercles blancs
blockSize = 50

# L'offset de la grid
grid_x_offset = int((SCREEN_DIMENSION[0] - grid_dim[0]*blockSize) / 2)
grid_y_offset = SCREEN_DIMENSION[1] - grid_dim[1]*blockSize - 25
	
# L'offset du cercle par rapport au block
circle_offset = (blockSize - token_radius) / 2


def init_graphics(screen_dimension, grid_dimension):
	global SCREEN_DIMENSION, grid_dim
	SCREEN_DIMENSION = screen_dimension
	grid_dim = grid_dimension





def draw_grid(screen):
	screen.fill((255,255,255))

	rect = pygame.Rect(grid_x_offset-5, grid_y_offset-5, blockSize*grid_dim[0]+10, blockSize*grid_dim[1]+10)
	pygame.draw.rect(screen, BLACK, rect)

	for x in range(grid_dim[0]):
		for y in range(grid_dim[1]):
			circle_coords = calculate_real_coords((x,y))
			pygame.draw.circle(screen, WHITE, circle_coords, token_radius)


	pygame.display.flip()



# Une fonction qui va dessiner un token qui a été posé
def draw_token(screen, grid_coords, color):
	coords = calculate_real_coords(grid_coords)
	if color == 1:
		pygame.draw.circle(screen, RED, coords, token_radius)
	else:
		pygame.draw.circle(screen, BLUE, coords, token_radius)

	pygame.display.flip()




def draw_cursor(screen, x, previous_x, color):
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





class Button:
	def __init__(self, win, color, x, y, width, height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.draw(win, 2)

	def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
		if self.text != '':
			font = pygame.font.SysFont('calibri', 60)
			text = font.render(self.text, 1, (0, 0, 0))
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
		
		pygame.display.flip()

	def is_over(self, pos):
		# Pos is the mouse position or a tuple of (x, y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
            
		return False

class Text:
	def __init__(self, win: pygame.display, text: str, position: tuple[int], size=60):
		font = pygame.font.SysFont('calibri', size)
		text = font.render(self.text, 1, (0, 0, 0))
		win.blit(text, position)
		pygame.display.flip()