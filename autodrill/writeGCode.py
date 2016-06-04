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

from PyQt4.QtCore import QFile, QFileInfo, QIODevice

def writeGCode(dia, drillPath, originalFilename, feedrate, depth, spacing, toolChangePosition):

	fi=QFileInfo(originalFilename)
	filename=fi.absolutePath() + "/" + fi.completeBaseName() + str(dia) + ".ngc"
	#filename = str(filename.toUtf8())
	file=QFile(filename)
	
	file.open(QIODevice.WriteOnly)


	# initial G-codes
	file.write("G90\n")									# set to absolut positioning
	#file.write("G21\n")								# use millimeters
	file.write("F{:f}\n".format(feedrate*60))			# set feedrate (mm/min)


	x, y, z = toolChangePosition
	file.write("G00 Z{:.3f}\n".format(z))									# first go up for savety
	
	x, y = drillPath[0]
	file.write("G00 X{:.3f} Y{:.3f}\n".format(x, y))						# place drill over first hole
	file.write("G00 Z{:.3f}\n".format(spacing))								# go down
	
	file.write("M03\n")														# turn on spindle
	file.write("G04 P1.0\n")												# wait 1 second (to turn up spindle)

	# start drilling path
	for p in drillPath:
		x, y = p

		# place drill over hole
		file.write("G00 X{:.3f} Y{:.3f}\n".format(x, y))

		# drill
		file.write("G01 Z{:.3f}\n".format(-depth))		# drill with feedrate
		#file.write("G00 Z{:.3f}\n".format(-depth))		# drill as fast as possible

		# lift drill
		file.write("G00 Z{:.3f}\n".format(spacing))


	# final G-codes
	file.write("M05\n")												# turn off spindle
	x, y, z = toolChangePosition
	file.write("G00 Z{:.3f}\n".format(z))							# first go up
	file.write("G00 X{:.3f} Y{:.3f}\n".format(x, y))				# go back to drill change position
	file.write("M02\n")												# end of program

	file.close()
