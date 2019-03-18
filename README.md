# CrowdSim-SocialForces
Using social forces for crowd simulations in a physics engineering degree project at KTH.

For now, run '''SimDisplay.py''' to test out.
Using numpy in python for the calculations we could plot the walls, agents and their trails with matplotlib.

## 6 Groups with 22 Agents in total
![](/images/22A_6G.gif)
## 8 Groups with 36 Agents in total
![](/images/29A_8G.gif)
## 10 Groups with 36 Agents in total
![](/images/36A_10G.gif)
## 20 Groups with 71 Agents in total
![](/images/71A_20G.gif)
## 50 Groups with 166 Agents in total
![](/images/166A_50G.gif)




The data could be imported to Unity, and be animated in 3D.
![](/images/unitygif.gif)
## TODO
* Analyze the weight coefficients that is used for the obstacle and social forces.
* Rename all variables to something shorter and descriptive.
* Optimize all calculation methods, some of them are O(n^2).
