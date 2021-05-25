import pyxel
from pymunk import Space, Vec2d
from layout_builder import LayoutBuilder
from player import Player
from ninja import Ninja
from constants import WIDTH, HEIGHT
from collision_handler import CollisionHandler


class Game:
    FPS = 30
    NINJAS_NUMBER = 8
    GRAVITY = Vec2d(0, 50)

    def __init__(self):
        self.space = Space()
        self.space.gravity = self.GRAVITY
        self.camera_pos = Vec2d(0, 0)

        self.player = Player()
        self.player.enter_space(self.space)

        self.layout_builder = LayoutBuilder()
        self.layout_builder.add_segments_to_space(self.space)

        self.ninjas = []

        for _ in range(self.NINJAS_NUMBER):
            ninja = Ninja()
            ninja.enter_space(self.space)
            self.ninjas.append(ninja)

        collision_handler = CollisionHandler(self.space)
        collision_handler.add_handlers_to_space()

    def update(self):
        if self.player.hit_points <= 0:
            return

        dt = 1 / self.FPS

        self.player.update(self.camera_pos)

        for ninja in self.ninjas:
            ninja.update(self.player.position)

        pos = self.player.position
        self.camera_pos = Vec2d(pos[0], 20) - Vec2d(WIDTH / 2, 0)
        self.space.step(dt)

    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)

        shift = self.camera_pos

        self.layout_builder.draw(shift)
        self.player.draw(shift)

        for ninja in self.ninjas:
            ninja.draw(shift)

        for i in range(self.player.hit_points):
            heart_size = 16
            offset = 5
            x = i * heart_size + i * offset
            y = 0
            heart_position = (x, y)

            image_index = 0
            image_u = 0
            image_v = 2 * heart_size
            image_w = heart_size
            image_h = heart_size

            pyxel.blt(
                *heart_position,
                image_index,
                image_u,
                image_v,
                image_w,
                image_h,
                pyxel.COLOR_YELLOW
            )

    def run(self):
        pyxel.init(WIDTH, HEIGHT, fps=self.FPS)
        pyxel.load("assets.pyxres")
        pyxel.run(self.update, self.draw)


game = Game()
game.run()
