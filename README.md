![header](https://i.imgur.com/7E258Dd.png)
# Simulation of Groups within Crowds using Social Forces
This algorithm is a part of a bachelor thesis in engineering physics at KTH Royal Institute of Technology 2019. 

Crowd simulations are useful in a variety of fields including entertain-
ment, robotics and evacuation planning. 
The social force model (SFM) uses a microscopic approach and simulates interactions between single
agents to include group behaviour new group related attraction force that adds cohesiveness within groups
is introduced. 

<p align="center">
  <img src="https://media.giphy.com/media/JOQdlnLTC9lurYSPiz/giphy.gif">
</p>

## Running simulations
Inintialize a simulation by declaring the following
```
sim = SF_Model()
```
To add an agent or a group of agents, call `add_group()` on `sim`.
```
sim.add_group(int nAgents, ndarray startPosition, ndarray endPosition, string color)
```
Each group has a corrisponding color and a starting/ending point in the form of a 
2D array `[x_0, y_0]`.
To add a wall to the simulation, call `add_wall()` on `sim`.
```
sim.add_group(float x0, float y0, float x1, float y1)
```
Where `[x_0, y_0]` is the starting point of the wall, and `[x_1, y_1]` the ending point. 

To run the simulation execute `sim.step(float dt)` over the amount of desired frames.
Here `dt` is the timestep, a recommended value is `0.1`.

## Extract to CSV
The whole simulation can be extracted to two CSV files. This is done by call `write_to_CSV()` on `sim`
after the simulation is completed. 
```	
sim.write_to_csv(int FRAMES)
```
Two CSV files will be created in the file directory,  `walls.csv` will have a header structure of
`ID, P1_X, P1_Y, P2_X, P2_Y`, `simulation.csv` will have a header structure of 
`TIME ,ID ,POS_X ,POS_Y, TAR_X, TAR_Y, AGENT_RADIUS, COLOR_R, COLOR_G, COLOR_B`.
These CSV files can be used to vizualize the simulation in 3D using Unity-Crowd-Visualizer
found here; https://github.com/hsaikia/Unity-Crowd-Visualizer .

<p align="center">
  <img width=400 height=200 src="https://i.imgur.com/NpCYxgR.gif">
</p>

## Dependencies

The algorithm has a dependency available for Windows, Linux and OSX.
The dependency include:
  - Numpy

This can be acquired via Anaconda or with  `pip ` using the following command:

  `pip install numpy`


   
## Attribution

- 
-
-


If you use the model as part of an academic publication, we request that you cite the model as follows:

```
  @article{SFMG,
	author = {Amin Bolakhrif, Julia Li},
	title = {Simulation of Groups within Crowds using Social Forces},
	year = {2019},
	keywords = {crowd simulation; pedestrians; open source; groups; social force model},
	url = {x}
  }
```
