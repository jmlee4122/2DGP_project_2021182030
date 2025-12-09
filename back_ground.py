from pico2d import load_image, load_music

import game_world
from game_world import enemies
from state_machine import StateMachine

def switch_to_stage01(e):
    return e[0] == 'NEXT' and e[1] == 'STAGE01'
def switch_to_stage02(e):
    return e[0] == 'NEXT' and e[1] == 'STAGE02'
def switch_to_stage03(e):
    return e[0] == 'NEXT' and e[1] == 'STAGE03'

class Stage01:
    def __init__(self, back_ground):
        file_path = '2DGP_background/stage_1/'
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
        if self.back_ground.need_switch:
            self.back_ground.STATE_MACHINE.handle_state_event(('NEXT', 'STAGE02'))

    def enter(self, e):
        self.back_ground.need_switch = False
        self.back_ground.stage_num = 1
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
        file_path = '2DGP_background/stage_2/'
        self.back_ground = back_ground

        self.back_color = load_image(file_path + 'bg_color.png')
        self.tile = load_image(file_path + 'bg_tile.png')
        self.cloud = load_image(file_path + 'bg_cloud.png')
        self.building_1 = load_image(file_path + 'bg_building_stage02_1.png')
        self.building_2 = load_image(file_path + 'bg_building_stage02_2.png')
        self.mid_sign = load_image(file_path + 'bg_mid_sign.png')
        self.fence = load_image(file_path + 'bg_fence.png')

    def do(self):
        if self.back_ground.need_switch:
            self.back_ground.STATE_MACHINE.handle_state_event(('NEXT', 'STAGE03'))

    def enter(self, e):
        self.back_ground.need_switch = False
        self.back_ground.stage_num = 2
        print("enter Stage02")

    def exit(self, e):
        pass

    def draw(self):
        self.back_color.draw(1920 / 2, 1080 / 2)
        self.cloud.draw(1920 / 2, 1080 / 2)
        self.building_1.draw(1300, 1080 / 2, 500, 1000)
        self.building_2.draw(800, 500, 600, 800)
        self.fence.draw(1920 / 2, 650)
        self.tile.draw(1920 / 2, 1080 / 2)
        self.mid_sign.draw(1600, 1080 / 2)

class Stage03:
    def __init__(self, back_ground):
        file_path = '2DGP_background/stage_3/'
        self.back_ground = back_ground

        self.back_color = load_image(file_path + 'bg_color.png')
        self.tile = load_image(file_path + 'bg_tile.png')
        self.cloud = load_image(file_path + 'bg_cloud.png')
        self.building_1 = load_image(file_path + 'bg_building_stage03_1.png')
        self.building_2 = load_image(file_path + 'bg_building_stage03_2.png')
        self.power_pole = load_image(file_path + 'bg_power_pole.png')
        self.fence = load_image(file_path + 'bg_fence.png')

    def do(self):
        if self.back_ground.need_switch:
            self.back_ground.STATE_MACHINE.handle_state_event(('NEXT', 'STAGE01'))

    def enter(self, e):
        self.back_ground.need_switch = False
        self.back_ground.stage_num = 3
        print("enter Stage03")

    def exit(self, e):
        pass

    def draw(self):
        self.back_color.draw(1920 / 2, 1080 / 2)
        self.cloud.draw(1920 / 2, 1080 / 2)
        self.building_1.draw(1300, 1080 / 2, 500, 1000)
        self.building_2.draw(300, 1080 / 2, 600, 800)
        self.fence.draw(1920 / 2, 650)
        self.tile.draw(1920 / 2, 1080 / 2)
        self.power_pole.draw(400, 1080 / 2)


class BackGround:
    def __init__(self, last_stage):
        self.need_switch = False
        self.stage_num = 1
        self.STAGE_01 = Stage01(self)
        self.STAGE_02 = Stage02(self)
        self.STAGE_03 = Stage03(self)

        self.initial_stage = self.STAGE_01
        if last_stage == 0:
            self.initial_stage = self.STAGE_01
        elif last_stage == 1:
            self.initial_stage = self.STAGE_02
        elif last_stage == 2:
            self.initial_stage = self.STAGE_03
        self.STATE_MACHINE = StateMachine(
            self.initial_stage,
            {
                self.STAGE_01: {switch_to_stage02: self.STAGE_02},
                self.STAGE_02: {switch_to_stage03: self.STAGE_03},
                self.STAGE_03: {switch_to_stage01: self.STAGE_01}
            }
        )

    def update(self):
        if game_world.stage_switch_requested:
            self.need_switch = True
            game_world.stage_switch_requested = False
        self.STATE_MACHINE.update() # 상태 머신으로 하여금 업데이트

    def draw(self):
        self.STATE_MACHINE.draw() # 상태 머신으로 하여금 그리기

    def handle_event(self, event):
        pass
