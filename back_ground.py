from pico2d import load_image

from state_machine import StateMachine
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

file_path = '2DGP_background/stage_1/'

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class Stage01:
    def __init__(self, back_ground):
        self.back_ground = back_ground

        self.back_color = load_image(file_path + 'bg_color.png')
        self.tile = load_image(file_path + 'bg_tile.png')
        self.cloud = load_image(file_path + 'bg_cloud.png')
        self.building_1 = load_image(file_path + 'bg_building_stage01_1.png')
        self.building_2 = load_image(file_path + 'bg_building_stage01_2.png')
        self.building_3 = load_image(file_path + 'bg_building_stage01_3.png')
        self.power_pole = load_image(file_path + 'bg_power_pole.png')
        self.fence = load_image(file_path + 'bg_fence.png')

    def do(self):
        pass

    def enter(self, e):
        print("enter Stage01")

    def exit(self, e):
        pass

    def draw(self):
        self.back_color.draw(1920 / 2, 1080 / 2)
        self.cloud.draw(1920 / 2, 1080 / 2)
        self.building_1.draw(1300, 1080 / 2, 500, 1000)
        self.building_2.draw(800, 300, 600, 800)
        self.building_3.draw(400, 1080 / 2, 500, 1000)
        self.fence.draw(1920 / 2, 650)
        self.tile.draw(1920 / 2, 1080 / 2)
        self.power_pole.draw(1600, 1080 / 2)

class Stage02:
    def __init__(self, back_ground):
        self.back_ground = back_ground

        self.back_color = load_image(file_path + 'bg_color.png')

    def do(self):
        pass

    def enter(self, e):
        print("enter Stage02")

    def exit(self, e):
        pass

    def draw(self):
        self.back_color.draw(1920 / 2, 1080 / 2)

class Stage03:
    def __init__(self, back_ground):
        self.back_ground = back_ground

        self.back_color = load_image(file_path + 'bg_color.png')
        self.cloud = load_image(file_path + 'bg_cloud.png')

    def do(self):
        pass

    def enter(self, e):
        print("enter Stage03")

    def exit(self, e):
        pass

    def draw(self):
        self.back_color.draw(1920 / 2, 1080 / 2)
        self.cloud.draw(1920 / 2, 1080 / 2)


class BackGround:
    def __init__(self):
        self.STAGE_01 = Stage01(self)
        self.STAGE_02 = Stage02(self)
        self.STAGE_03 = Stage03(self)
        self.STATE_MACHINE = StateMachine(
            self.STAGE_01,
            {
                self.STAGE_01: {space_down: self.STAGE_02},
                self.STAGE_02: {space_down: self.STAGE_03},
                self.STAGE_03: {space_down: self.STAGE_01}
            }
        )

    def update(self):
        self.STATE_MACHINE.update() # 상태 머신으로 하여금 업데이트

    def draw(self):
        self.STATE_MACHINE.draw() # 상태 머신으로 하여금 그리기

    def handle_event(self, event):
        self.STATE_MACHINE.handle_state_event(('INPUT', event))
