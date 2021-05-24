import pyxel
from pymunk import Body, Circle, Vec2d
from constants import HEIGHT


class Ninja:
    BALL_RADIUS = 8
    IMAGE_SIZE = BALL_RADIUS * 2
    SPEED = 20
    VISION_DISTANCE = 100

    def __init__(self):
        body = Body(50, 1)
        shape = Circle(body, self.BALL_RADIUS)
        shape.friction = 0.5

        self.body = body
        self.shape = shape

    def enter_space(self, space):
        space.add(self.body, self.shape)
        self.body.position = (140, HEIGHT - 10)

    def draw(self, shift):
        shape = self.shape

        bb = shape.bb
        x, y, _, _ = bb

        position = Vec2d(x, y) - shift

        image_page_index = 0
        image_position = (0, 0)

        vx, _ = self.body.velocity
        orientation = -1 if vx >= 0 else 1

        image_width = orientation * self.IMAGE_SIZE
        image_height = self.IMAGE_SIZE

        transparent_color = pyxel.COLOR_YELLOW

        pyxel.blt(
            *position,
            image_page_index,
            *image_position,
            -image_width,
            image_height,
            transparent_color
        )

    def update(self, player_position):
        vx, vy = self.body.velocity
        self_position = self.body.position
        player_distance = self_position - player_position

        if self.can_see_player(player_distance):
            x, y = player_distance

            if x >= 0:
                tx = vx - self.SPEED
                self.body.velocity = (max(tx, -self.SPEED), vy)
            else:
                t_x = vx + self.SPEED
                self.body.velocity = (min(self.SPEED, t_x), vy)
        else:
            self.body.velocity = (0, vy)

    def can_see_player(self, distance):
        dx, _ = distance
        return abs(dx) <= self.VISION_DISTANCE
