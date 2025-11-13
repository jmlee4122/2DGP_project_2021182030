from pico2d import load_image, get_time, draw_rectangle, load_font

import game_framework
import game_world
from slash import Slash
from state_machine import StateMachine

def hp_depleted(e):
    return e[0] == 'HP' and e[1] == 'DEATH'

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION_DEATH = 1.0
ACTION_PER_TIME_DEATH = 1.0 / TIME_PER_ACTION_DEATH
FRAMES_PER_ACTION_DEATH = 8

TIME_PER_ACTION_IDLE = 1.5
ACTION_PER_TIME_IDLE = 1.0 / TIME_PER_ACTION_IDLE
FRAMES_PER_ACTION_IDLE = 5

class Death:
    def __init__(self, boss_monster):
        self.boss = boss_monster
        self.frame = 0
        self.clip_height = 0

    def enter(self, e):
        file_path = '2DGP_character/boss_monster/'
        self.boss.image = load_image(file_path + 'boss_death_sprite_sheet.png')
        self.boss.frame = 0
        self.boss.clip_size_x = 402
        self.boss.clip_size_y = 382

        self.frame = 0
        self.clip_height = 0

    def exit(self, e):
        self.boss.frame = 0
        self.frame = 0
        self.clip_height = 0

    def do(self):
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION_DEATH * ACTION_PER_TIME_DEATH * game_framework.frame_time) % 10
        self.frame = int(self.boss.frame)
        if self.frame >= 9:
            self.boss.is_dead = True
        if self.boss.face_dir == 1:
            if self.frame < 5:
                self.clip_height = 1
            else:
                self.frame -= 5
                self.clip_height = 0
        elif self.boss .face_dir == -1:
            if self.frame < 5:
                self.clip_height = 3
            else:
                self.frame -= 5
                self.clip_height = 2


    def draw(self):
        if self.boss.face_dir == 1:
            self.boss.image.clip_draw(self.frame * self.boss.clip_size_x, self.clip_height * self.boss.clip_size_y,
                                       self.boss.clip_size_x, self.boss.clip_size_y, self.boss.x, self.boss.y)
        elif self.boss.face_dir == -1:
            self.boss.image.clip_draw(self.frame * self.boss.clip_size_x, self.clip_height * self.boss.clip_size_y,
                                       self.boss.clip_size_x, self.boss.clip_size_y, self.boss.x, self.boss.y)

class Idle:
    def __init__(self, boss_monster):
        self.boss = boss_monster

    def enter(self, e):
        file_path = '2DGP_character/boss_monster/'
        self.boss.image = load_image(file_path + 'boss_idle_sprite_sheet.png')
        self.boss.clip_size_x = 402
        self.boss.clip_size_y = 382
        self.boss.wait_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME_IDLE * game_framework.frame_time) % 5
        if self.boss.user.x < self.boss.x:
            self.boss.face_dir = -1
        else:
            self.boss.face_dir = 1
        if get_time() - self.boss.wait_time > 1.5:
            self.boss.attack()
            self.boss.wait_time = get_time()

    def draw(self):
        if self.boss.face_dir == 1:
            self.boss.image.clip_draw(int(self.boss.frame) * self.boss.clip_size_x, 0 * self.boss.clip_size_y,
                                       self.boss.clip_size_x, self.boss.clip_size_y, self.boss.x, self.boss.y)
        elif self.boss.face_dir == -1:
            self.boss.image.clip_draw(int(self.boss.frame) * self.boss.clip_size_x, 1 * self.boss.clip_size_y,
                                       self.boss.clip_size_x, self.boss.clip_size_y, self.boss.x, self.boss.y)


class BossMonster:
    def __init__(self, x, y, user_char = None):
        self.hp = 100
        self.x = x
        self.y = y
        self.face_dir = -1 # 1: right, -1: left
        self.delta_move = 0
        self.frame = 0

        self.font = load_font('ENCR10B.TTF', 16)

        self.clip_size_x = 0
        self.clip_size_y = 0

        file_path = '2DGP_character/boss_monster/'
        self.image = load_image(file_path + 'boss_idle_sprite_sheet.png')

        self.user = user_char
        self.is_dead = False

        self.IDLE = Idle(self)
        self.DEATH = Death(self)
        self.STATE_MACHINE = StateMachine(
            self.IDLE,  # 시작상태
            {  # 룰
                self.IDLE: {hp_depleted: self.DEATH},
                self.DEATH: {}  # 죽음 상태에서는 아무 이벤트도 처리하지 않음
            }
        )

    def update(self):
        if self.is_dead:
            game_world.remove_object(self)
            game_world.enemies.remove(self)
            if game_world.is_need_stage_switch():
                game_world.stage_switch_requested = True
        self.STATE_MACHINE.update()

    def draw(self):
        self.STATE_MACHINE.draw()
        self.font.draw(self.x - 40, self.y + 100, f'Hp {self.hp:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.STATE_MACHINE.handle_state_event(('INPUT', event))

    def attack(self):
        loc_x = 180 * self.face_dir
        loc_y = 20
        slash = Slash(self.x + loc_x, self.y + loc_y, self.face_dir * 10)
        game_world.add_object(slash, 1)
        #game_world.add_collision_pair('uc:fire', None, fire)

    def get_bb(self):
        return self.x - 80, self.y - 140, self.x + 50, self.y + 180

    # def handle_collision(self, group, other):
    #     if group == 'basic:bullet':
    #         damage = 10
    #         self.hp -= damage
    #         print('basic:bullet collision')
    #         if self.hp <= 0:
    #             self.STATE_MACHINE.handle_state_event(('HP', 'DEATH'))