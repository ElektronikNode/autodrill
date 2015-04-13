
import re

# read .drl file (excellon format)
# return value:
#	dictionary from drill diameter to set X/Y-coordinates
#	e.g.: {d1 -> {(x1, y1), (x2, y2), ...}, d2 -> {(x3, y3), (x4, y4), ...}, ...}

def readDrillFile(filename):
	try:
		drillfile=open(filename, "r")

	except:
		print("could not open file!")
		return
	
	tools={}
	holes={}
	
	for line in drillfile:
		
		# read tool table
		mo=re.search(r"^T(\d+)C(\d+\.\d+)$", line)
		if mo:
			#print mo.group()
			toolNum=int(mo.group(1))
			toolDia=float(mo.group(2))
			#print toolNum, toolDia
			tools[toolNum]=toolDia
			
			holes[toolDia]=set()
			
		
		# tool change
		mo=re.search(r"^T(\d+)$", line)
		if mo:
			currentTool=int(mo.group(1))
			
		
		# read coordinates
		mo=re.search(r"^X(-?\d+.\d+)Y(-?\d+.\d+)$", line)
		if mo and currentTool in tools:
			
			holes[tools[currentTool]].add((float(mo.group(1)), float(mo.group(2))))
	
	
	return holes


