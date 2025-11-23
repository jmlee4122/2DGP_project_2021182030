from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_MOUSEBUTTONDOWN

import game_framework
import game_world
from quit_button import QuitButton
from restart_button import RestartButton
from resume_button import ResumeButton


def init():
    global restart_button
    global resume_button
    global quit_button

    restart_button = RestartButton()
    resume_button = ResumeButton()
    quit_button = QuitButton()

    #game_world.add_menu_object(restart_button, 0)
    game_world.add_menu_object(resume_button, 0)
    #game_world.add_menu_object(quit_button, 0)

def finish():
    global restart_button
    global resume_button
    global quit_button

    game_world.remove_menu_object(restart_button)
    game_world.remove_menu_object(resume_button)
    game_world.remove_menu_object(quit_button)

    del restart_button
    del resume_button
    del quit_button

def update():
    #game_world.update()
    game_world.update_menu()

def draw():
    clear_canvas()
    game_world.render()
    game_world.render_menu()
    update_canvas()

def handle_events():
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if resume_button is not None:
                if resume_button.is_active:
                    game_framework.pop_mode()
        else:
            if resume_button is not None:
                resume_button.handle_event(event)

def pause():
    pass

def resume():
    pass