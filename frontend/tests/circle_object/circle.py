from typing import Tuple


class Circle:
    def __init__(self, x, y, color, radius, focus):
        self.pos = (x, y)
        self.x_boundary = (x - radius, x + radius)
        self.y_boundary = (y - radius, y + radius)
        self.color = color
        self.radius = radius
        self.focus = focus
        self.dir_vect = self.recalc_dir_vect((x, y), focus)

    # Boundaries need to be recalculated when circle is moving
    def recalc_boundary(self) -> None:
        self.x_boundary = (
            self.pos[0] - self.radius, self.pos[0] + self.radius
        )
        self.y_boundary = (
            self.pos[1] - self.radius, self.pos[1] + self.radius
        )

    # Direction vector needs to be recalculated when circle is moving
    def recalc_dir_vect(self, circle_point: Tuple, focus_point: Tuple) -> None:
        self.dir_vect = (focus_point[0] - circle_point[0], focus_point[1] - circle_point[1])
