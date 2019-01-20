from helper import *
from Agent import *
import math
import numpy as np
from Constants import *
import csv


class Simulation:
    """A Crowd consists of multiple Agents, and different methods to manipulate them."""

    def __init__(self):
        self.agents = []
        self.walls = []
        self.amount_agents = 0
        self.amount_walls = 0

    def add_agent(self, agent):
        """Adds an angent to the Crowd."""
        agent.id = self.amount_agents
        self.agents.append(agent)
        self.amount_agents += 1

    def add_wall(self, wall):
        wall.id = self.amount_walls
        self.walls.append(wall)
        self.amount_walls += 1

    def add_group(self, n_agents, position, destination, color):
        """Adds a group to the Crowd. 
        To initialize the starting position, we let the agents spawn around the position
        on a certain angle theta and distance d, away from the wanted initial point.
        Essentialy we form a spiral around the initial point, with 6 agents covering the first
        agent, 12 agents on top of the 6 agents etc. 
        """

        n = 1  # The n:th layer around the initial point.

        x_origin = position[0]
        y_origin = position[1]

        self.add_agent(
            Agent(np.array([x_origin, y_origin]), destination, color))

        theta = 0.0
        d = 6*AGENT_RADIUS

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
                d += 6*AGENT_RADIUS
                x_temp = x_origin + d*math.cos(theta)
                y_temp = y_origin + d*math.sin(theta)

            self.add_agent(
                Agent(np.array([x_temp, y_temp]), destination, color))

    def get_agents(self):
        """ Returns an array with all the agents in the crowd."""
        return self.agents

    def get_walls(self):
        """ Returns an all walls in the simulations. """
        return self.walls

    def calc_goal_force(self, agent):
        """ Returns the Goal Force. 
        F_goal = (v_prefered - v_actual)/tau"""
        return (agent.desired_velocity*agent.direction-agent.velocity)/TAU

    def calc_agent_repulsion(self, agent, neighbor):
        """ Returns the total Repulsion Force (Social Force + Physical Force) 
        that affects each agent as a result of it's other neighbours. 
        The social force is weighted since forces behind a person typically don't affect the person.  
        """

        relative_distance = agent.position-neighbor.position
        norm_relative_distance = np.linalg.norm(relative_distance)
        relative_velocity = agent.velocity-neighbor.velocity
        diff_position = relative_distance-relative_velocity*T_S
        b = calc_b(relative_distance, relative_velocity, T_S)
        R = agent.radius + neighbor.radius

        # Social Forces
        social_1 = (relative_distance + np.linalg.norm(diff_position))/4*b
        social_2 = normalize(relative_distance) + normalize(diff_position)
        social_3 = F_SOCIAL*np.exp(-b/SIGMA_SOCIAL)
        social_force = social_1*social_2*social_3

        # Physical Forces
        physical_force = F_PHYSICAL * \
            np.exp((2*R-norm_relative_distance)/SIGMA_PHYSICAL) * \
            normalize(relative_distance)

        # Weigting the Social Forces
        angle = calc_angle(agent.position, agent.direction)
        weight = calc_weight(LAMBDA_ISOTROPY, angle)

        return weight*social_force+physical_force

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
            for i in range(FRAMES):
                for agent in self.get_agents():
                    simulation_writer.writerow([sim_time, agent.id, round(agent.x_trail[i], 5), round(agent.y_trail[i], 5),
                                                agent.destination[0], agent.destination[1], agent.radius, 1, 0, 0])
                sim_time += dt

        with open('walls.csv', mode='w') as simulation_file:
            simulation_writer = csv.writer(
                simulation_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            simulation_writer.writerow(
                ['ID ', 'P1_X ', 'P1_Y ', 'P2_X ', 'P2_Y '])

            for wall in self.get_walls():
                simulation_writer.writerow([wall.get_id(), wall.get_start()[0], wall.get_start()[
                                           1], wall.get_end()[0], wall.get_end()[1]])
