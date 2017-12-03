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


def writeGCode(paths, filename, feedrate, depth, spacing):
	
	outfile=QFile(filename)
	
	outfile.open(QIODevice.WriteOnly)
	
	# initial G-codes
	outfile.write("G90\n")									# set to absolut positioning
	outfile.write("G21\n")									# units: millimeters
	outfile.write("F{:f}\n".format(feedrate*60))			# set feedrate (mm/min)
	
	tools=paths.keys()
	tools.sort()											# begin with smallest drill
	
	for toolNr in tools:
		writeDrillPath(outfile, toolNr, paths[toolNr], depth, spacing)
	
	outfile.write("T0\n".format(toolNr))					# select no tool
	outfile.write("M06\n")									# change tool
	outfile.write("M02\n")									# end of program
	outfile.close()
	
	
def writeDrillPath(outfile, toolNr, drillPath, depth, spacing):

	outfile.write("T{:d}\n".format(toolNr))							# select tool
	outfile.write("M06\n")											# change tool
	outfile.write("G00 Z{:.3f}\n".format(spacing))					# first go up to spacing height
	
	outfile.write("M03\n")											# turn on spindle
	outfile.write("G04 P1.0\n")										# wait 1 second (to turn up spindle)

	# start drilling path
	for p in drillPath:
		x, y = p

		# place drill over hole
		outfile.write("G00 X{:.3f} Y{:.3f}\n".format(x, y))

		# drill
		outfile.write("G01 Z{:.3f}\n".format(-depth))		# drill with feedrate
		#outfile.write("G00 Z{:.3f}\n".format(-depth))		# drill as fast as possible

		# lift drill
		outfile.write("G00 Z{:.3f}\n".format(spacing))


	# final G-codes
	outfile.write("M05\n")									# turn off spindle

