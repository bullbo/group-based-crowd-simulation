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
    return (l + (l-1)*(1-np.cos(angle))*0.5)


def calc_angle(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'."""
    return v1[0]*v2[1] - v1[1]*v2[0]


def rot_v(v1, theta):
    """ Rotates a vector v1 theta degrees, returns the new rotated vector. """
    theta = np.radians(theta)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, s], [-s, c]])
    return (R.dot(v1))


def angle2(v1, v2):
    """ Returns the signed angle in radians between two vectors v1, v2. """
    angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
    return angle


def check_vector_inbetween(v1, v2, point):
    """ Checks if point lies inbetween two vectors v1, v2. Returns boolean. """
    if (np.dot(np.cross(v1, point), np.cross(v1, v2))) >= 0 and (np.dot(np.cross(v2, point), np.cross(v2, v1))) >= 0:
        return True
    else:
        return False
