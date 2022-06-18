import random
import cv2 as cv
import copy
from typing import Tuple
import math

from confetti.particle_object.particle import Particle

img = cv.imread('../images/blank_back.jpg')
img_copy = copy.deepcopy(img)

height, width, _ = img.shape

emit_pos_t = (round(width / 2), 0)
emit_pos_r = (width, round(height / 2))
emit_pos_b = (round(width / 2), height)
emit_pos_l = (0, round(height / 2))


def init_particles(num: int) -> None:
    for i in range(num):
        r_blue = random.randint(0, 255)
        r_green = random.randint(0, 255)
        r_red = random.randint(0, 255)
        r_radius = random.randint(2, 10)

        if i < 30:
            end = rand_end_pos(emit_pos_t[0], emit_pos_t[1])
            curr_part = Particle(emit_pos_t, r_radius, (r_blue, r_green, r_red), end, 10.0)
        elif i < 60:
            end = rand_end_pos(emit_pos_r[0], emit_pos_r[1])
            curr_part = Particle(emit_pos_r, r_radius, (r_blue, r_green, r_red), end, 10.0)
        elif i < 90:
            end = rand_end_pos(emit_pos_b[0], emit_pos_b[1])
            curr_part = Particle(emit_pos_b, r_radius, (r_blue, r_green, r_red), end, 10.0)
        else:
            end = rand_end_pos(emit_pos_l[0], emit_pos_l[1])
            curr_part = Particle(emit_pos_l, r_radius, (r_blue, r_green, r_red), end, 10.0)

        particles.append(curr_part)


def start_anim() -> None:
    global img

    img = copy.deepcopy(img_copy)
    part_max_deviation = 10000

    for particle in particles:
        if not particle.at_end and part_max_deviation >= particle.x >= -part_max_deviation:
            particle.x += round(math.cos(launch_angle(particle.start, particle.end)) * particle.launch_velocity(10.0))
            particle.y += round(math.sin(launch_angle(particle.start, particle.end)) * particle.launch_velocity(10.0))
            cv.circle(img, (particle.x, particle.y), particle.radius, particle.color, -1)
            # cv.rectangle(img, (particle.x, particle.y), (particle.x + 8, particle.y + 20), particle.color, -1)


def reset_anim() -> None:
    for particle in particles:
        particle.x = particle.start[0]
        particle.y = particle.start[1]
        particle.end = rand_end_pos(particle.x, particle.y)
        particle.at_end = False


def rand_end_pos(x: int, y: int) -> Tuple:
    x_bounds = [-x, width - x]
    y_bounds = [-y, height - y]

    return x + random.randint(x_bounds[0], x_bounds[1]), \
           y + random.randint(y_bounds[0], y_bounds[1])


def launch_angle(start_pos: Tuple, rand_end: Tuple) -> float:
    return math.atan2(rand_end[1] - start_pos[1], rand_end[0] - start_pos[0])


title = 'Confetti Demo'
particles = []

cv.namedWindow(title, cv.WINDOW_GUI_NORMAL)
cv.imshow(title, img)

init_particles(120)

while True:
    cv.imshow(title, img)
    start_anim()
    key = cv.waitKey(10)

    if (key == ord('r')):
        reset_anim()

    if (key == ord('q')):
        cv.destroyAllWindows()
        break
