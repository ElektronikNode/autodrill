import sys
import linuxcnc
try:
	s = linuxcnc.stat() # create a connection to the status channel
	s.poll() # get current values
except linuxcnc.error, detail:
	print "error", detail
	sys.exit(1)
	
print s.position
