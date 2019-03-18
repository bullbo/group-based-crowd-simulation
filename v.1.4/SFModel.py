from Utilities import *
from Constants import *
from Group import Group
from Agent import Agent
from Wall import Wall

import math
import numpy as np
import csv


class SF_Model:
    """A Simulation consists of multiple Agents, and walls."""

    def __init__(self):
        self.agents = []
        self.walls = []
        self.groups = []
        self.amount_agents = 0
        self.amount_walls = 0
        self.amount_groups = 0

    def add_wall(self, x0, y0, x1, y1):
        """Adds a wall to the Simulation."""
        wall = Wall(x0, y0, x1, y1)
        wall.id = self.amount_walls
        self.walls.append(wall)
        self.amount_walls += 1

    def import_agent(self, agent):
        """Imports an angent to the Simulation from a group."""
        agent.id = self.amount_agents
        self.agents.append(agent)
        self.amount_agents += 1

    def add_group(self, n_agents, position, destination, color):
        """Adds a group of agents to the Simulation."""
        group = Group(n_agents, position, destination, color)
        group.id = self.amount_groups
        self.groups.append(group)

        for agent in group.get_agents():
            self.import_agent(agent)
        self.amount_groups += 1

    def get_agents(self):
        """ Returns an array with all the agents in the crowd."""
        return self.agents

    def get_walls(self):
        """ Returns an all walls in the simulations. """
        return self.walls

    def get_groups(self):
        return self.groups

    def step(self, dt):
        """Moves every agent in the crowd one step ahead in time."""

        for agent in self.agents:

            initial_velocity = agent.velocity
            intial_position = agent.position

            agent_repulsion = 0
            group_attraction_force = 0
            #wall_repulsion = 0

            goal_force = agent.calc_goal_force()
            group_attraction_force += agent.calc_group_attraction_force()

            for neighbor in self.agents:
                agent_repulsion += agent.calc_agent_repulsion(neighbor)

            # for wall in self.get_walls():
            #     wall_repulsion += wall.calc_wall_repulsion(agent)

            acceleration = goal_force+agent_repulsion+group_attraction_force

            # Checks if the estimated velocity surpasses the desired velocity
            estimated_velocity = initial_velocity + acceleration*dt
            norm_ev = np.linalg.norm(estimated_velocity)

            if np.abs(norm_ev) > AGENT_VELOCITY:
                agent.velocity = normalize(estimated_velocity)*AGENT_VELOCITY
            else:
                agent.velocity = estimated_velocity


            # Stop the agent if the destination is reached
            if np.all(np.isclose(agent.position, agent.destination, atol=((len(agent.group.agents)-2)*AGENT_RADIUS))): #0.1 rtol is standard
                agent.velocity = 0
                acceleration = 0

            # Updates the agents position
            agent.position = intial_position+agent.velocity*dt

            #agent.direction = normalize(agent.destination - agent.position)
            agent.direction = normalize(agent.velocity)
            if type(normalize(agent.velocity)) == int:
                agent.direction = [0, 0]


            # Records the agents trail
            agent.x_trail.append(agent.position[0])
            agent.y_trail.append(agent.position[1])



    def write_to_CSV(self, frames, dt):
        """ Writes the whole simulation into two csv files containing the 
        agents trails and the wall positions. These files can be used in the 
        Unity Crowd Visualizer."""

        with open('simualtion.csv', mode='w') as simulation_file:
            simulation_writer = csv.writer(
                simulation_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            simulation_writer.writerow(['TIME ', 'ID ', 'POS_X ', 'POS_Y ', 'TAR_X ',
                                        'TAR_Y ', 'AGENT_RADIUS ', 'COLOR_R ', 'COLOR_G ', 'COLOR_B '])

            sim_time = 0
            for i in range(frames):
                for agent in self.get_agents():
                    simulation_writer.writerow([sim_time, agent.id, round(agent.x_trail[i], 5), round(agent.y_trail[i], 5),
                                                agent.destination[0], agent.destination[1], agent.radius, agent.color[0], agent.color[1], agent.color[2]])
                sim_time += dt

        with open('walls.csv', mode='w') as simulation_file:
            simulation_writer = csv.writer(
                simulation_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            simulation_writer.writerow(
                ['ID ', 'P1_X ', 'P1_Y ', 'P2_X ', 'P2_Y '])

            for wall in self.get_walls():
                simulation_writer.writerow([wall.get_id(), wall.get_x()[0], wall.get_y()[
                                           0], wall.get_x()[-1], wall.get_y()[-1]])
