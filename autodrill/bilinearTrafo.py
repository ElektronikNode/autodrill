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

import numpy


# Bilinear transformation for 2D points:
#	x_t = kxx * x + kxy * y + x0 + kxm * x * y
#	y_t = kyx * x + kyy * y + y0 + kym * x * y
#
# Assign by 3 or 4 pairs of corresponding points (points and points_t)

class bilinearTrafo(object):
	def __init__(self, points, points_t):

		self.n=len(points)
		assert(self.n==3 or self.n==4)		# transformation is only valid for 3 or 4 points

		# convert to numpy data types
		P=numpy.matrix(list(points))
		x=P[:,0]
		y=P[:,1]

		P_t=numpy.matrix(list(points_t))
		x_t=P_t[:,0]
		y_t=P_t[:,1]


		# equation systems:
		# x_t = M * kx
		# and:
		# y_t = M * ky

		M=numpy.concatenate((x, y, numpy.ones((self.n, 1))), axis=1)	# create matrix

		if self.n==4:
			M=numpy.concatenate((M, numpy.multiply(x, y)), axis=1)

		#print(M)

		# solve linear equation system
		self.kx = numpy.linalg.solve(M, x_t)
		self.ky = numpy.linalg.solve(M, y_t)


	# apply transformation on points
	def transform(self, points):

		points_t=list()

		for p in points:
			x = p[0]
			y = p[1]
			x_t = self.kx[0]*x + self.kx[1]*y + self.kx[2]
			y_t = self.ky[0]*x + self.ky[1]*y + self.ky[2]

			if self.n==4:
				x_t += self.kx[3]*x*y
				y_t += self.ky[3]*x*y

			points_t.append((float(x_t), float(y_t)))

		return points_t
