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

from logger import logger
logger = logger.getChild(__name__)


try:
	import linuxcnc
	linuxcnc_available=True
except ImportError:
	linuxcnc_available=False
	logger.warning("could not find LinuxCNC")


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
		return (s.position[0]-s.g5x_offset[0], s.position[1]-s.g5x_offset[1], s.position[2]-s.g5x_offset[2])
	except linuxcnc.error:
		logger.warning("Could not connect to LinuxCNC.")
		return (0,0,0)


def isEmergencyStopPressed():
	try:
		s = linuxcnc.stat() # create a connection to the status channel
		s.poll() 			# get current values
		return s.estop
	except linuxcnc.error:
		logger.warning("Could not connect to LinuxCNC.")
		return None


def isMachineEnabled():
	try:
		s = linuxcnc.stat() # create a connection to the status channel
		s.poll() 			# get current values
		return s.enabled and not s.estop
	except linuxcnc.error:
		logger.warning("Could not connect to LinuxCNC.")
		return None


def isMachineHomed():
	try:
		s = linuxcnc.stat() # create a connection to the status channel
		s.poll() 			# get current values
		return s.homed
	except linuxcnc.error:
		logger.warning("Could not connect to LinuxCNC.")
		return None


def jogAxis(axis, speed):
	if not isMachineEnabled():
		return

	try:
		c=linuxcnc.command()

		c.jog(linuxcnc.JOG_CONTINUOUS, axis, speed)

	except linuxcnc.error:
		logger.warning("Could not connect to LinuxCNC.")


def stopAxis(axis):
	if not isMachineEnabled():
		return

	try:
		c=linuxcnc.command()

		c.jog(linuxcnc.JOG_STOP, axis)
	except linuxcnc.error:
		logger.warning("Could not connect to LinuxCNC.")
