from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_MOUSEBUTTONDOWN

import game_framework
import game_world
import play_mode
import title_mode
from quit_button import QuitButton
from restart_button import RestartButton
from resume_button import ResumeButton

def init():
    global restart_button
    global resume_button
    global quit_button

    restart_button = RestartButton(1920 / 2, 1080 * 0.5)
    resume_button = ResumeButton(1920 / 2, 1080 * 0.8)
    quit_button = QuitButton(1920 / 2, 1080 * 0.2)

    game_world.add_menu_object(restart_button, 0)
    game_world.add_menu_object(resume_button, 0)
    game_world.add_menu_object(quit_button, 0)

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
    global restart_button
    global resume_button
    global quit_button
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and restart_button.is_active:
            play_mode.last_stage = None
            play_mode.saved_user_char = None
            game_framework.change_mode_clear(title_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN and resume_button.is_active:
            game_framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN and quit_button.is_active:
            game_framework.quit()
        else:
            if restart_button is not None:
                restart_button.handle_event(event)
            if resume_button is not None:
                resume_button.handle_event(event)
            if quit_button is not None:
                quit_button.handle_event(event)


def pause():
    pass

def resume():
    pass