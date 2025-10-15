from pico2d import load_image

from state_machine import StateMachine

file_path = '2DGP_background/stage_1/'

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
        pass

    def do(self):
        print("enter Stage01")
        pass

    def enter(self):
        pass

    def exit(self):
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
        pass

class Stage02:
    def __init__(self, back_ground):
        pass

class Stage03:
    def __init__(self, back_ground):
        pass


class BackGround:
    def __init__(self):
        self.STAGE = Stage01(self)
        self.STATE_MACHINE = StateMachine(self.STAGE)
        pass

    # def update(self):
    #     self.STATE_MACHINE.update() # 상태 머신으로 하여금 업데이트

    def draw(self):
        self.STATE_MACHINE.draw() # 상태 머신으로 하여금 그리기
        pass
