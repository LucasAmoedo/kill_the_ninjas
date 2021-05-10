import pyxel
from pymunk import Space, Body, Circle, Vec2d


class Game:
    WIDTH = 256
    HEIGHT = 200
    FPS = 30
    GRAVITY = Vec2d(0, 50)
    BALL_RADIUS = 10

    def __init__(self):
        self.space = Space()
        self.space.gravity = self.GRAVITY

        # Create a ball
        ball = Body(1.0, 1.0)
        ball_shape = Circle(ball, self.BALL_RADIUS)
        ball.position = (self.WIDTH / 2, 0)
        self.space.add(ball, ball_shape)
        self.player = ball

    def update(self):
        ball = self.player
        x, y = ball.position
        if y > self.HEIGHT + self.BALL_RADIUS:
            ball.position = x, 0
            
        dt = 1 / self.FPS
        self.space.step(dt)
        print(self.player.position)

    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)

        # Desenha bola
        ball = self.player
        pyxel.circ(*ball.position, self.BALL_RADIUS, pyxel.COLOR_RED)

    def run(self):
        pyxel.init(self.WIDTH, self.HEIGHT, fps=self.FPS)
        pyxel.run(self.update, self.draw)


game = Game()
game.run()

