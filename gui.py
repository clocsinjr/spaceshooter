import pygame
import entity
from clocspaceshooter import size, player, screen, difficulty
from clocspaceshooter import WHITE, RED, GREEN

pygame.font.init()
scorefont = pygame.font.Font("vgasys.fon", 64)

scorex = (size[0] / 7) * 5
scorey = size[1] - 110

hpx = (size[0] / 7) * 6
hpy = size[1] - 110

# difficulty 
diffx = (size[0] / 7) * 3
diffy = size[1] - 110

hpbarxmin = 50
hpbarxmax = size[0] - 50
hpbarymax = size[1] - 50
hpbarymin = hpbarymax - 30
hpbarlen = hpbarxmax - hpbarxmin

def draw_hpbar():
    hpbarlim = hpbarlen * (player.HP / 100.0) + 1
    hpbarlim2 = hpbarlen * ((100 - player.HP) / 100.0)

    if player.HP > 0.0:
        pygame.draw.rect(screen, GREEN, [hpbarxmin, hpbarymin, hpbarlim, 30])

    if player.HP < 100.0:
        pygame.draw.rect(
            screen, RED, [hpbarlim + hpbarxmin, hpbarymin, hpbarlim2, 30])
			
def drawgui():
    scoretxt = scorefont.render("Score: " + str(player.score), False, WHITE)
    screen.blit(scoretxt, (scorex, scorey))

    hptxt = scorefont.render("HP: " + str(player.HP) + "/ 100", False, WHITE)
    screen.blit(hptxt, (hpx, hpy))

    difftext = scorefont.render("Difficulty: " + str(difficulty), False, WHITE)
    screen.blit(difftext, (diffx, diffy))
	
    draw_hpbar()

    