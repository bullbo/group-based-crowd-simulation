from Utilities import *
from Constants import *
from Group import Group
from Agent import Agent
from Wall import Wall

import math
import numpy as np
import csv




class Simulation:
    """A Simulation consists of multiple Agents, and walls."""

    def __init__(self):
        self.agents = []
        self.walls = []
        self.groups = []
        self.amount_agents = 0
        self.amount_walls = 0
        self.amount_groups = 0

    def add_agent(self, position, destination, color):
        """Adds an angent to the Simulation."""
        agent = Agent(position, destination, color)
        agent.id = self.amount_agents
        self.agents.append(agent)
        self.amount_agents += 1

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

    def calc_goal_force(self, agent):
        """ Returns the Goal Force. """
        return (agent.desired_velocity*agent.direction-agent.velocity)/TAU

    def calc_agent_repulsion(self, agent, neighbor):
        """ Returns the total Repulsion Force (Social Force + Physical Force) 
        that affects each agent as a result of it's other neighbours. 
        The social force is weighted since forces behind a person typically don't affect the person.  

        Agents within the same group experience less repelling force between each other. 
        """

        relative_distance = agent.position-neighbor.position
        norm_relative_distance = np.linalg.norm(relative_distance)
        relative_velocity = agent.velocity-neighbor.velocity
        diff_position = relative_distance-relative_velocity*T_S
        b = calc_b(relative_distance, relative_velocity, T_S)
        R = agent.radius + neighbor.radius

        # Social Forces
        social_force = F_SOCIAL*np.exp(-b/SIGMA_SOCIAL)*((relative_distance + np.linalg.norm(
            diff_position))/4*b)*(normalize(relative_distance) + normalize(diff_position))

        # Physical Forces
        physical_force = F_PHYSICAL * \
            np.exp((2*R-norm_relative_distance)/SIGMA_PHYSICAL) * \
            normalize(relative_distance)

        # Weigting the Social Forces
        angle = calc_angle(agent.position, agent.direction)
        weight = calc_weight(LAMBDA_ISOTROPY, angle)

        # If the neighbour is part of the group, the repelling force isn't as strong.
        social_factor, physical_factor = 1, 1
        if agent.group_id != -1 and agent.group_id == neighbor.group_id:
            social_factor = GROUP_S_FACTOR
            physical_factor = GROUP_P_FACTOR

        return (weight*social_force*social_factor+physical_force*physical_factor)

    def calc_wall_repulsion(self, agent):
        """ Returns the total Repulsion Force from objects that affects each agent. 
        The physical force is weighted since forces typically apply only when the object
        is faced infrot of the agent.
        """

        distance_to_closest_wall = agent.position-self.walls[0].get_points()[0]

        for wall in self.walls:
            for point in wall.get_points():
                temp = agent.position - point

                if np.linalg.norm(temp) < np.linalg.norm(distance_to_closest_wall):
                    distance_to_closest_wall = temp

        angle = calc_angle(
            agent.position-distance_to_closest_wall, agent.direction)
        weight = calc_weight(LAMBDA_ISOTROPY, angle)

        object_force = weight*F_OBSTACLE*np.exp(-1*np.linalg.norm(
            distance_to_closest_wall/SIGMA_OBSTACLE))*normalize(distance_to_closest_wall)

        return object_force

    def step(self, dt):
        """Moves every agent in the crowd one step ahead in time."""

        for agent in self.agents:
            initial_velocity = agent.velocity
            intial_position = agent.position
            agent.direction = normalize(agent.destination - agent.position)

            goal_force = self.calc_goal_force(agent)

            agent_repulsion = 0
            wall_repulsion = 0

            for neighbor in self.agents:
                if agent.id == neighbor.id:
                    continue
                agent_repulsion += self.calc_agent_repulsion(agent, neighbor)

            wall_repulsion += self.calc_wall_repulsion(agent)

            acceleration = goal_force+agent_repulsion+wall_repulsion

            # Checks if the estimated velocity surpasses the desired velocity
            estimated_velocity = initial_velocity + acceleration*dt
            norm_ev = np.linalg.norm(estimated_velocity)

            if np.abs(norm_ev) > AGENT_VELOCITY:
                agent.velocity = normalize(estimated_velocity)*AGENT_VELOCITY
            else:
                agent.velocity = estimated_velocity


            # Stop the agent if the destination is reached
            if np.all(np.isclose(agent.position, agent.destination, rtol=0.1)):
                agent.velocity = 0
                acceleration = 0

            # Updates the agents position
            agent.position = intial_position+initial_velocity*dt+0.5*acceleration*dt**2

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
