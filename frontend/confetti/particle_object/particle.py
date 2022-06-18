from typing import Tuple, Any
import math


def calc_point_dist(a: int, b: int) -> float:
    distance = math.sqrt(a ** 2 + b ** 2)

    return distance


def translate(value, l_min, l_max, r_min, r_max):
    # Figure out how 'wide' each range is
    l_span = l_max - l_min
    r_span = r_max - r_min

    # Convert the left range into a 0-1 range (float)
    val_scale = float(value - l_min) / float(l_span)

    # Convert the 0-1 range into a value in the right range.
    return r_min + (val_scale * r_span)


class Particle:
    def __init__(self, start: Tuple, radius: int, color: Any, end: Tuple, vel_val: float):
        self.start = start
        self.x = start[0]
        self.y = start[1]
        self.radius = radius
        self.color = color
        self.end = end
        self.at_end = False
        self.velocity = self.launch_velocity(vel_val)

    def launch_velocity(self, start_velo: float) -> float:
        dir_vect = (self.end[0] - self.x, self.end[1] - self.y)
        dir_vect_max = (self.end[0] - self.start[0], self.end[1] - self.start[1])

        distance = calc_point_dist(dir_vect[0], dir_vect[1])
        distance_max = calc_point_dist(dir_vect_max[0], dir_vect_max[1])

        if distance <= 35 and not self.at_end:
            self.at_end = True

        return translate(distance, 0, distance_max, start_velo * 0.3, 1 * start_velo)
