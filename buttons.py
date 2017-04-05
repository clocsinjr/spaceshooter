import pygame
import images

import global_vars as g

def b_continue():
    g.paused = not g.paused

def b_exit():
    g.done = True

class gui_button():
    def __init__(self, img, sel_img, func):
        self.img = img
        self.sel_img = sel_img
        self.rect = img.get_rect()
        self.func = func


button_continue = gui_button(images.button_continue, images.button_continue_sel, b_continue)
button_exit = gui_button(images.button_exit, images.button_exit_sel, b_exit)