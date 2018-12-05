==========================
=====	Intro	==========
==========================
This is a rrt simulation. It uses the Polygon and Point class from shapely to do polygon collision detection. It takes txt input file and will generate rrt with animation.

==========================
======	packages	======
==========================

Necessary packages:
pyplot from matplotlib
shapely  

Installation:
pip install matplotlib
pip install shapely


==========================
======	How to run	======
==========================

"python rrt.py"

The script is set to run "input_rrt.txt" by default

to change to other input configuration, there are two places need to be modify:
1. line 217, change inputFile name
2. line 222, change window size, this is also the area where random point will be generated. [max,min]

Example:

1. line 217 change inputFile to "input_triangle.rrt"
2. line 222 change explore are to [-2,14]
