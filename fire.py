from pico2d import *

import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9

class Fire:
    image = None

    def __init__(self, x, y, velocity):
        if not Fire.image:
            file_path = '2DGP_attack/'
            Fire.image = load_image(file_path + 'basic_fire.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.range, self.dis = 700, 0

    def draw(self):
        if self.velocity < 0:
            Fire.image.draw(self.x, self.y, 200, 200)
        else:
            Fire.image.composite_draw(0, 'h', self.x, self.y, 200, 200)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x = self.x + self.velocity
        self.dis = self.dis + self.velocity
        if self.dis > self.range or self.dis < -self.range:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 40, self.y - 20, self.x + 40, self.y + 20
