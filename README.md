# Simulation of Groups within Crowds using Social Forces
Crowd simulations are useful in a variety of fields including entertain-
ment, robotics and evacuation planning. 

The social force model (SFM) uses a microscopic approach and simulates interactions between single
agents to include group behaviour new group related attraction force that adds cohesiveness within groups
is introduced. This algorithm is a part of a bachelor thesis in engineering physics at KTH 2019. 

## Running simulations

## Extract to CSV

### Dependencies

The algorithm has a dependency available for Windows, Linux and OSX.
The dependency include:
  - Numpy

This can be acquired via Anaconda or with  `pip ` using the following command:

  `pip install numpy`


   
## Attribution

- Menge uses [www.sourceforge.net/projects/tinyxml](tinyxml) to parse XML.
- Menge makes use of an implementation of normal random distrubtions implemented by John Burkardt.
  See `src/MengeCore/Math/SimRandom.cpp` for details.
- Menge uses [http://tclap.sourceforge.net/](tclap) to handle command-line parsing.
- The GCF model (`src/Plugins/GCFAgent`) uses an algorithm for computing the distance of closest
  approach (DCA) between two ellipses from http://www.math.kent.edu/~zheng/ellipsoid.c.

If you use Menge as part of an academic publication, we request that you cite Menge as follows:

```
  @article{SFMG,
	author = {Amin Bolakhrif, Julia Li},
	title = {Simulation of Groups within Crowds using Social Forces},
	year = {2019},
	keywords = {crowd simulation; pedestrians; open source; groups; social force model},
	url = {x}
  }
```
