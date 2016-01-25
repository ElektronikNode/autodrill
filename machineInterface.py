

try:
	import linuxcnc
	linuxcnc_available=True
except ImportError:
	linuxcnc_available=False


def LinuxCNCInstalled():
	return linuxcnc_available
	
def LinuxCNCRunning():
	try:
		s = linuxcnc.stat() # create a connection to the status channel
		s.poll() 			# get current values
		return True
	except linuxcnc.error:
		return False
		
def getMachinePosition():
	try:
		s = linuxcnc.stat() # create a connection to the status channel
		s.poll() 			# get current values
		return (s.position[0], s.position[1])
	except linuxcnc.error:
		print("Could not connect to LinuxCNC.")
		
		
def jogAxis(axis, speed):
	try:
		c=linuxcnc.command()
			
		c.jog(linuxcnc.JOG_CONTINUOUS, axis, speed)
		
	except linuxcnc.error:
		print("Could not connect to LinuxCNC.")
		
		
		
def stopAxis(axis):
	try:
		c=linuxcnc.command()
			
		c.jog(linuxcnc.JOG_STOP, axis)
	except linuxcnc.error:
		print("Could not connect to LinuxCNC.")
		
		
