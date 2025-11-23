from pico2d import load_image
from pico2d import draw_rectangle
from state_machine import StateMachine


class Inactive:
    def __init__(self, button):
        self.button = button

    def enter(self, event):
        self.button.image = load_image("2DGP_background/start_screen/exit_1.png")

    def exit(self, event):
        pass

    def do(self):
        pass

    def draw(self):
        self.button.image.draw(self.button.x, self.button.y, self.button.width, self.button.height)

class Active:
    def __init__(self, button):
        self.button = button

    def enter(self, event):
        self.button.image = load_image("2DGP_background/start_screen/exit_2.png")

    def exit(self, event):
        pass

    def do(self):
        pass

    def draw(self):
        self.button.image.draw(self.button.x, self.button.y, self.button.width, self.button.height)

class Exit_button:
    def __init__(self):
        file_path = "2DGP_background/start_screen/"
        self.image = load_image(file_path + 'exit_1.png')

        self.x = 1920 / 2
        self.y = 1080 / 2 * 0.3
        self.width = 450
        self.height = 150

        self.INACTIVE = Inactive(self)
        self.ACTIVE = Active(self)
        self.STATE_MACHINE = StateMachine(
            self.INACTIVE,  # 시작상태
            {  # 룰
                self.INACTIVE: {},
                self.ACTIVE: {}
            }
        )

    def update(self):
        self.STATE_MACHINE.update()

    def draw(self):
        self.STATE_MACHINE.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.STATE_MACHINE.handle_state_event(('INPUT', event))

    def get_bb(self):
        return self.x - self.width / 4, self.y - self.height / 2, self.x + self.width / 4, self.y + self.height / 2