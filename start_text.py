from pico2d import draw_rectangle, load_image, get_canvas_height, load_wav
from sdl2 import SDL_MOUSEMOTION

from state_machine import StateMachine

class Inactive:
    def __init__(self, text):
        self.text = text

    def enter(self, e):
        self.text.image = load_image("2DGP_background/start_screen/game_start_1.png")

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        self.text.image.draw(self.text.x, self.text.y, self.text.width, self.text.height)


class Active:
    def __init__(self, text):
        self.text = text

    def enter(self, e):
        self.text.is_active = True
        self.text.image = load_image("2DGP_background/start_screen/game_start_2.png")
        StartText.sound.play()

    def exit(self, e):
        self.text.is_active = False

    def do(self):
        pass

    def draw(self):
        self.text.image.draw(self.text.x, self.text.y, self.text.width, self.text.height)


class StartText:
    sound = None
    def __init__(self):
        if StartText.sound is None:
            StartText.sound = load_wav("2DGP_sound/button_hover_sound.wav")
            StartText.sound.set_volume(32)
        file_path = "2DGP_background/start_screen/"
        self.image = load_image(file_path + 'game_start_1.png')

        self.x = 1920 / 2
        self.y = 1080 / 2 * 0.6
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
        #draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.STATE_MACHINE.handle_state_event(('INPUT', event))

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2
