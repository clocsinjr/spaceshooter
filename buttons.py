import pygame
import images

import global_vars as g


class gui_button():
    def __init__(self, img, sel_img, func):
        self.img = img
        self.sel_img = sel_img
        self.rect = img.get_rect()
        self.func = func

def b_continue():
    g.paused = not g.paused

def b_exit():
    g.done = True

def b_toggle_music():
    if g.music_paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
    g.music_paused = not g.music_paused



button_continue = gui_button(
    images.button_continue, images.button_continue_sel, b_continue)
button_exit = gui_button(
    images.button_exit, images.button_exit_sel, b_exit)
button_toggle_music = gui_button(
    images.button_music_toggle, images.button_music_toggle_sel, b_toggle_music)