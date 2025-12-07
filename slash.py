from pico2d import load_image, draw_rectangle

import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Slash:
    image = None

    def __init__(self, x, y, velocity):
        if not Slash.image:
            file_path = '2DGP_attack/'
            Slash.image = load_image(file_path + 'boss_slash.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.range, self.dis = 700, 0
        self.frame = 0

    def draw(self):
        if self.velocity < 0:
            Slash.image.clip_draw(int(self.frame) * 300, 0, 300, 300, self.x, self.y)
        else:
            Slash.image.clip_composite_draw(int(self.frame) * 300, 0, 300, 300, 0, 'h', self.x, self.y)
        #draw_rectangle(*self.get_bb())

    def update(self):
        dt = min(game_framework.frame_time, 0.06)
        dx = self.velocity * dt * PIXEL_PER_METER
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.x += dx
        self.dis += abs(dx)
        if self.dis > self.range:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 140, self.y - 140, self.x + 140, self.y + 140

    def handle_collision(self, group, other):
        if group == 'uc:slash':
            game_world.remove_object(self)
