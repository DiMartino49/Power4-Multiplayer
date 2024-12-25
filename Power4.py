import pygame
from power4_graphics import *

# ------------------------
# PYGAME

pygame.init()

# On initialise la fenetre pygame
SCREEN_DIMENSION = (800, 750)
screen = pygame.display.set_mode(SCREEN_DIMENSION)

clock = pygame.time.Clock()

init_graphics(SCREEN_DIMENSION, grid_dim)

# ------------------------

# La grille de jeu et ses dimensions
grid_dim = (15, 12)
# La grille va contenir que des 0 pour définir un vide
# Et le numéro du player en fonction de la couleur du token
grid: list[list[int]] = [[0 for _ in range(grid_dim[0])] for _ in range(grid_dim[1])]

# Le numéro du joueur qui joue
# Pour l'instant le player est le 2 pour que ce soit le 1 qui commence
turn: int = 2
winner: int = 0

# La variable qui determine si le jeu est en ligne ou local
online: bool = False
# La variable qui determine si le joueur est le 1 ou le 2 pour les parties en ligne
player_number: int = 1





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

	draw_token(screen, (x,y), turn)

	check_end((x,y))
	return True


# On change de joueur qui joue
def change_turn():
	global turn
	if turn == 1: turn = 2
	else: turn = 1


# On renvoie 0 s'il y a un winner
# turn s'il y en a un
def check_end(token_coord):
	global winner

	# Vertiacalement
	winner = check_winner(token_coord, dirs["VERTICAL"])
	if winner != 0:
		return 
	winner = check_winner(token_coord, dirs["HORIZONTAL"])
	if winner != 0:
		return
	winner = check_winner(token_coord, dirs["DIAGONAL1"])
	if winner != 0:
		return
	winner = check_winner(token_coord, dirs["DIAGONAL2"])

dirs = {
	"VERTICAL" : 0,
	"HORIZONTAL" : 1,
	"DIAGONAL1" : 2,
	"DIAGONAL2" : 3,
}

# On regarde s'il y a un vainqueur en fonction d'une direction
def check_winner(coords, dir):
	t_array = []
	
	# On détermine un array de transformation en fonction de la direction
	if dir == dirs["VERTICAL"]:
		t_array = [0,-1]
	elif dir == dirs["HORIZONTAL"]:
		t_array = [-1,0]
	elif dir == dirs["DIAGONAL1"]:
		t_array = [-1,-1]
	elif dir == dirs["DIAGONAL2"]:
		t_array = [1, -1]
	

	# On trouve le "dernier" token en fonction de l'array
	tk = turn
	x = coords[0] ; y = coords[1]
	while tk == turn and x >= 0 and y >= 0:
		coords = (x,y)
		x -= t_array[0]
		y -= t_array[1]
		try:
			tk = grid[y][x]
		except:
			break

	
	# On compte le nombre de token 
	x = coords[0] ; y = coords[1]
	tk_nb = 0
	for i in range(3):
		x += t_array[0]
		y += t_array[1]
		try:
			if grid[y][x] == turn:
				tk_nb += 1
		except:
			break

	if tk_nb == 3:
		return turn
	
	return 0




def check_for_token(x, y):
	if grid[y][x] == turn:
		return True	
	return 0



	# On va regarder si la somme du nombre de token a gauche et a droite est egal à 4
	# Si oui, c'est que la partie est finie



# La fonction qui fait toute les action nécessaire quand on pose un jeton
# Quand on joue localement
def game_turn_local(cursor_x):
	# On ajoute le jeton
	add_token_worked = add_token(cursor_x)

	# Si on n'a pas pu ajouter le token
	if add_token_worked == False:
		# On aborte le tour
		return


	change_turn()
	draw_cursor(screen, cursor_x, cursor_x, turn)

	


# La fonction qui fait toute les action spéciques quand on pose un jeton
# Quand on joue online
def game_turn_online(cursor_x):
	# On ajoute le jeton
	add_token_worked =  add_token(cursor_x)

	# Si on n'a pas pu ajouter le token
	if add_token_worked == False:
		# On aborte le tour
		return

	if winner != 0:
		print("WINNER")

	change_turn()
	draw_cursor(screen, cursor_x, cursor_x, turn)

	check_end()

	# On envoie les données de notre tour ici je suppose


# Menu principal
def menu():
	global online
	screen.fill(WHITE)
	# Pygame Buttons to choose beetween online and local
	online_button = Button(screen, WHITE, 300, 300, 200, 100, 'Online')
	local_button = Button(screen, WHITE, 300, 500, 200, 100, 'Local')

	menu_running = True

	while menu_running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				menu_running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if online_button.is_over(pygame.mouse.get_pos()):
					online = True
					menu_running = False
				if local_button.is_over(pygame.mouse.get_pos()):
					online = False
					menu_running = False
			
	print(online)

# Menu de fin
def end_menu(winner):
	screen.fill(WHITE)
	# Pygame Buttons to choose beetween online and local
	play_again_button = Button(screen, WHITE, 300, 300, 200, 100, 'Play again')
	quit_button = Button(screen, WHITE, 300, 500, 200, 100, 'Local')

	if online == False:
		screen.



	menu_running = True

	while menu_running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				menu_running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if online_button.is_over(pygame.mouse.get_pos()):
					online = True
					menu_running = False
				if local_button.is_over(pygame.mouse.get_pos()):
					online = False
					menu_running = False
			
	print(online)


# Main game loop
def main():
	running = True
	cursor_x = 0

	draw_grid(screen)
	draw_cursor(screen, cursor_x, 0, turn)

	while winner == 0 and running:
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
					draw_cursor(screen, cursor_x, cursor_x-1, turn)
				if event.key == pygame.K_LEFT and cursor_x > 0:
					cursor_x -= 1
					draw_cursor(screen, cursor_x, cursor_x+1, turn)
				# On ajoute un token
				if event.key == pygame.K_RETURN:
					# Si on joue en ligne
					if online == True and turn == player_number:
						game_turn_online(cursor_x)
					# Si on joue local	
					else:
						game_turn_local(cursor_x)
		
		clock.tick(60)  # limits FPS to 60

	if winner != 0:
		print("Player " + str(winner) + " won !!")
	
	print("")
	input("Press Enter to quit...")
		

	
	pygame.quit()


menu()
main()

