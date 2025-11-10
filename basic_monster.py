from pico2d import load_image, delay

import game_framework
import game_world
from state_machine import StateMachine


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION_DEATH = 0.3
ACTION_PER_TIME_DEATH = 1.0 / TIME_PER_ACTION_DEATH
FRAMES_PER_ACTION_DEATH = 8

TIME_PER_ACTION_JUMP = 0.3
ACTION_PER_TIME_JUMP = 1.0 / TIME_PER_ACTION_JUMP
FRAMES_PER_ACTION_JUMP = 6
GRAVITY = 9.8  # 중력 가속도 (m/s²)

TIME_PER_ACTION_RUN = 0.3
ACTION_PER_TIME_RUN = 1.0 / TIME_PER_ACTION_JUMP
FRAMES_PER_ACTION_RUN = 6


class Death:
    def __init__(self, user_character):
        pass

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Run:
    def __init__(self, user_character):
        pass

    def enter(self, e):
        pass

    def exit(self, e):
       pass

    def do(self):
        pass

    def draw(self):
       pass

class Idle:
    def __init__(self, user_character):
        pass

    def enter(self, e):
       pass

    def exit(self, e):
       pass

    def do(self):
        pass

    def draw(self):
        pass


class BasicMonster:
    def __init__(self):
        self.x = 1300
        self.y = 400
        self.face_dir = 1 # 1: right, -1: left
        self.delta_move = 0

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.DEATH = Death(self)
        self.STATE_MACHINE = StateMachine(
            self.IDLE,  # 시작상태
            {  # 룰
                self.IDLE: {},
                self.RUN: {},
                self.DEATH: {}  # 죽음 상태에서는 아무 이벤트도 처리하지 않음
            }
        )
    def update(self):
        self.STATE_MACHINE.update()

    def draw(self):
        self.STATE_MACHINE.draw()

    def handle_event(self, event):
        self.STATE_MACHINE.handle_state_event(('INPUT', event))

    def attack(self):
        pass