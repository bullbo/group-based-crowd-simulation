import numpy as np
from random import randint
from Constants import AGENT_RADIUS, AGENT_VELOCITY


class Agent():
    """Represents a single agent and his/her properties. """
    def __init__(self, position, destination, color):
        self.id = 0
        self.radius = AGENT_RADIUS
        self.desired_velocity = AGENT_VELOCITY
        self.direction = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.position = position
        self.destination = destination
        self.color = color
        self.x_trail = [self.position[0]]
        self.y_trail = [self.position[1]]
        self.group_id = -1
