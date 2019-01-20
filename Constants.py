
"""Simulation Constants"""
N_AGENTS = 7
RADIUS = 5
SCALE = 1.5
FRAMES = 300
# Look-Ahead Time
T_S = 1.27 
WALL_STEP = 0.1


"""Crowd Constants"""
AGENT_RADIUS = 0.25
AGENT_VELOCITY = 0.15

# Social Forces #

# Parameter describing the magnitude of the force social force.
F_SOCIAL = 0.015
# Parameter describing the range scale of the Social Force.
SIGMA_SOCIAL = 0.6  
# Describing time scale for the adaptation to the preferred velocity.
TAU = 0.6

# Physical Forces #

# Parameter describing the magnitude of the force physical force.
F_PHYSICAL = 0.2
# Parameter describing the range scale of the physical Force.
SIGMA_PHYSICAL = 0.2
# Model parameter, describing the strength of the isotropy.
LAMBDA_ISOTROPY = 0

# Obstacle Forces #

# Parameter describing the magnitude of the force obstacle force.
F_OBSTACLE = 2.3
# Parameter describing the range scale of the obstacle Force.
SIGMA_OBSTACLE = 0.2
