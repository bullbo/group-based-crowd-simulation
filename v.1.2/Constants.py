"""Crowd Constants"""
AGENT_RADIUS = 0.15
AGENT_VELOCITY = 0.15
# The distance between each point within a wall.
WALL_STEP = 0.1
# Scale of which an agent experiences social force from neighbours of the same group.
GROUP_S_FACTOR = 0.6
# Scale of which an agent experiences physical force from neighbours of the same group.
GROUP_P_FACTOR = 0.6
""""""""""""""""""""

""" Social Forces """
# Look-Ahead Time, the extent to which the affected walker extrapolates the relative position of the affecting walker.
T_S = 1.27
# Parameter describing the magnitude of the force social force.
F_SOCIAL = 0.015
# Parameter describing the range scale of the Social Force.
SIGMA_SOCIAL = 0.6
# Parameter describing time scale for the adaptation to the preferred velocity.
TAU = 0.6
""""""""""""""""""""

""" Physical Forces """
# Parameter describing the magnitude of the force physical force.
F_PHYSICAL = 0.2
# Parameter describing the range scale of the physical Force.
SIGMA_PHYSICAL = 0.2
# Model parameter, describing the strength of the isotropy.
LAMBDA_ISOTROPY = 0
""""""""""""""""""""

""" Obstacle Forces"""
# Parameter describing the magnitude of the force obstacle force.
F_OBSTACLE = 5.5
# Parameter describing the range scale of the obstacle Force.
SIGMA_OBSTACLE = 0.2
""""""""""""""""""""

