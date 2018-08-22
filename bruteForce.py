import argparse
from copy import deepcopy
import math
import time
import sys

start = time.time()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputFile',
                   help='the randTSP file to import.  each city must be on its own line, consisting of a name, x quardinate, and y quardinate seperated by spaces')
#This is for easy exporting to excel to create the plots
parser.add_argument('-r','--raw', action="store_true",
                   help='only outputs final length')

parser.add_argument('-t','--time', action="store_true",
                   help='only outputs time it took to complete')

args = parser.parse_args()


class city:
	name = "_";
	x = 0
	y = 0

cityList = []


F = open(args.inputFile)

#import cities
i=0
for line in F:
  tempStr = line.split()
  if len(tempStr) > 1:
  	newCity = city()
  	newCity.name = tempStr[0]
  	newCity.x = int(tempStr[1])
  	newCity.y = int(tempStr[2])
  	cityList.append(newCity)


F.close()

minimum = 99999999999
optimumOrder = []
states = []

def compute(order, left, length):
	global minimum
	global optimumOrder
	if len(left) == 0:
		length += math.sqrt((order[-1].x - order[0].x)**2 + (order[-1].y - order[0].y)**2)
		order.append(order[0])
		if length < minimum:
			#print(length)
			#for c in order:
			#	print(c.name)
			#print()
			minimum = length
			optimumOrder = order[:]
	current = time.time()
	global start
	if current - start >=300:
		print("timeout... current minimum: " + str(minimum))
		sys.exit()
	for c in left:
		newOrder = order[:]
		newOrder.append(c)
		newLeft = left[:]
		newLeft.remove(c)
		partLength = math.sqrt((order[-1].x - c.x)**2 + (order[-1].y - c.y)**2)
		compute(newOrder,newLeft,length + partLength)




order = []
left = []
order.append(cityList[0])
cityList.pop(0)
compute(order, cityList, 0)

if args.raw:
	print(minimum)
else:
	print("Minimum distance: " + str(minimum) + " in time: " + str(time.time() - start))

	for c in optimumOrder:
		print(c.name)