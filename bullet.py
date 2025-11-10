from pico2d import *
import game_world

class Bullet:
    image = None
    def __init__(self, x, y, velocity):
        if not Bullet.image:
            file_path = '2DGP_attack/'
            Bullet.image = load_image(file_path + 'uc_bullet.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.range, self.dis = 500, 0

    def draw(self):
        if self.velocity > 0:
            Bullet.image.draw(self.x, self.y, 24, 14)
        else:
            Bullet.image.composite_draw(0, 'h', self.x, self.y, 24, 14)
        draw_rectangle(*self.get_bb())


    def update(self):
        self.x = self.x + self.velocity
        self.dis = self.dis + self.velocity
        if self.dis > self.range or self.dis < -self.range:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 5, self.x + 10, self.y + 5