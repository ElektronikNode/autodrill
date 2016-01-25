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
