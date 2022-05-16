from typing import Tuple

class Circle:
    def __init__(self, x, y, color, radius):
        self.pos = (x, y)
        self.x_boundary = (x - radius, x + radius)
        self.y_boundary = (y - radius, y + radius)
        self.color = color
        self.radius = radius

    # Boundaries need to be recalculated when circle is moved
    def recalc_boundary(self) -> None:
        self.x_boundary = (
            self.pos[0] - self.radius, self.pos[0] + self.radius
        )
        self.y_boundary = (
            self.pos[1] - self.radius, self.pos[1] + self.radius
        )
