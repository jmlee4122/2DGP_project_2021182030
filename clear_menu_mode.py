from pico2d import clear_canvas, update_canvas, get_events, load_image, get_canvas_width, get_canvas_height
from sdl2 import SDL_QUIT, SDL_MOUSEBUTTONDOWN

import game_framework
import game_world
import play_mode
import title_mode
from quit_button import QuitButton
from restart_button import RestartButton


def init():
    file_path = "2DGP_GUI/"
    global image
    global restart_button
    global quit_button

    image = load_image(file_path + 'clear_board.png')
    restart_button = RestartButton(1920 / 2, 1080 * 0.55)
    quit_button = QuitButton(1920 / 2, 1080 * 0.35)

    game_world.add_menu_object(restart_button, 0)
    game_world.add_menu_object(quit_button, 0)

def finish():
    global restart_button
    global quit_button

    game_world.remove_menu_object(restart_button)
    game_world.remove_menu_object(quit_button)

    del restart_button
    del quit_button

def update():
    game_world.update_menu()

def draw():
    clear_canvas()
    if image is None:
        update_canvas()
        return

    canvas_w, canvas_h = get_canvas_width(), get_canvas_height()
    cx = canvas_w // 2
    cy = canvas_h // 2

    game_world.render()

    image.draw(cx, cy)
    game_world.render_menu()
    update_canvas()

def handle_events():
    global restart_button
    global quit_button
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and restart_button.is_active:
            play_mode.last_stage = None
            play_mode.saved_user_char = None
            game_framework.change_mode_clear(title_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN and quit_button.is_active:
            game_framework.quit()
        else:
            if restart_button is not None:
                restart_button.handle_event(event)
            if quit_button is not None:
                quit_button.handle_event(event)

