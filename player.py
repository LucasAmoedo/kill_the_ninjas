import pyxel
from pymunk import Body, Circle, Vec2d

from constants import HEIGHT
from ball_gun import BallGun


class Player:
    BALL_RADIUS = 8
    SPEED = 50
    ORIENTATION_LEFT = 1
    ORIENTATION_RIGHT = -1
    IMAGE_SIZE = BALL_RADIUS * 2

    def __init__(self):
        ball = Body(1.0, 1.0)
        ball_shape = Circle(ball, self.BALL_RADIUS)
        ball.position = (0, HEIGHT - 10)

        self.orientation = self.ORIENTATION_RIGHT

        self.body = ball
        self.shape = ball_shape

        self.ball_gun = BallGun()

    def enter_space(self, space):
        space.add(self.body, self.shape)
        self.space = space

        self.ball_gun.enter_space(space)

    @property
    def position(self):
        return self.body.position

    def move(self, camera_pos):
        ball = self.body
        vx, vy = ball.velocity
        px, py = ball.position

        sx, sy = camera_pos

        if py > HEIGHT + sy:
            ball.position = px, 0

        if pyxel.btn(pyxel.KEY_LEFT):
            ball.velocity = (-self.SPEED, vy)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            ball.velocity = (self.SPEED, vy)
        else:
            ball.velocity = (0, vy)

        if vy == 0.0 and pyxel.btn(pyxel.KEY_UP):
            ball.velocity = (vx, -self.SPEED)

    def shoot(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.ball_gun.fire(self.body.position, self.orientation)

        self.ball_gun.update()

    def update(self, camera_pos):
        self.move(camera_pos)
        self.shoot()

    def draw(self, shift):
        ball_shape = self.shape

        bb = ball_shape.bb

        x, y, _, _ = bb

        player_position = Vec2d(x, y) - shift

        if self.body.velocity.x > 0:
            self.orientation = self.ORIENTATION_RIGHT
        elif self.body.velocity.x < 0:
            self.orientation = self.ORIENTATION_LEFT

        image_page_index = 0
        image_width = self.orientation * self.IMAGE_SIZE
        image_heigth = self.IMAGE_SIZE
        transparent_color = pyxel.COLOR_YELLOW

        image_quantity = 4
        animation_speed = 2

        image_index = int(
            self.body.position.x // animation_speed
        ) % image_quantity

        image_u = self.IMAGE_SIZE * image_index
        image_position = (image_u, self.IMAGE_SIZE)

        pyxel.blt(
            *player_position,
            image_page_index,
            *image_position,
            image_width,
            image_heigth,
            transparent_color
        )

        self.ball_gun.draw(shift)
