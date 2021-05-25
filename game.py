import pyxel
from pymunk import Space, Vec2d
from layout_builder import LayoutBuilder
from player import Player
from ninja import Ninja
from constants import (
    WIDTH,
    HEIGHT,
    BULLET_COLLISION_TYPE,
    NINJA_COLLISION_TYPE
)


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


        bullet_ninja_collision_handler = self.space.add_collision_handler(
            BULLET_COLLISION_TYPE,
            NINJA_COLLISION_TYPE
        )

        def handle_bullet_ninja_collision(arbiter, space, data):
            _, ninja_shape = arbiter.shapes
            ninja = ninja_shape.body.reference
            ninja.hit_points -= 1

            return True

        bullet_ninja_collision_handler.begin = handle_bullet_ninja_collision

    def update(self):
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
        shift = Vec2d(0, 0)

        self.layout_builder.draw(shift)
        self.player.draw(shift)

        for ninja in self.ninjas:
            ninja.draw(shift)

    def run(self):
        pyxel.init(WIDTH, HEIGHT, fps=self.FPS)
        pyxel.load("assets.pyxres")
        pyxel.run(self.update, self.draw)


game = Game()
game.run()
