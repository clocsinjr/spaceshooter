import pygame
import images
import buttons

from clocspaceshooter import size, screen
from clocspaceshooter import WHITE, RED, GREEN, BLACK

import global_vars as g

PAUSE_NUM_BUTTONS = 2
PAUSE_CONTINUE = 0
PAUSE_EXIT = 1

BUTTON_WIDTH = 128
BUTTON_HEIGHT = 32
BUTTON_OFFSET_X = 16
BUTTON_OFFSET_Y = 16

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

class gui_window():
    def __init__(self, buttons, defpos=None):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        
        self.opt_selected = (0, 0)
        self.opt_cols = buttons
        
        self.place_buttons(defpos)
    
    def handle(self, key):
        newc = self.opt_selected[0]
        newr = self.opt_selected[1]
        if key == pygame.K_LEFT:
            lencol = len(self.opt_cols)
            newc = (self.opt_selected[0] - 1) % lencol
            self.opt_selected = (newc, newr)
        elif key == pygame.K_RIGHT:
            lencol = len(self.opt_cols)
            newc = (self.opt_selected[0] + 1) % lencol
            self.opt_selected = (newc, newr)
        elif key == pygame.K_DOWN:
            lenrow = len(self.opt_cols[self.opt_selected[0]])
            newr = (self.opt_selected[1] + 1) % lenrow
            self.opt_selected = (newc, newr)
        elif key == pygame.K_UP:
            lenrow = len(self.opt_cols[self.opt_selected[0]])
            newr = (self.opt_selected[1] - 1) % lenrow
            self.opt_selected = (newc, newr)
        
        # if ENTER is pressed:
        elif key == pygame.K_RETURN:
            c, r = self.opt_selected
            self.opt_cols[c][r].func()
    def draw(self):
        bgrect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, BLACK, bgrect)
        pygame.draw.rect(screen, WHITE, bgrect, 2)
        for c in range(len(self.opt_cols)):
            for r in range(len(self.opt_cols[c])):
                opt = self.opt_cols[c][r]
                if (c, r) == self.opt_selected:
                    screen.blit(opt.sel_img, opt.rect)
                else:
                    screen.blit(opt.img, opt.rect)
    
    def place_buttons(self, defpos):
        """ figures out on what coordinates to put the various buttons in the
        rows and cols list. """
        
        ncols = len(self.opt_cols)
        nrows = max([len(self.opt_cols[i]) for i in range(ncols)])
        
        self.w = BUTTON_OFFSET_X * (ncols + 1) + BUTTON_WIDTH * ncols
        self.h = BUTTON_OFFSET_Y * (nrows + 1) + BUTTON_HEIGHT * nrows
        
        if defpos:
            self.x, self.y = defpos
        else:
            self.x = (size[0] - self.w)/2
            self.y = (size[1] - self.h)/2 
            
        mid = self.x + (self.w / 2.0)
        maxleft = self.x + BUTTON_OFFSET_X
        maxtop = self.y + BUTTON_OFFSET_Y
        for c in range(len(self.opt_cols)):
            for r in range(len(self.opt_cols[c])):
                thisrect = self.opt_cols[c][r].rect
                thisrect.x = maxleft + c * (BUTTON_WIDTH + BUTTON_OFFSET_X)
                thisrect.y = maxtop + r * (BUTTON_HEIGHT + BUTTON_OFFSET_Y)


def draw_hpbar():
    """ Draws the HP bar at the bottom of the gamescreen using the global
    variables set at initialization """
    
    # Where the red bar starts
    hpbarlim = hpbarlen * (g.player.HP / 100.0) + 1
    # Length of the red bar
    hpbarlim2 = hpbarlen * ((100 - g.player.HP) / 100.0)

    if g.player.HP > 0.0:
        pygame.draw.rect(screen, GREEN, [hpbarxmin, hpbarymin, hpbarlim, 30])

    if g.player.HP < 100.0:
        pygame.draw.rect(
            screen, RED, [hpbarlim + hpbarxmin, hpbarymin, hpbarlim2, 30])
			
def drawgui():
    """ Called at the main loop. Draws everything GUI related."""
    
    # draw score number display
    scoretxt = scorefont.render("Score: " + str(g.player.score), False, WHITE)
    screen.blit(scoretxt, (scorex, scorey))

    # draw HP number display
    hptxt = scorefont.render("HP: " + str(g.player.HP) + "/ 100", False, WHITE)
    screen.blit(hptxt, (hpx, hpy))

    # draw difficulty number display
    difftext = scorefont.render("Difficulty: " + str(g.difficulty), False, WHITE)
    screen.blit(difftext, (diffx, diffy))
	
    # draw HPbar
    draw_hpbar()
    
    # draw the pause menu window if the game is paused
    if g.paused:
        pausemenu.draw()

pausemenu = gui_window([[buttons.button_continue, buttons.button_toggle_music], [buttons.button_exit]])