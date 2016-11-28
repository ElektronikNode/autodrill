'''
autodrill is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

autodrill is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with autodrill. If not, see < http://www.gnu.org/licenses/ >.

(C) 2014- by Friedrich Feichtinger, <fritz_feichtinger@aon.at>
'''

import math
from copy import copy

# find a (short) path through the set of points
def findPath(points):

	mypoints=copy(points)		# make local copy
	path=[mypoints.pop()]		# start with a random point


	while mypoints:

		# find the next point using nearest neighbour search

		base=path[-1]			# last path point is base point for NN search
		mindist=float("inf")	# minimal distance

		for p in mypoints:
			if distance(base, p) < mindist:
				mindist = distance(base, p)
				bestPoint = p

		path.append(bestPoint)		# append nearest point to path
		mypoints.remove(bestPoint)

	return path



# euclidian distance between 2 points
def distance(p1, p2):
	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
