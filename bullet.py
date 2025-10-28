from pico2d import *
import game_world

class Bullet:
    image = None
    def __init__(self, x, y, face):
        if not Bullet.image:
            file_path = '2DGP_attack/'
            self.image = load_image(file_path + 'uc_bullet.png')
        self.x, self.y, self.face = x, y, face

    def draw(self):
        self.image.draw(self.x, self.y, 24, 14)
        self.x = self.x + self.face

    def update(self):
        pass