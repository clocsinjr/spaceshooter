import pygame

# menu state variables
done = False
paused = False

# original gamestate:
playerGroup = pygame.sprite.Group()
pickups = pygame.sprite.Group()
fProj = pygame.sprite.Group()
eProj = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = None
time = 0
difficulty = 0
diffcount = 0

music_selected = 0
music_paused = False