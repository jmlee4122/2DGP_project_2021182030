from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a
from state_machine import StateMachine

class Death:
    def __init__(self, user_character):
        self.user_char = user_character

    def enter(self, e):
       pass

    def exit(self, e):
        pass

    def do(self):
       pass

    def draw(self):
       pass

class Jump:
    def __init__(self, user_character):
        self.user_char = user_character

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
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_idle_sprite_sheet.png')
        self.clip_width = 402
        self.clip_height = 382
        self.clip_bottom = 0

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
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_idle_sprite_sheet.png')
        self.clip_width = 402
        self.clip_height = 382
        self.clip_bottom = 0

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        if self.uc.face_dir == 1:  # right
            self.image.clip_draw(
                3 * self.clip_width, self.clip_bottom, self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
            )
        else:  # face_dir == -1: # left
            self.image.clip_draw(
                0 * self.clip_width, self.clip_bottom, self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
            )

class UserChar:
    def __init__(self):

        self.x, self.y = 960, 400
        self.frame = 0
        self.face_dir = 1 # 1: right, -1: left
        self.delta_move = 0

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.DEATH = Death(self)
        self.STATE_MACHINE = StateMachine(
            self.IDLE,  # 시작상태
            {  # 룰
                self.IDLE: {},
                self.RUN: {},
                self.JUMP: {},
                self.DEATH: {}
            }
        )

    def update(self):
        self.STATE_MACHINE.update()

    def draw(self):
        self.STATE_MACHINE.draw()

    def handle_event(self, event):
        self.STATE_MACHINE.handle_state_event(('INPUT', event))