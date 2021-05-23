import pyxel
from pymunk import Space, Body, Circle, Vec2d, Segment, BB
from pymunk.autogeometry import march_hard


WIDTH = 256
HEIGHT = 200


class LayoutBuilder:
    def __init__(self):
        self.layout = [
            "       ",
            "       ",
            "     xx",
            "    x  ",
            "   x   ",
            "  x    ",
            "xxxxxxx"
        ]
        self.segment_radius = 1
        self.segments = []

    def __build_polyline_set(self):
        x_count = 0
        y_count = 0

        def analyze_samples(point):
            nonlocal y_count, x_count

            c = self.layout[y_count][x_count]

            x_count += 1

            if x_count >= x_samples_size:
                x_count = 0
                y_count += 1

            return 1 if c == "x" else 0

        left = 0
        bottom = 0
        right = WIDTH
        top = HEIGHT

        error_threshold = .5

        bounding_box = BB(left, bottom, right, top)

        y_samples_size = len(self.layout)
        x_samples_size = len(self.layout[0])

        pl_set = march_hard(
            bounding_box,
            x_samples_size,
            y_samples_size,
            error_threshold,
            analyze_samples
        )

        return pl_set

    def add_segments_to_space(self, space):
        pl_set = self.__build_polyline_set()
        bdy = space.static_body

        for pl in pl_set:
            for i, p in enumerate(pl[:-1]):
                a = p
                b = pl[i + 1]
                a = (int(round(a[0], 0)), int(round(a[1], 0)))
                b = (int(round(b[0], 0)), int(round(b[1], 0)))
                r = self.segment_radius
                s = Segment(bdy, a, b, r)

                space.add(s)
                self.segments.append(s)

        return True

    def draw(self):
        for segment in self.segments:
            x1, y1 = segment.a
            x2, _ = segment.b
            w = x2 - x1
            h = segment.radius
            c = pyxel.COLOR_RED
            pyxel.rect(x1, y1, w, h, c)

        return True


class Bullet:
    def __init__(self, body, shape, tick):
        self.body = body
        self.shape = shape
        self.tick = tick


class BallGun:
    RADIUS = 2
    POWER = 270
    BULLET_DURATION = 30

    def __init__(self):
        self.bullets = []

    def enter_space(self, space):
        self.space = space

    def fire(self, position, orientation):
        body = Body(body_type=Body.DYNAMIC)
        shape = Circle(body, self.RADIUS)

        shape.friction = 0.5
        shape.density = 0.1

        body.position = position

        self.space.add(body, shape)

        self.bullets.append(
            Bullet(body, shape, 0)
        )

        self.__apply_impulse(body, orientation)

    def __apply_impulse(self, body, orientation):
        impulse = Vec2d(-orientation, 0) * self.POWER

        body.apply_impulse_at_world_point(impulse, body.position)

    def update(self):
        for bullet in self.bullets.copy():
            bullet.tick += 1

            if bullet.tick >= self.BULLET_DURATION:
                self.space.remove(bullet.body, bullet.shape)
                self.bullets.remove(bullet)

    def draw(self, shift):
        for bullet in self.bullets:
            body = bullet.body
            shape = bullet.shape

            pos = body.position - shift

            pyxel.circ(
                *pos,
                shape.radius,
                pyxel.COLOR_RED
            )


class Player:
    BALL_RADIUS = 8
    SPEED = 50
    ORIENTATION_LEFT = 1
    ORIENTATION_RIGHT = -1
    IMAGE_SIZE = BALL_RADIUS * 2

    def __init__(self):
        ball = Body(1.0, 1.0)
        ball_shape = Circle(ball, self.BALL_RADIUS)
        ball.position = (0, HEIGHT - self.BALL_RADIUS)

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
        ball = self.body
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
        

class Game:
    FPS = 30
    GRAVITY = Vec2d(0, 50)
    GROUND_RADIUS = 3
    SCREEN = Vec2d(WIDTH, HEIGHT)

    def __init__(self):
        self.space = Space()
        self.space.gravity = self.GRAVITY
        # self.camera_pos = Vec2d(0, 0)

        # self.player = Player()
        # self.player.enter_space(self.space)

        x, y = WIDTH, HEIGHT

        self.layout_builder = LayoutBuilder()
        self.layout_builder.add_segments_to_space(self.space)

    def update(self):
        dt = 1 / self.FPS

        # self.player.update(self.camera_pos)

        # pos = self.player.position
        # self.camera_pos = Vec2d(pos[0], 20) - Vec2d(WIDTH / 2, 0)
        self.space.step(dt)

    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)

        self.layout_builder.draw()


        # shift = self.camera_pos
        # shift = (0, 0)

        # self.player.draw(shift)

        # for platform in self.platforms:
        #     bb = platform.bb
        #     p = Vec2d(bb.left, bb.bottom) - shift
        #     w = bb.right - bb.left
        #     h = self.GROUND_RADIUS

        #     pyxel.rect(*p, w, h, pyxel.COLOR_GREEN)

        # # Desenha o chão
        # platforms = self.platforms
        # for platform in platforms:
        #     bb = platform.bb
        #     p = Vec2d(bb.left, bb.bottom) - shift
        #     w = bb.right - bb.left
        #     h = self.GROUND_RADIUS
        #     pyxel.rect(*p, w, h, pyxel.COLOR_GREEN)
        # pyxel.rect(0, HEIGHT - 3, WIDTH, 3, pyxel.COLOR_GREEN)

    def run(self):
        pyxel.init(WIDTH, HEIGHT, fps=self.FPS)

        # pyxel.load("assets.pyxres")

        pyxel.run(self.update, self.draw)


game = Game()
game.run()
