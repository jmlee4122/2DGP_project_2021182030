from pico2d import load_image, get_time, delay
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a
from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

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
        self.image = load_image(file_path + 'user_running_sprite_sheet.png')
        self.clip_width = 402
        self.clip_height = 382
        self.clip_bottom = 0
        self.frame = 0
        self.frame_delay = 0

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.uc.delta_move = self.uc.face_dir = 1
            self.clip_bottom = 0
        elif left_down(e) or right_up(e):
            self.uc.delta_move = self.uc.face_dir = -1
            self.clip_bottom = 2

    def exit(self, e):
        pass

    def do(self):
        self.uc.frame = (self.uc.frame + 1) % 12
        self.frame = self.uc.frame
        self.uc.x += self.uc.delta_move * 8

        if self.uc.face_dir == 1 and self.uc.frame >= 6:
            self.clip_bottom = 1
            self.frame -= 6
        elif self.uc.face_dir == -1 and self.uc.frame >= 6:
            self.clip_bottom = 3
            self.frame -= 6

    def draw(self):
        if self.uc.face_dir == 1:  # right
            self.image.clip_draw(
                self.frame * self.clip_width, self.clip_bottom * self.clip_height,
                self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
            )
        else:  # face_dir == -1: # left
            self.image.clip_draw(
                self.frame * self.clip_width, self.clip_bottom * self.clip_height,
                self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
            )
        delay(0.005)



class Idle:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_idle_sprite_sheet.png')
        self.clip_width = 402
        self.clip_height = 382
        self.clip_bottom = 0

    def enter(self, e):
        self.uc.delta_move = 0

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        if self.uc.face_dir == 1:  # right
            self.image.clip_draw(
                3 * self.clip_width, self.clip_bottom * self.clip_height,
                self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
            )
        else:  # face_dir == -1: # left
            self.image.clip_draw(
                0 * self.clip_width, self.clip_bottom * self.clip_height,
                self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
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
                self.IDLE: {right_up: self.RUN, left_up: self.RUN, right_down: self.RUN, left_down: self.RUN},
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE},
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