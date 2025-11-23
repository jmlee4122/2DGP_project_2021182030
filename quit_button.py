from pico2d import load_image, get_canvas_height, draw_rectangle
from sdl2 import SDL_MOUSEMOTION

from state_machine import StateMachine


class Inactive:
    def __init__(self, button):
        self.button = button

    def enter(self, e):
        self.button.text_image = load_image("2DGP_GUI/quit_basic.png")

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        self.button.button_image.draw(self.button.x, self.button.y, self.button.width, self.button.height)
        self.button.text_image.draw(self.button.x, self.button.y, self.button.width, self.button.height)


class Active:
    def __init__(self, button):
        self.button = button

    def enter(self, e):
        self.button.is_active = True
        self.button.text_image = load_image("2DGP_GUI/quit_2.png")

    def exit(self, e):
        self.button.is_active = False

    def do(self):
        pass

    def draw(self):
        self.button.button_image.draw(self.button.x, self.button.y, self.button.width, self.button.height)
        self.button.text_image.draw(self.button.x, self.button.y, self.button.width, self.button.height)

class QuitButton:
    def __init__(self):
        file_path = "2DGP_GUI/"
        self.text_image = load_image(file_path + 'quit_basic.png')
        self.button_image = load_image(file_path + 'button.png')

        self.x = 1920 / 2
        self.y = 1080 * 0.2
        self.width = 450
        self.height = 150
        self.is_active = False

        self.INACTIVE = Inactive(self)
        self.ACTIVE = Active(self)

        def mouse_in(e):
            if e[0] != 'INPUT':
                return False
            ev = e[1]
            if ev.type != SDL_MOUSEMOTION:
                return False
            mx, my = ev.x, ev.y
            my = get_canvas_height() - my
            l, b, r, t = self.get_bb()
            return l <= mx <= r and b <= my <= t
        def mouse_out(e):
            if e[0] != 'INPUT':
                return False
            ev = e[1]
            if ev.type != SDL_MOUSEMOTION:
                return False
            mx, my = ev.x, ev.y
            my = get_canvas_height() - my
            l, b, r, t = self.get_bb()
            return not (l <= mx <= r and b <= my <= t)

        self.STATE_MACHINE = StateMachine(
            self.INACTIVE,  # 시작상태
            {  # 룰
                self.INACTIVE: {mouse_in: self.ACTIVE},
                self.ACTIVE: {mouse_out: self.INACTIVE}
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
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2
