import pyxel
from pymunk import Body, Circle, Vec2d


class Ninja:
    BALL_RADIUS = 8
    IMAGE_SIZE = BALL_RADIUS * 2

    def __init__(self):
        body = Body(1, 1)
        shape = Circle(body, self.BALL_RADIUS)

        self.body = body
        self.shape = shape

    def enter_space(self, space):
        space.add(self.body, self.shape)
        self.body.position = (140, 40)

    def draw(self, shift):
        shape = self.shape

        bb = shape.bb
        x, y, _, _ = bb

        position = Vec2d(x, y) - shift

        image_page_index = 0
        image_position = (0, 0)

        image_width = self.IMAGE_SIZE
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

    def update(self):
        pass
