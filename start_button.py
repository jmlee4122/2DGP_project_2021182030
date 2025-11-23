from pico2d import draw_rectangle, load_image, get_canvas_height
from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN

from state_machine import StateMachine

def left_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN

class Inactive:
    def __init__(self, button):
        self.button = button

    def enter(self, e):
        self.button.image = load_image("2DGP_background/start_screen/game_start_1.png")

    def exit(self, event):
        pass

    def do(self):
        pass

    def draw(self):
        self.button.image.draw(self.button.x, self.button.y, self.button.width, self.button.height)


class Active:
    def __init__(self, button):
        self.button = button

    def enter(self, e):
        if e[1].type == SDL_MOUSEBUTTONDOWN:
            self.button.is_clicked = True
        self.button.image = load_image("2DGP_background/start_screen/game_start_2.png")

    def exit(self, event):
        pass

    def do(self):
        pass

    def draw(self):
        self.button.image.draw(self.button.x, self.button.y, self.button.width, self.button.height)


class StartButton:
    def __init__(self):
        file_path = "2DGP_background/start_screen/"
        self.image = load_image(file_path + 'game_start_1.png')

        self.x = 1920 / 2
        self.y = 1080 / 2 * 0.6
        self.width = 450
        self.height = 150
        self.is_clicked = False

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
                self.ACTIVE: {mouse_out: self.INACTIVE, left_click: self.ACTIVE}
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
