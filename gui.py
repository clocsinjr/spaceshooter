import pygame
import images
from clocspaceshooter import size, screen, done
from clocspaceshooter import WHITE, RED, GREEN, BLACK

PAUSE_NUM_BUTTONS = 2
PAUSE_CONTINUE = 0
PAUSE_EXIT = 1

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

pauseblockx1 = size[0] * ( 1 / 10.0)
pauseblocky1 = size[1] * ( 2 / 5.0)
pauseblockw = size[0] * ( 8 / 10.0)
pauseblockh = size[1] * ( 1 / 5.0)

button_continue_rect = images.button_continue.get_rect()
button_continue_rect.x = size[0]/2 - (16 + button_continue_rect.width)
button_continue_rect.y = size[1]/2 - (button_continue_rect.height / 2)

button_exit_rect = images.button_exit.get_rect()
button_exit_rect.x = size[0]/2 + 16
button_exit_rect.y = button_continue_rect.y
    
def handle_pausemenu(key, pause_selected):
    r = {'selected': None, 'done': None, 'pause': None}
    if key == pygame.K_LEFT:
        r['selected'] = PAUSE_CONTINUE
    elif key == pygame.K_RIGHT:
        r['selected'] = PAUSE_EXIT
    elif key == pygame.K_RETURN:
        if pause_selected == PAUSE_CONTINUE:
            r['pause'] = True
        elif pause_selected == PAUSE_EXIT:
            r['done'] = True
    return r
        
def draw_pausescreen(pause_selected):
    pygame.draw.rect(
        screen, BLACK, [pauseblockx1, pauseblocky1, pauseblockw, pauseblockh])
    
    if pause_selected == PAUSE_CONTINUE:
        screen.blit(images.button_continue_sel, button_continue_rect)
    else:
        screen.blit(images.button_continue, button_continue_rect)

    if pause_selected == PAUSE_EXIT:
        screen.blit(images.button_exit_sel, button_exit_rect)
    else:
        screen.blit(images.button_exit, button_exit_rect)
    
def draw_hpbar(player, difficulty):
    # Where the red bar starts
    hpbarlim = hpbarlen * (player.HP / 100.0) + 1
    # Length of the red bar
    hpbarlim2 = hpbarlen * ((100 - player.HP) / 100.0)

    if player.HP > 0.0:
        pygame.draw.rect(screen, GREEN, [hpbarxmin, hpbarymin, hpbarlim, 30])

    if player.HP < 100.0:
        pygame.draw.rect(
            screen, RED, [hpbarlim + hpbarxmin, hpbarymin, hpbarlim2, 30])
			
def drawgui(player, difficulty):
    scoretxt = scorefont.render("Score: " + str(player.score), False, WHITE)
    screen.blit(scoretxt, (scorex, scorey))

    hptxt = scorefont.render("HP: " + str(player.HP) + "/ 100", False, WHITE)
    screen.blit(hptxt, (hpx, hpy))

    difftext = scorefont.render("Difficulty: " + str(difficulty), False, WHITE)
    screen.blit(difftext, (diffx, diffy))
	
    draw_hpbar(player, difficulty)
    