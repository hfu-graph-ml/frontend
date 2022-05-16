import copy
from typing import Tuple

import cv2 as cv
import math

from frontend.tests.circle_object.circle import Circle

# Small lambda function that'll take care of
# checking whether or not a point x is
# within two boundaries.
within = lambda x, low, high: low <= x <= high

# Boolean that attests to whether or not the
# user is clicking on circle
selected = False

img = cv.imread('../images/blank_back.jpg')
img_copy = copy.deepcopy(img)


def click_frame(event, x, y, flags, param) -> None:
    global spawned_circles, selected, img, img_copy, focus_point, selected_circle

    if event == cv.EVENT_LBUTTONDOWN and len(spawned_circles) == 0:
        circle = draw_focus_point(x, y)
        spawned_circles[circle.pos] = circle
        focus_point += circle.pos

    elif event == cv.EVENT_LBUTTONDOWN and len(spawned_circles) > 0:
        circle = draw_default_point(x, y)
        spawned_circles[circle.pos] = circle

    elif event == cv.EVENT_RBUTTONDOWN:
        pos = (x, y)

        # If we click within a circle, mark as selected
        for key in spawned_circles:
            if (
                within(pos[0], *spawned_circles[key].x_boundary)
                and within(pos[1], *spawned_circles[key].y_boundary)
            ):
                selected = True
                selected_circle = spawned_circles[key]

    elif event == cv.EVENT_RBUTTONUP:
        selected = False

    if selected:
        print('drawing')
        # Clean image of old points in order to avoid
        # visual error
        img = copy.deepcopy(img_copy)
        selected_circle.pos = (x, y)
        selected_circle.recalc_boundary()

        # If the selected circle is the main circle,
        # set focus point to new main circle position
        if (
            within(focus_point[0], *selected_circle.x_boundary)
            and within(focus_point[1], *selected_circle.y_boundary)
        ):
            focus_point = selected_circle.pos

        for key in spawned_circles:
            cv.circle(img,
                      spawned_circles[key].pos,
                      spawned_circles[key].radius,
                      spawned_circles[key].color,
                      -1)

            if not spawned_circles[key].pos == focus_point:
                draw_vector(spawned_circles[key], recalc_scaling(spawned_circles[key]))

def draw_focus_point(x: int, y: int) -> Circle:
    circle = Circle(x, y, (0, 0, 255), 40)
    cv.circle(img, circle.pos, circle.radius, circle.color, -1)

    return circle

def draw_default_point(x: int, y: int) -> Circle:
    circle = Circle(x, y, (0, 255, 0), 25)
    cv.circle(img, circle.pos, circle.radius, circle.color, -1)
    draw_vector(circle, recalc_scaling(circle))

    return circle

def recalc_scaling(circle: Circle) -> int:
    direction_vect = calc_dir_vect(circle.pos, focus_point)
    distance = calc_point_dist(direction_vect[0], direction_vect[1])

    if distance >= 200:
        return 70
    elif 200 > distance > 50:
        return round(distance / 2.8428) # replace magic number with smart equation
    else:
        return 0

def draw_vector(circle: Circle, length_scale: int) -> None:
    direction_vect = calc_dir_vect(circle.pos, focus_point)
    vector = normalize(direction_vect)
    vector = (vector[0] * length_scale, vector[1] * length_scale) # Scale up vector size
    arrow_point = (round(circle.pos[0] + vector[0]), round(circle.pos[1] + vector[1]))
    cv.arrowedLine(img, circle.pos, arrow_point, (0, 0, 0), 2)

def calc_dir_vect(circle_point: Tuple, focus_point: Tuple) -> Tuple:
    dir_vect = (focus_point[0] - circle_point[0], focus_point[1] - circle_point[1])

    return dir_vect

def calc_point_dist(a: int, b: int) -> float:
    distance = math.sqrt(a ** 2 + b ** 2)

    return distance

def normalize(vector) -> Tuple:
    distance = calc_point_dist(vector[0], vector[1])
    normalized = (vector[0] / distance, vector[1] / distance)

    return normalized


title = 'Compass Demo'
spawned_circles = {}
focus_point = ()
selected_circle = None

cv.namedWindow(title, cv.WINDOW_GUI_NORMAL)
cv.setMouseCallback(title, click_frame)
cv.imshow(title, img)

while True:
    cv.imshow(title, img)
    key = cv.waitKey(10)

    if (key == ord('q')):
        cv.destroyAllWindows()
        break
