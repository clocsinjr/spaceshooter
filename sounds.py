import pygame
# http://stackoverflow.com/questions/18273722/pygame-sound-delay
pygame.mixer.pre_init(44100, -16, 1, 4096)
pygame.mixer.init()

bgmusic = pygame.mixer.music.load("bgmusic3.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

fireChannel = pygame.mixer.Channel(1)
hitMarker = pygame.mixer.Channel(2)
playerHit = pygame.mixer.Channel(3)
pickups = pygame.mixer.Channel(4)

fireChannel.set_volume(0.5)
hitMarker.set_volume(0.5)

playerFireSound = pygame.mixer.Sound("playerFireSound.ogg")
hitEnemySound = pygame.mixer.Sound("hitEnemySound.ogg")
killEnemySound = pygame.mixer.Sound("killEnemySound.ogg")
hitPlayerSound = pygame.mixer.Sound("hitPlayerSound.ogg")
pickupBuff = pygame.mixer.Sound("pickupBuff.ogg")
pickupWeap = pygame.mixer.Sound("pickupWeap.ogg")