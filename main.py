from pico2d import *


# background = load_image('BG_1_1.png') stage 1~3 동일
# cloud = load_image('BG_cloud_1_6.png') stage 1~3 동일

def reset_world():
    pass

def handle_events():
    pass

def update_world():
    pass

def render_world():
    pass


open_canvas(1920, 1080)
reset_world()

while True:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()