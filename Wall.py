import numpy as np
from random import randint
from Constants import *
from Utilities import *


class Wall():
    """Represents a single wall. """

    def __init__(self, x0, y0, x1, y1):
        self.id = 0
        self.start_position = [x0, y0]
        self.end_position = [x1, y1]
        self.x = []
        self.y = []
        self.points = []

        if (x1-x0) != 0:
            m = (y1-y0)/(x1-x0)
            c = m*x0 - y0

            x = np.arange(min(x0, x1), max(x0, x1), WALL_STEP)
            y = c + m*x
        else:
            n = int(abs(y1-y0)/WALL_STEP)
            x = [x0 for _ in range(n)]
            y = np.linspace(min(y0, y1), max(y0, y1), num=n)

        out = []
        for i in range(len(x)):
            out.append([x[i], y[i]])

        self.x = x
        self.y = y
        self.points = out

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_points(self):
        return self.points

    def get_start(self):
        return self.start_position

    def get_end(self):
        return self.end_position

    def get_id(self):
        return self.id

    def calc_wall_repulsion(self, agent):
        """ Returns the total Repulsion Force from objects that affects each agent. 
        The physical force is weighted since forces typically apply only when the object
        is faced infrot of the agent.
        """
        object_force = 0

        distance_to_closest_wall = agent.position-self.start_position

        for point in self.get_points():
            temp = agent.position - point

            if np.linalg.norm(temp) < np.linalg.norm(distance_to_closest_wall):
                distance_to_closest_wall = temp

        angle = calc_angle(
            agent.position-distance_to_closest_wall, agent.direction)
        weight = calc_weight(LAMBDA_ISOTROPY, angle)

        object_force = weight*F_OBSTACLE*np.exp(-1*np.linalg.norm(
            distance_to_closest_wall/SIGMA_OBSTACLE))*normalize(distance_to_closest_wall)

        return object_force
