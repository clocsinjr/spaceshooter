import pygame
import images
from clocspaceshooter import size, screen, done, paused
from clocspaceshooter import WHITE, RED, GREEN, BLACK

PAUSE_NUM_BUTTONS = 2
PAUSE_CONTINUE = 0
PAUSE_EXIT = 1

BUTTON_WIDTH = 128
BUTTON_HEIGHT = 32

pygame.font.init()
scorefont = pygame.font.Font("vgasys.fon", 64)

# score number display coordinates
scorex = (size[0] / 7) * 5
scorey = size[1] - 110

# HP number display coordinates
hpx = (size[0] / 7) * 6
hpy = size[1] - 110

# difficulty display x and y coordinates
diffx = (size[0] / 7) * 3
diffy = size[1] - 110

# HP bar coordinates
hpbarxmin = 50                      # start 50p from the left
hpbarxmax = size[0] - 50            # end 50p from the right
hpbarymax = size[1] - 50            # set bar 50p from the bottom
hpbarymin = hpbarymax - 30          # set bar height to 30p
hpbarlen = hpbarxmax - hpbarxmin    # help variable, tracks hpbar length

# pause window coordinates
pauseblockx1 = size[0] * ( 1 / 10.0)
pauseblocky1 = size[1] * ( 2 / 5.0)
pauseblockw = size[0] * ( 8 / 10.0)
pauseblockh = size[1] * ( 1 / 5.0)

# pause button image rects
button_continue_rect = images.button_continue.get_rect()
button_continue_rect.x = size[0]/2 - (16 + button_continue_rect.width)
button_continue_rect.y = size[1]/2 - (button_continue_rect.height / 2)

button_exit_rect = images.button_exit.get_rect()
button_exit_rect.x = size[0]/2 + 16
button_exit_rect.y = button_continue_rect.y

class gui_button():
    def __init__(img, func):
        self.rect = img.get_rect()
        self.func = func
class gui_window():
    def __init__(defx=0, defy=0, defw=size[0], defh=size[1]):
        self.x = defx
        self.y = defy
        self.w = defw
        self.h = defh
        
        self.opt_selected = (0, 0)
        self.opt_cols = []
        
        self.place_buttons()
    
    def handle(key):
        newc = self.opt_selected[0]
        newr = self.opt_selected[1]
        if key == pygame.K_LEFT:
            lencol = len(self.cols)
            newc = (self.opt_selected[0] - 1) % lencol
            self.opt_selected = (newc, newr)
        elif key == pygame.K_RIGHT:
            lencol = len(self.cols)
            newc = (self.opt_selected[0] + 1) % lencol
            self.opt_selected = (newc, newr)
        elif key == pygame.K_DOWN:
            lenrow = len(self.cols[self.opt_selected[0]])
            newr = (self.opt_selected[1] + 1) % lenrow
            self.opt_selected = (newc, newr)
        elif key == pygame.K_UP:
            lenrow = len(self.cols[self.opt_selected[0]])
            newr = (self.opt_selected[1] - 1) % lenrow
            self.opt_selected = (newc, newr)
        
        # if ENTER is pressed:
        elif key == pygame.K_RETURN:
            # set dict entry to True based on selected option
            if pause_selected == PAUSE_CONTINUE:
                r['pause'] = True
            elif pause_selected == PAUSE_EXIT:
                r['done'] = True
    def draw():
        for optrow in self.opt_cols
            for opt in optrow:
                pass
    
    def place_buttons():
        """ figures out on what coordinates to put the various buttons in the
        rows and cols list. """
        mid = self.x + (self.w / 2.0)
        maxleft = (len(self.opt_cols) * BUTTON_WIDTH +\ 
            (len(self.opt_cols) - 1) * 16)/2.0
        maxtop = self.y + 16
        for c in len(self.opt_cols):
            for r in len(self.opt_cols[c]):
                self.opt_cols[c][r].rect.x = maxleft + c * BUTTON_WIDTH
                self.opt_cols[c][r].rect.y = maxtop + r * BUTTON_HEIGHT
   
                
        
def handle_pausemenu(key, pause_selected):
    """ handle_pausemenu() is called from the main loop when pause == True.
    handles the pausemenu by looking at user input. returns a dict with content
    depending on what key is pressed. """
    
    # initialize response dict
    r = {'selected': None, 'done': None, 'pause': None}
    
    # return the new selection if a direction key is pressed.
    if key == pygame.K_LEFT:
        r['selected'] = PAUSE_CONTINUE
    elif key == pygame.K_RIGHT:
        r['selected'] = PAUSE_EXIT
    
    # if ENTER is pressed:
    elif key == pygame.K_RETURN:
        # set dict entry to True based on selected option
        if pause_selected == PAUSE_CONTINUE:
            r['pause'] = True
        elif pause_selected == PAUSE_EXIT:
            r['done'] = True
    
    # return response
    return r
        
def draw_pausescreen(pause_selected):
    """ Draws the pause menu window"""
    
    # draw pause menu background
    pygame.draw.rect(
        screen, BLACK, [pauseblockx1, pauseblocky1, pauseblockw, pauseblockh])
    
    # draw continue button
    if pause_selected == PAUSE_CONTINUE:
        screen.blit(images.button_continue_sel, button_continue_rect)
    else:
        screen.blit(images.button_continue, button_continue_rect)

    # draw exit button
    if pause_selected == PAUSE_EXIT:
        screen.blit(images.button_exit_sel, button_exit_rect)
    else:
        screen.blit(images.button_exit, button_exit_rect)
    
def draw_hpbar(player, difficulty):
    """ Draws the HP bar at the bottom of the gamescreen using the global
    variables set at initialization """
    
    # Where the red bar starts
    hpbarlim = hpbarlen * (player.HP / 100.0) + 1
    # Length of the red bar
    hpbarlim2 = hpbarlen * ((100 - player.HP) / 100.0)

    if player.HP > 0.0:
        pygame.draw.rect(screen, GREEN, [hpbarxmin, hpbarymin, hpbarlim, 30])

    if player.HP < 100.0:
        pygame.draw.rect(
            screen, RED, [hpbarlim + hpbarxmin, hpbarymin, hpbarlim2, 30])
			
def drawgui(paused, pause_selected, player, difficulty):
    """ Called at the main loop. Draws everything GUI related."""
    
    # draw score number display
    scoretxt = scorefont.render("Score: " + str(player.score), False, WHITE)
    screen.blit(scoretxt, (scorex, scorey))

    # draw HP number display
    hptxt = scorefont.render("HP: " + str(player.HP) + "/ 100", False, WHITE)
    screen.blit(hptxt, (hpx, hpy))

    # draw difficulty number display
    difftext = scorefont.render("Difficulty: " + str(difficulty), False, WHITE)
    screen.blit(difftext, (diffx, diffy))
	
    # draw HPbar
    draw_hpbar(player, difficulty)
    
    # draw the pause menu window if the game is paused
    if paused:
        draw_pausescreen(pause_selected)
    