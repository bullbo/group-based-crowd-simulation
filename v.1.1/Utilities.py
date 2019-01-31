import numpy as np
import random
import math
from Constants import *


def normalize(v):
    """ Returns the normalized vector v."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def random_circle(input_radius, scale):
    """ Returns two points on separate sides of a dounut. """
    theta = random.random()*2*(math.pi)

    radius_start = random.uniform(input_radius, input_radius*scale)
    radius_end = random.uniform(input_radius, input_radius*scale)

    start_position = np.array(
        [radius_start*math.cos(theta), radius_start*math.sin(theta)])
    end_position = np.array(
        [radius_end*math.cos(theta+math.pi), radius_end*math.sin(theta+math.pi)])

    return [start_position, end_position]


def calc_b(relative_distance, relative_velocity, dt):
    """ Returns value for b, from Dirk Helbing paper.  """

    norm_relative_distance = np.linalg.norm(relative_distance)
    norm_relative_velocity = np.linalg.norm(relative_velocity)

    temp_1 = (norm_relative_distance +
              np.linalg.norm(relative_distance-relative_velocity*dt))
    temp_2 = (dt*norm_relative_velocity)

    return 0.5*np.sqrt(temp_1**2-temp_2**2)


def calc_weight(l, angle):
    """ Returns the weights for the social force based on the agents field of vision."""
    return l + 0.5*(1-l)*(1-np.cos(angle))


def calc_angle(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'."""
    cosang = np.dot(v1, v2)
    sinang = np.linalg.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)
