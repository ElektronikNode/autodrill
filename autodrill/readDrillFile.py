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

import re

# read .drl file (excellon format)
# return value:
#	dictionary from drill diameter to set X/Y-coordinates
#	e.g.: {d1 -> {(x1, y1, ID1), (x2, y2, ID2), ...}, d2 -> {(x3, y3, ID3), (x4, y4, ID4), ...}, ...}

def readDrillFile(filename):
	try:
		drillfile=open(filename, "rU")

	except:
		print("could not open file!")
		return

	tools={}
	holes={}

	unit="metric"				# "metric" or "inch" units
	zeroMode="trailing"			# "leading" or "trailing" zeros are kept
	leftDigits=3				# digits left of decimal point
	rightDigits=3				# digits right of decimal point
	fileFormatSpecified=False	# True if the line ;FILE_FORMAT=... was found

	ID=0						# ID of hole
	
	x=0							# last coordinates
	y=0

	for line in drillfile:
		
		# read "FILE_FORMAT"
		mo=re.search(r"^;FILE_FORMAT=(\d+):(\d+)$", line)
		if mo:
			fileFormatSpecified=True
			leftDigits=int(mo.group(1))
			rightDigits=int(mo.group(2))

		# read unit
		if ("M71" in line) or ("METRIC" in line):
			unit="metric"
			# default metric format: 000.000
			if not fileFormatSpecified:
				leftDigits=3
				rightDigits=3
				
		if ("M72" in line) or ("INCH" in line):
			unit="inch"
			#default inch format: 00.0000
			if not fileFormatSpecified:
				leftDigits=2
				rightDigits=4

		# read zeroMode
		if "LZ" in line:
			zeroMode="leading"
		if "TZ" in line:
			zeroMode="trailing"


		# read tool table
		mo=re.search(r"^T(\d+)(F(\d+))?(S(\d+))?C(\d*\.\d*)$", line)
		if mo:
			#print mo.group()
			toolNum=int(mo.group(1))
			toolDia=float(mo.group(6))
			if(unit=="inch"):
				toolDia=toolDia*25.4
			#print toolNum, toolDia
			tools[toolNum]=toolDia
			holes[toolDia]=set()


		# tool change
		mo=re.search(r"^T(\d+)$", line)
		if mo:
			tool=int(mo.group(1))
			if tool in tools:
				currentTool=tool
			
		
		# read coordinates
		coordinateFound=False

		# read X without decimal point
		mo=re.search(r"X(-?\d+)", line)
		if mo:
			s=mo.group(1)
			coordinateFound=True
			
			# for leading zeros we need to append the missing trailing zeros
			if zeroMode=="leading":
				s=s.ljust(leftDigits+rightDigits, '0')
			
			# convert to float and correct decimal point
			co=float(s)/pow(10, rightDigits)
			
			# conversion from inch to metric
			if unit=="inch":
				x=co*25.4
			else:
				x=co
				
		# read Y without decimal point
		mo=re.search(r"Y(-?\d+)", line)
		if mo:
			s=mo.group(1)
			coordinateFound=True
			
			# for leading zeros we need to append the missing trailing zeros
			if zeroMode=="leading":
				s=s.ljust(leftDigits+rightDigits, '0')
			
			# convert to float and correct decimal point
			co=float(s)/pow(10, rightDigits)
			
			# conversion from inch to metric
			if unit=="inch":
				y=co*25.4
			else:
				y=co
				
		# read X with decimal point
		mo=re.search(r"X(-?\d*\.\d*)", line)
		if mo:
			co=float(mo.group(1))
			coordinateFound=True
			
			# conversion from inch to metric
			if unit=="inch":
				x=co*25.4
			else:
				x=co
					
		# read Y with decimal point
		mo=re.search(r"Y(-?\d*\.\d*)", line)
		if mo:
			co=float(mo.group(1))
			coordinateFound=True
			
			# conversion from inch to metric
			if unit=="inch":
				y=co*25.4
			else:
				y=co

		
		if coordinateFound:	
			#print("read hole: "+str(tools[currentTool])+", "+str(x)+", "+str(y))
			holes[tools[currentTool]].add((x, y, ID))
			ID=ID+1

	return holes
