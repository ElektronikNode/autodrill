


from readDrill import *
from bilinear import *
from findPath import *


# assign holes to drills from given toolbox
# pick next larger drill except d_hole < d_drill + tol
def fitHolesToDrills(holes, drills, tol):
	diaList=list(holes.keys())		# list of hole diameters
	drillDiaList=list(drills)		# list of drill diameters
	
	diaList.sort()
	drillDiaList.sort()
	
	newHoles={}							# dict of holes with assigned diameters
	drillNo=0							# index of current drill
	drillDia=drillDiaList[0]			# current drill diameter
	
	for dia in diaList:
		
		while dia>drillDia+tol:
			# we need a bigger drill
			if drillNo==len(drillDiaList)-1:
				# there is no bigger drill
				break
			
			drillNo=drillNo+1
			drillDia=drillDiaList[drillNo]
		
		# drill fits to hole
		
		# create hole set if not existing
		if drillDia not in newHoles:
			newHoles[drillDia]=set()
			
		# assign holes
		newHoles[drillDia] |= (holes[dia])
		
	return newHoles



if __name__ == '__main__':
	
	allHoles=readDrillFile("test.drl")

	drills={0.6, 0.8, 1.1, 1.3, 1.5, 1.7, 2.0}
	
	newHoles=fitHolesToDrills(allHoles, drills, 0.05)
	
	for dia in newHoles:
		print()
		print("dia "+str(dia)+":")
		print(newHoles[dia])
		print()
		
	
	points = {(0, 0), (1, 0), (0, 1), (1, 1)}
	#points_t = {(0, 0), (1, 0.1), (-0.1, 1)}

	#path=findPath(points)
	path=findPath(newHoles[0.8])
	
	print(path)
	
	#T=bilinear(points, points_t)
	
	#p = (0.5, 0.5)

	#print(T.transform(p))

