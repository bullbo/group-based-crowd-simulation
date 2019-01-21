import numpy as np
from random import randint
from Constants import AGENT_RADIUS
import math
from Agent import Agent


class Group():

    def __init__(self, n_agents, position, destination, color):
        self.id = 0
        self.agents = []
        self.position = position
        self.destination = destination
        self.color = color


        n = 1  # The n:th layer around the initial point.

        x_origin = position[0]
        y_origin = position[1]

        first_agent = Agent(np.array([x_origin, y_origin]), destination, color)
        first_agent.group_id = self.id
        self.add_agent(first_agent)

        theta = 0.0
        d = 3*AGENT_RADIUS

        for _ in range(n_agents-1):
            theta += (60*math.pi/180.0)/n

            if theta < 2*math.pi:
                x_temp = x_origin + d*math.cos(theta)
                y_temp = y_origin + d*math.sin(theta)

            else:
                n += 1
                if n % 2 == 0:
                    theta = 0
                else:
                    theta = (60*math.pi/180.0)/n
                d += 3*AGENT_RADIUS
                x_temp = x_origin + d*math.cos(theta)
                y_temp = y_origin + d*math.sin(theta)

            agent = Agent(np.array([x_temp, y_temp]), destination, color)
            agent.group_id = self.id
            self.add_agent(agent)

    def get_agents(self):
        return self.agents
    
    def get_id(self):
        return self.id
    
    def add_agent(self, agent):
        """Adds an angent to the Crowd."""
        self.agents.append(agent)
    
