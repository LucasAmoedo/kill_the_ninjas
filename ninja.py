import pyxel
from pymunk import Body, Circle, Vec2d
from constants import HEIGHT


class Ninja:
    BALL_RADIUS = 8
    IMAGE_SIZE = BALL_RADIUS * 2
    SPEED = 30
    VISION_DISTANCE = 100

    def __init__(self):
        body = Body(50, 1)
        shape = Circle(body, self.BALL_RADIUS)
        shape.friction = 0.5
        shape.collision_type = 2

        body.reference = self

        self.body = body
        self.shape = shape

        self.hit_points = 3

    def enter_space(self, space):
        space.add(self.body, self.shape)
        self.body.position = (140, HEIGHT - 10)

        self.space = space

        return True

    def leave_space(self):
        self.space.remove(self.body, self.shape)
        self.space = None

        return True

    def draw(self, shift):
        if not self.space:
            return

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
        if self.hit_points == 0:
            if self.space:
                self.leave_space()

            return

        vx, vy = self.body.velocity
        self_position = self.body.position
        _, sy = self_position
        player_distance = self_position - player_position
        _, py = player_position

        if self.can_see_player(player_distance):
            x, y = player_distance

            if x >= 0:
                tx = vx - self.SPEED
                tx = max(tx, -self.SPEED)
                self.body.velocity = (tx, vy)
            else:
                t_x = vx + self.SPEED
                tx = min(self.SPEED, t_x)
                self.body.velocity = (tx, vy)

            if vy == 0.0 and abs(py-sy) >= 3:
                self.body.velocity = (tx, -2 * self.SPEED)

        else:
            self.body.velocity = (0, vy)

    def can_see_player(self, distance):
        dx, _ = distance
        return abs(dx) <= self.VISION_DISTANCE
