import pyxel
from pymunk import Space, Vec2d
from layout_builder import LayoutBuilder
from player import Player
from ninja import Ninja
from constants import WIDTH, HEIGHT
from collision_handler import CollisionHandler


class Game:
    FPS = 30
    NINJAS_NUMBER = 32
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

    @property
    def game_over(self):
        return self.player.hit_points <= 0

    @property
    def victory(self):
        return not self.ninjas

    def update(self):
        if self.game_over or self.victory:
            return

        dt = 1 / self.FPS

        self.player.update(self.camera_pos)

        for ninja in self.ninjas.copy():
            ninja.update(self.player.position)
            if ninja.hit_points <= 0:
                self.ninjas.remove(ninja)

        pos = self.player.position
        self.camera_pos = Vec2d(pos[0], 20) - Vec2d(WIDTH / 2, 0)
        self.space.step(dt)

    def __draw_hearts(self):
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

        return True

    def __draw_ninja_counter(self):
        image_index = 0
        image_u = 0
        image_v = 48
        image_w = 16
        image_h = 16
        position = (WIDTH - 16, 0)

        pyxel.blt(
            *position,
            image_index,
            image_u,
            image_v,
            image_w,
            image_h,
            pyxel.COLOR_YELLOW
        )

        ninja_counter = self.NINJAS_NUMBER - len(self.ninjas)
        counter_text = f"{ninja_counter}/{self.NINJAS_NUMBER}"
        pyxel.text(
            WIDTH - 32 - len(counter_text),
            5,
            counter_text,
            pyxel.COLOR_BLACK
        )

    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)

        if self.game_over:
            game_over_text = "Game Over"
            pyxel.text(
                WIDTH / 2 - len(game_over_text),
                HEIGHT / 2,
                game_over_text,
                pyxel.COLOR_BLACK
            )

        if self.victory:
            victory_text = "Congratulations!"
            pyxel.text(
                WIDTH / 2 - len(victory_text),
                HEIGHT / 2,
                victory_text,
                pyxel.COLOR_BLACK
            )

        shift = self.camera_pos

        self.layout_builder.draw(shift)
        self.player.draw(shift)

        for ninja in self.ninjas:
            ninja.draw(shift)

        self.__draw_hearts()
        self.__draw_ninja_counter()

    def run(self):
        pyxel.init(WIDTH, HEIGHT, fps=self.FPS)
        pyxel.load("assets.pyxres")
        pyxel.run(self.update, self.draw)


game = Game()
game.run()
