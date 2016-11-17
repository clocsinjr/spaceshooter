import pygame
# http://stackoverflow.com/questions/18273722/pygame-sound-delay
pygame.mixer.pre_init(44100, -16, 1, 4096)
pygame.mixer.init()

src = "audio/"
bgmusic = pygame.mixer.music.load(src + "bgmusic2.wav")
#bgmusic = pygame.mixer.music.load(src + "bgmusic3.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

fireChannel = pygame.mixer.Channel(1)
hitMarker = pygame.mixer.Channel(2)
playerHit = pygame.mixer.Channel(3)
pickups = pygame.mixer.Channel(4)

fireChannel.set_volume(0.5)
hitMarker.set_volume(0.5)

playerFireSound = pygame.mixer.Sound(src + "playerFireSound.ogg")
hitEnemySound = pygame.mixer.Sound(src + "hitEnemySound.ogg")
killEnemySound = pygame.mixer.Sound(src + "killEnemySound.ogg")
hitPlayerSound = pygame.mixer.Sound(src + "hitPlayerSound.ogg")
pickupBuff = pygame.mixer.Sound(src + "pickupBuff.ogg")
pickupWeap = pygame.mixer.Sound(src + "pickupWeap.ogg")