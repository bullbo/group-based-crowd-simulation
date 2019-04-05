import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from random import random, seed
import csv
from Utilities import random_circle, normalize
from SFModel import SF_Model
import numpy as np
from tqdm import tqdm
import time

plt.figure(figsize=(11,5))

#plt.figure(figsize=(5,5))

plt.style.use("ggplot")
cmap = matplotlib.cm.get_cmap('brg')

# Dark color maps gist_stern, brg, 

FRAMES = 250
dt = 0.1
AGENT_RADIUS = 0.15



N_GROUPS = 10
RADIUS = 12
SCALE = 1.5

velocity_vector = []
density_vector = []

data = np.array([0,0])

for h in tqdm(range(50)):
    sim = SF_Model()

    for _ in range(N_GROUPS):
        circle = random_circle(RADIUS, SCALE)
        position = circle[0]
        destination = circle[1]
        sim.add_group(np.random.randint(2,5), position, destination, cmap(random()))
        #sim.add_group(g[i], position, destination, cmap(random()))

    for i in tqdm(range(FRAMES)):
        sim.step(dt)
        v = 0
        density = len(sim.get_agents())/(sim.radius()**2)

        for agent in sim.get_agents():
            v+= np.linalg.norm(agent.velocity)/len(sim.get_agents())

        if i>60:
            if not np.all(np.isclose(agent.position, agent.destination, atol=((len(agent.group.agents)+2)*AGENT_RADIUS))):
                plt.scatter(density, v,color="midnightblue", s=5, marker="x")


                data = np.vstack([data, np.array([density, v])])
                #print(data)
                #velocity_vector.append(v)
                #density_vector.append(density)
 
np.save("data", data)




plt.xlabel(r"Density $1/m^{2}$")
plt.ylabel(r"Average velocity $m/s$")
plt.title("Fundamental diagram")
plt.ylim(0, 1.4)
plt.xlim(0, 6)
plt.show()

