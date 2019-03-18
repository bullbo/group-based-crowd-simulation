import numpy as np
from random import randint
from Constants import AGENT_RADIUS
import math
from Agent import Agent
from Utilities import *

class Group():

    def __init__(self, n_agents, position, destination, color):
        self.id = 0
        self.agents = []
        self.position = position
        self.destination = destination
        self.color = color
        self.threshold_radius = (n_agents - 1)/1.5

        n = 1  # The n:th layer around the initial point.

        x_origin = position[0]
        y_origin = position[1]

        first_agent = Agent(np.array([x_origin, y_origin]), destination, color, self)
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

            agent = Agent(np.array([x_temp, y_temp]), destination, color, self)
            agent.group_id = self.id
            self.add_agent(agent)

    def get_agents(self):
        return self.agents
    
    def get_id(self):
        return self.id
    
    def add_agent(self, agent):
        """Adds an angent to the Crowd."""
        agent.group = self
        self.agents.append(agent)
    

    def center_mass(self):
        cmass = 0
        for agent in self.agents:
            cmass += agent.position/len(self.agents)
        return cmass

    def direction(self):
        direction = np.array([0, 0])
        for agent in self.agents:
            direction += agent.direction
        return normalize(direction)

    def velocity(self):
        group_velocity = 0
        for agent in self.agents:
            group_velocity += agent.velocity/len(self.agents)
        return group_velocity

    def radius(self):
        furthest_distance = 0
        for agent in self.agents:
            if np.linalg.norm(agent.position-self.center_mass()) > furthest_distance:
                furthest_distance = np.linalg.norm(
                    agent.position-self.center_mass())

        return furthest_distance+AGENT_RADIUS

    # def calc_group_repulsion(self, agent):
    #     """Works well except when group radius becomes too big,
    #     make sure that individual agents dont wander too far from
    #     the central mass """
    #     rij = agent.radius + self.radius()
    #     dist =agent.position - self.center_mass()
    #     dist_n = np.linalg.norm(dist)
    #     ev = np.array([0, agent.direction[1]])
    #     angle = calc_angle(dist, ev)
    #     d = dist_n * np.cos(angle)

    #     S = 1- d/rij
    #     if S <= 0:
    #         S = 0

    #     force = -GROUP_FORCE*math.exp((rij-dist_n)/GROUP_SIGMA)*S*ev
    #     return force

    

    
        
