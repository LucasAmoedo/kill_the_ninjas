import pyxel
from pymunk import Segment, BB
from pymunk.autogeometry import march_hard
from constants import WIDTH, HEIGHT


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

    def draw(self, shift):
        for segment in self.segments:
            x1, y1 = segment.a
            x2, _ = segment.b
            w = x2 - x1
            h = segment.radius
            c = pyxel.COLOR_RED
            pos = (x1, y1) - shift
            pyxel.rect(*pos, w, h, c)

        return True
