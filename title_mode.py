from pico2d import *

import exit_button
import game_framework
import play_mode
import start_button
from exit_button import ExitButton
from start_button import StartButton

image = None

def init():
    # 타이틀 이미지를 로드
    file_path = "2DGP_background/start_screen/"
    global image
    global start_button
    global exit_button

    image = load_image(file_path + 'start_screen.png')
    start_button = StartButton()
    exit_button = ExitButton()
    # 디버그 출력: 실제 캔버스와 이미지 크기 확인
    try:
        canvas_w, canvas_h = get_canvas_width(), get_canvas_height()
        #print(f"[DEBUG] canvas: {canvas_w}x{canvas_h}, image: {image.w}x{image.h}")
    except Exception:
        #print("[DEBUG] init: unable to read canvas/image sizes")
        pass


def update():
    if start_button is not None:
        if start_button.is_clicked:
            game_framework.change_mode(play_mode)
    if exit_button is not None:
        if exit_button.is_clicked:
            game_framework.quit()
#game_framework.change_mode(play_mode)


def draw():
    # 이미지가 로드되지 않았으면 빈 캔버스만 업데이트
    clear_canvas()
    if image is None:
        update_canvas()
        return

    # 캔버스 크기를 그대로 사용하여 이미지를 캔버스에 맞춤
    canvas_w, canvas_h = get_canvas_width(), get_canvas_height()
    cx = canvas_w // 2
    cy = canvas_h // 2

    # 캔버스 크기로 강제로 그려서 어떤 화면 배율에서도 동일하게 보이게 함
    image.draw(cx, cy, canvas_w, canvas_h)
    start_button.draw()
    exit_button.draw()
    update_canvas()


def finish():
    global image
    global start_button
    global exit_button

    if start_button is not None:
        del start_button
        start_button = None

    if exit_button is not None:
        del exit_button
        exit_button = None

    # 타이틀 이미지 정리
    if image is not None:
        del image
        image = None

def handle_events():
    event_list = get_events() #현재까지 들어온 이벤트를 받아온다.
    # space 키 이벤트 처리
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if start_button is not None:
                start_button.handle_event(event)
            if exit_button is not None:
                exit_button.handle_event(event)


def pause():
    pass


def resume():
    pass