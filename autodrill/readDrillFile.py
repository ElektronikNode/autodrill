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

	unit="metric"		# assume mm units by default
	zeroMode="trailing"	# assume trailing zeros by default

	ID=0

	for line in drillfile:

		# read unit
		if ("M71" in line) or ("METRIC" in line):
			unit="metric"
		if ("M72" in line) or ("INCH" in line):
			unit="inch"

		# read zeroMode
		if "LZ" in line:
			zeroMode="leading"
		if "TZ" in line:
			zeroMode="trailing"


		# read tool table
		mo=re.search(r"^T(\d+)C(\d*\.\d+)$", line)
		if mo:
			#print mo.group()
			toolNum=int(mo.group(1))
			toolDia=float(mo.group(2))
			if(unit=="inch"):
				toolDia=toolDia*25.4
			#print toolNum, toolDia
			tools[toolNum]=toolDia

			holes[toolDia]=set()


		# tool change
		mo=re.search(r"^T(\d+)$", line)
		if mo:
			currentTool=int(mo.group(1))

		# read coordinates (with decimal point)
		mo=re.search(r"^X(-?\d+\.\d+)Y(-?\d+\.\d+)$", line)
		if mo and currentTool in tools:
			x=float(mo.group(1))
			y=float(mo.group(2))
			if unit=="inch":
				x=x*25.4
				y=y*25.4
			holes[tools[currentTool]].add((x, y, ID))

		# read coordinates (without decimal point)
		mo=re.search(r"^X(-?\d+)Y(-?\d+)$", line)
		if mo and currentTool in tools:
			strX=mo.group(1)
			strY=mo.group(2)
			if zeroMode=="leading":
				strX=strX.ljust(6, '0')		# there are always 6 digits
				strY=strY.ljust(6, '0')

			x=float(strX)
			y=float(strY)
			if(unit=="metric"):
				x=x/1000		# metric format: 000.000
				y=y/1000
			elif(unit=="inch"):
				x=x/10000*25.4	# inch format: 00.0000
				y=y/10000*25.4

			holes[tools[currentTool]].add((x, y, ID))

		ID=ID+1

	return holes
