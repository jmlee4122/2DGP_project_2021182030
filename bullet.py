from pico2d import *
import game_world

class Bullet:
    image = None
    def __init__(self, x, y, velocity):
        if not Bullet.image:
            file_path = '2DGP_attack/'
            self.image = load_image(file_path + 'uc_bullet.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.range, self.dis = 500, 0

    def draw(self):
        self.image.draw(self.x, self.y, 24, 14)


    def update(self):
        self.x = self.x + self.velocity
        self.dis = self.dis + self.velocity
        if self.dis > self.range or self.dis < -self.range:
            game_world.remove_object(self)