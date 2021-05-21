import pyxel
from pymunk import Space, Body, Circle, Vec2d, Segment, BB


class Game:
    WIDTH = 256
    HEIGHT = 200
    FPS = 30
    GRAVITY = Vec2d(0, 50)
    BALL_RADIUS = 8
    GROUND_RADIUS = 3
    PLAYER_SPEED = 50
    SCREEN = Vec2d(WIDTH, HEIGHT)
    PLAYER_ORIENTATION_LEFT = 1
    PLAYER_ORIENTATION_RIGHT = -1
    PLAYER_IMAGE_SIZE = BALL_RADIUS * 2

    def __init__(self):
        self.space = Space()
        self.space.gravity = self.GRAVITY
        self.camera_pos = Vec2d(0, 0)
        self.player_orientation = self.PLAYER_ORIENTATION_RIGHT

        x, y = self.WIDTH, self.HEIGHT
        # Create a ball
        ball = Body(1.0, 1.0)
        ball_shape = Circle(ball, self.BALL_RADIUS)
        ball.position = (0, y - self.BALL_RADIUS)
        self.space.add(ball, ball_shape)
        self.player = ball

        # Crate the ground
        ground = self.space.static_body
        ground_shape = Segment(ground, (0, y), (x/2, y), self.GROUND_RADIUS)
        self.space.add(ground_shape)

        self.ground = ground

    def update(self):
        dt = 1 / self.FPS

        ball = self.player
        vx, vy = ball.velocity
        px, py = ball.position

        sx, sy = self.camera_pos

        if py > self.HEIGHT + sy:
            ball.position = px, 0

        if pyxel.btn(pyxel.KEY_LEFT):
            ball.velocity = (-self.PLAYER_SPEED, vy)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            ball.velocity = (self.PLAYER_SPEED, vy)
        else:
            ball.velocity = (0, vy)

        if vy == 0.0 and pyxel.btn(pyxel.KEY_UP):
            ball.velocity = (vx, -self.PLAYER_SPEED)
        
        pos = self.player.position
        self.camera_pos = Vec2d(pos[0], 20) - Vec2d(self.WIDTH / 2, 0)
        self.space.step(dt)

    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)
        shift = self.camera_pos

        # Desenha bola
        ball = self.player
        ball_shape = list(ball.shapes)[0]

        bb = ball_shape.bb

        x, y, _, _ = bb

        player_position = Vec2d(x, y) - shift

        # pyxel.circ(
        #     *self.player.position - shift,
        #     self.BALL_RADIUS,
        #     pyxel.COLOR_YELLOW
        # )

        if self.player.velocity.x > 0:
            self.player_orientation = self.PLAYER_ORIENTATION_RIGHT
        elif self.player.velocity.x < 0:
            self.player_orientation = self.PLAYER_ORIENTATION_LEFT

        image_page_index = 0
        image_width = self.player_orientation * self.PLAYER_IMAGE_SIZE
        image_heigth = self.PLAYER_IMAGE_SIZE
        transparent_color = pyxel.COLOR_YELLOW

        image_quantity = 4
        animation_speed = 2
        image_index = int(
            self.player.position.x // animation_speed
        ) % image_quantity

        image_u = self.PLAYER_IMAGE_SIZE * image_index
        image_position = (image_u, self.PLAYER_IMAGE_SIZE)

        pyxel.blt(
            *player_position,
            image_page_index,
            *image_position,
            image_width,
            image_heigth,
            transparent_color
        )

        # Desenha o chão
        ground = self.ground
        ground_shape = list(ground.shapes)[0]
        bb : BB = ground_shape.bb
        p = Vec2d(bb.left, bb.bottom) - shift
        w = bb.right - bb.left
        h = self.GROUND_RADIUS
        pyxel.rect(*p, w, h, pyxel.COLOR_GREEN)

    def run(self):
        pyxel.init(self.WIDTH, self.HEIGHT, fps=self.FPS)

        pyxel.load("assets.pyxres")

        pyxel.run(self.update, self.draw)


game = Game()
game.run()
