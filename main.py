import pyxel


class Game:
    WIDTH = 100
    HEIGHT = 100

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        pyxel.init(self.WIDTH, self.HEIGHT)
        pyxel.run(self.update, self.draw)


game = Game()
game.run()

