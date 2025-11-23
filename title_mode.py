from pico2d import *

import game_framework
import play_mode
from exit_text_title_mode import ExitText
from start_text_title_mode import StartText

image = None

def init():
    file_path = "2DGP_background/start_screen/"
    global image
    global start_text
    global exit_text

    image = load_image(file_path + 'start_screen.png')
    start_text = StartText()
    exit_text = ExitText()

    try:
        canvas_w, canvas_h = get_canvas_width(), get_canvas_height()
        #print(f"[DEBUG] canvas: {canvas_w}x{canvas_h}, image: {image.w}x{image.h}")
    except Exception:
        #print("[DEBUG] init: unable to read canvas/image sizes")
        pass


def update():
        # if start_text is not None:
        #     if start_text.is_clicked:
        #         game_framework.change_mode(play_mode)
        # if exit_text is not None:
        #     if exit_text.is_clicked:
        #         game_framework.quit()
        pass
#game_framework.change_mode(play_mode)


def draw():
    clear_canvas()
    if image is None:
        update_canvas()
        return

    canvas_w, canvas_h = get_canvas_width(), get_canvas_height()
    cx = canvas_w // 2
    cy = canvas_h // 2

    image.draw(cx, cy, canvas_w, canvas_h)
    start_text.draw()
    exit_text.draw()
    update_canvas()


def finish():
    global image
    global start_text
    global exit_text

    if start_text is not None:
        del start_text
        start_text = None

    if exit_text is not None:
        del exit_text
        exit_text = None

    # 타이틀 이미지 정리
    if image is not None:
        del image
        image = None

def handle_events():
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if start_text is not None:
                if start_text.is_active:
                    game_framework.change_mode(play_mode)
            if exit_text is not None:
                if exit_text.is_active:
                    game_framework.quit()
        else:
            if start_text is not None:
                start_text.handle_event(event)
            if exit_text is not None:
                exit_text.handle_event(event)


def pause():
    pass


def resume():
    pass