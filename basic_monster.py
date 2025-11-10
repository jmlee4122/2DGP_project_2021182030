from pico2d import load_image, get_time
from sdl2 import SDLK_b, SDL_KEYDOWN

import game_framework
import game_world
from fire import Fire
from state_machine import StateMachine

def b_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_b
time_out = lambda e: e[0] == 'TIMEOUT'

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION_DEATH = 0.3
ACTION_PER_TIME_DEATH = 1.0 / TIME_PER_ACTION_DEATH
FRAMES_PER_ACTION_DEATH = 8

TIME_PER_ACTION_IDLE = 1.0
ACTION_PER_TIME_IDLE = 1.0 / TIME_PER_ACTION_IDLE
FRAMES_PER_ACTION_IDLE = 5

class Death:
    def __init__(self, basic_monster):
        self.basic = basic_monster
        self.frame = 0
        self.clip_height = 0

    def enter(self, e):
        file_path = '2DGP_character/basic_monster/'
        self.basic.image = load_image(file_path + 'basic_death_sprite_sheet.png')
        self.basic.frame = 0
        self.basic.clip_size_x = 402
        self.basic.clip_size_y = 382

        self.frame = 0
        self.clip_height = 0

    def exit(self, e):
        self.basic.frame = 0
        self.frame = 0
        self.clip_height = 0

    def do(self):
        self.basic.frame = (self.basic.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME_IDLE * game_framework.frame_time) % 10
        self.frame = int(self.basic.frame)
        if self.frame >= 9:
            self.basic.is_dead = True
        if self.basic.face_dir == 1:
            if self.frame < 5:
                self.clip_height = 1
            else:
                self.frame -= 5
                self.clip_height = 0
        elif self.basic .face_dir == -1:
            if self.frame < 5:
                self.clip_height = 3
            else:
                self.frame -= 5
                self.clip_height = 2


    def draw(self):
        if self.basic.face_dir == 1:
            self.basic.image.clip_draw(self.frame * self.basic.clip_size_x, self.clip_height * self.basic.clip_size_y,
                                       self.basic.clip_size_x, self.basic.clip_size_y, self.basic.x, self.basic.y)
        elif self.basic.face_dir == -1:
            self.basic.image.clip_draw(self.frame * self.basic.clip_size_x, self.clip_height * self.basic.clip_size_y,
                                       self.basic.clip_size_x, self.basic.clip_size_y, self.basic.x, self.basic.y)

class Idle:
    def __init__(self, basic_monster):
        self.basic = basic_monster

    def enter(self, e):
        file_path = '2DGP_character/basic_monster/'
        self.basic.image = load_image(file_path + 'basic_idle_sprite_sheet.png')
        self.basic.frame = 0
        self.basic.clip_size_x = 402
        self.basic.clip_size_y = 382
        self.basic.wait_time = get_time()

    def exit(self, e):
        if e and e[0] == 'TIMEOUT':
            self.basic.attack()
            self.basic.is_attacking = True

    def do(self):
        self.basic.frame = (self.basic.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME_IDLE * game_framework.frame_time) % 5
        self.basic.frame = 0
        if self.basic.user.x < self.basic.x:
            self.basic.face_dir = -1
        else:
            self.basic.face_dir = 1
        if get_time() - self.basic.wait_time > 3:
            self.basic.STATE_MACHINE.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.basic.face_dir == 1:
            self.basic.image.clip_draw(0, 0 * self.basic.clip_size_y, self.basic.clip_size_x, self.basic.clip_size_y,
                                       self.basic.x, self.basic.y)
        elif self.basic.face_dir == -1:
            self.basic.image.clip_draw(0, 1 * self.basic.clip_size_y, self.basic.clip_size_x, self.basic.clip_size_y,
                                       self.basic.x, self.basic.y)
        # if self.basic.face_dir == 1:
        #     self.basic.image.clip_draw(int(self.basic.frame) * self.basic.clip_size_x, 0 * self.basic.clip_size_y,
        #                                self.basic.clip_size_x, self.basic.clip_size_y, self.basic.x, self.basic.y)
        # elif self.basic.face_dir == -1:
        #     self.basic.image.clip_draw(int(self.basic.frame) * self.basic.clip_size_x, 1 * self.basic.clip_size_y,
        #                                self.basic.clip_size_x, self.basic.clip_size_y, self.basic.x, self.basic.y)


class BasicMonster:
    def __init__(self, user_char = None):
        self.x = 1300
        self.y = 420
        self.face_dir = -1 # 1: right, -1: left
        self.delta_move = 0
        self.frame = 0

        self.clip_size_x = 0
        self.clip_size_y = 0

        file_path = '2DGP_character/basic_monster/'
        self.image = load_image(file_path + 'basic_idle_sprite_sheet.png')

        self.user = user_char
        self.is_dead = False

        self.IDLE = Idle(self)
        self.DEATH = Death(self)
        self.STATE_MACHINE = StateMachine(
            self.IDLE,  # 시작상태
            {  # 룰
                self.IDLE: {time_out: self.IDLE},
                self.DEATH: {}  # 죽음 상태에서는 아무 이벤트도 처리하지 않음
            }
        )

    def update(self):
        if self.is_dead:
            game_world.remove_object(self)
        self.STATE_MACHINE.update()

    def draw(self):
        self.STATE_MACHINE.draw()

    def handle_event(self, event):
        self.STATE_MACHINE.handle_state_event(('INPUT', event))

    def attack(self):
        loc_x = 180 * self.face_dir
        loc_y = 20
        fire = Fire(self.x + loc_x, self.y + loc_y, self.face_dir * 3)
        game_world.add_object(fire, 1)