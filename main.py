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
    pass

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()
    pass


open_canvas(1920, 1080)
reset_world()

while True:
    # handle_events()
    # update_world()
    render_world()
    delay(1)

close_canvas()