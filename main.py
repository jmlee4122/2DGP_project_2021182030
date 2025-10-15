from pico2d import *

from back_ground import BackGround

def reset_world():
    global world
    global backGround

    world = []

    backGround = BackGround()
    world.append(backGround)
    pass

def handle_events():
    global running
    global back_ground_update

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_SPACE: # 스페이스바를 누르면 배경이 바뀜 (테스트 용도)
                back_ground_update = True

def update_world():
    global back_ground_update
    for o in world:
        if o == backGround:
            if back_ground_update:
                o.update()
                back_ground_update = False
        else:
            o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()
    pass

running = True
back_ground_update = False

open_canvas(1920, 1080)
reset_world()

while running:
    update_world()
    render_world()
    handle_events()
    delay(0.01)

close_canvas()