
def writeGCode(dia, path):
	
	feedrate=500	# TODO
	spacing=2
	depth=2
	drillChangePosition=(0, 0, 100)
	
	file=open(str(dia)+".ngc", "w")
	
	
	# initial G-codes
	file.write("G90\n")									# set to absolut positioning
	#file.write("G21\n")								# use millimeters
	file.write("F{:f}\n".format(feedrate))				# set feedrate
	
	file.write("M03\n")														# turn on spindle
	x, y = path[0]
	file.write("G00 X{:.3f} Y{:.3f} Z{:.3f}\n".format(x, y, spacing))		# place drill over first hole
	file.write("G04 P1.0\n")												# wait 1 second (to turn up spindle)
	
	# start drilling path
	for p in path:
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
	x, y, z = drillChangePosition
	file.write("G00 X{:.3f} Y{:.3f} Z{:.3f}\n".format(x, y, z))		# go back to drill change position
	file.write("M02\n")												# end of program
	
	file.close()
