import numpy as np
from random import randint
from Constants import AGENT_RADIUS, AGENT_VELOCITY, TAU
from Utilities import *

class Agent():
    """Represents a single agent and his/her properties. """
    def __init__(self, position, destination, color, group):
        self.id = 0
        self.group = group
        self.radius = AGENT_RADIUS
        self.desired_velocity = AGENT_VELOCITY
        self.direction = normalize(destination - position)
        self.velocity = np.array([0.0, 0.0])
        self.position = position
        self.destination = destination
        self.color = color
        self.x_trail = [self.position[0]]
        self.y_trail = [self.position[1]]
        self.group_id = -1

    def calc_goal_force(self):
        """ Returns the Goal Force. """
        preferred_direction = normalize(self.destination - self.position)
        goal_force = (self.desired_velocity*preferred_direction-self.velocity)/TAU
        return goal_force

    def calc_agent_repulsion(self, neighbor):
        """ Returns the total Repulsion Force (Social Force + Physical Force) 
        that affects each agent as a result of it's other neighbours. 
        The social force is weighted since forces behind a person typically don't affect the person.  

        Agents within the same group experience less repelling force between each other. 
        """
        relative_distance = self.position-neighbor.position
        norm_relative_distance = np.linalg.norm(relative_distance)
        relative_velocity = self.velocity-neighbor.velocity
        diff_position = relative_distance-relative_velocity*T_S
        b = calc_b(relative_distance, relative_velocity, T_S)
        preferred_direction = normalize(self.destination - self.position)
        # Social Forces
        social_force = F_SOCIAL*np.exp(-b/SIGMA_SOCIAL)*((relative_distance + np.linalg.norm(
            diff_position))/4*b)*(normalize(relative_distance) + normalize(diff_position))


        # Physical Forces
        physical_force = F_PHYSICAL * \
            np.exp((2*self.radius-norm_relative_distance)/SIGMA_PHYSICAL) * \
            normalize(relative_distance)


        # Weigting the Social Forces
        angle = calc_angle(preferred_direction, relative_distance)
        weight = calc_weight(LAMBDA_ISOTROPY, angle)

        # If the neighbour is part of the group, the repelling force isn't as strong.
        social_factor, physical_factor = 1, 1
        if self.group_id != -1 and self.group_id == neighbor.group_id:
            social_factor = GROUP_S_FACTOR
            physical_factor = GROUP_P_FACTOR

        return (weight*social_force*social_factor+physical_force*physical_factor)
    
    def calc_group_attraction_force(self):

        distance_to_center = self.group.center_mass() - self.position
        q = np.linalg.norm(distance_to_center)/self.group.threshold_radius
        F = F_G_ATTRACTION*q*normalize(distance_to_center)        

        return F