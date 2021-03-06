#!/usr/local/bin/python3

# CMSC 441 Project 1
# Daniel Lesko
# Rachel Cohen

from __future__ import print_function
# Importing some common modules
import os, sys
import pprint
import time

#define the max number of pairings that we need between each pair
min_distance = 4 

#dictionary to store previous pairs, used in memoization 
memoOPT={}

#main function for our dynamic programming problem
def linePairing(data):

	S = set()
	dataLength = len(data)

	#create array to store a list of max pairs in a line
	OPT_array = [[0 for x in range(dataLength)] for y in range(dataLength)]


	#fill the OPT_array
	#keep track of time
	start_time = time.time()
	#nested loops for i,j where i must have 4 chars between j
	for i in range(0, dataLength - min_distance):
		for j in range(i+min_distance, dataLength):
			OPT_array[i][j] = opt(i, j, data)
	elapsed_time = time.time() - start_time

	#call to path function, pairs stored in S
	path(OPT_array, data, 0, dataLength-1, S)


	#file I/O
	f = open('outputPath.txt', 'w')

	S = sorted(S)
	f.write("Elapsed Time (s) - ")
	f.write(str(elapsed_time))
	f.write('\n')
	f.write("Number of Pairs - ")
	f.write(str(len(S)))
	f.write('\n')
	f.write("Line Pairs: \n")
	for elem in S:
		f.write(str(elem))
		f.write('\n')

def opt(i,j, data):

	#return if already exists
	if (i,j) in memoOPT:
		return memoOPT[(i,j)]
	
	#return if there is not the min distance between i and j
	if (i >= j - min_distance):
		return 0

	#otherwise we enter our sub problems
	else:

		#call to see there is not a pair
		#if we don't already have the value memoized,
		#call the recursive function
		if (i,j-1) not in memoOPT:
			notPaired = opt(i, j-1, data)
		else:
			notPaired = memoOPT[(i,j-1)]

		#set up to find best pairings
		best = -1;

		#iterate over t to find the max pairings in
		#a_1 ... a_t-1 and a_t+1 to a_j-1
		#return the max
		for t in range(i, j-min_distance):
			if (matchFn(data[t], data[j])):

				if (i, t-1) not in memoOPT:
					call1 = opt(i, t-1, data)
				else:
					call1 = memoOPT[(i, t-1)]

				if (t+1, j-1) not in memoOPT:
					call2 = opt(t+1, j-1, data)
				else:
					call2 = memoOPT[(t+1, j-1)]

				temp = (1 + call1 + call2)
				if temp > best:
					#memoOPT[(i,j)] = temp
					best = temp
		paired = best

		#store our max in our dictionary for later use
		memoOPT[(i,j)] = max(notPaired, paired)
		#return the max to the OPT_array
		return max(notPaired, paired)

def path(OPT_array, data, i, j, S):

	if i <= j-min_distance:

		#check path under to see if the same
		if OPT_array[i][j] == OPT_array[i+1][j]:
			path(OPT_array, data, i+1, j, S)

		#check path to the left to see if the same
		elif OPT_array[i][j] == OPT_array[i][j-1]:
			path(OPT_array, data, i, j-1, S)

		#check path to the diagonal to check for match
		elif OPT_array[i][j] == OPT_array[i+1][j-1] + matchFn(data[i], data[j]):
			#print ("Found match!")
			S.add((i, j))
			#call opt from new position in matrix
			path(OPT_array, data, i+1, j-1, S)

		#trace path for smaller sub problems
		else:
			for k in range(i, j):
				if OPT_array[i][j] == OPT_array[i][k] + OPT_array[k+1][j]:
					path(OPT_array, data, i, k, S)
					path(OPT_array, data, k+1, j, S)
					break

	return

#function to check and see if there is a pair
def matchFn(i, j):
	isMatch = i + j

	matches = set(["TW", "WT", "GH", "HG"])

	if isMatch in matches:
		#print ("Yes")
		return True
	else:
		#print ("No")
		return False

#function to read in the line of fans
def readString(stringFile, stringLength):
	with open(stringFile, "r") as f:
		data = f.read().replace('\n', '')

		if stringLength != -1:
			data = data[:int(stringLength)]

	return data

# This is the main function that acts as an entry point for the program
if __name__=="__main__":

	stringFile = sys.argv[1]

	if (len(sys.argv) > 2):
		stringLength = sys.argv[2]
	else:
		stringLength = -1

	data = readString(stringFile, stringLength)

	linePairing(data)


'''
Times

2000 : 1183.7687077522278
1500 : 482.6276047229767
1000 : 139.41797423362732
500  : 17.00997304916382
100  : 0.11900687217712402
90   : 0.08600497245788574
80   : 0.06000351905822754
70   : 0.04200243949890137
60   : 0.026001453399658203
50   : 0.014000654220581055
40   : 0.008000373840332031
30   : 0.0030002593994140625
20   : 0.0010001659393310547
10   : 0.0009999275207519531

http://arachnoid.com/polysolve/


Second Set - Randomized

100  : 0.12000679969787598
200  : 1.0020573139190674
300  : 3.498199939727783
400  : 8.509486675262451
500  : 17.170982122421265
600  : 29.522688388824463 
700  : 48.67878437042236
800  : 72.61715340614319
900  : 103.16590070724487
1000 : 143.08318376541138
1100 : 196.51523995399475
1200 : 254.38555002212524
1300 : 325.81263542175293
1400 : 405.2131769657135
1500 : 502.38073468208313

Third - All Input The Same (No Pairs)

1500 : 361.3236663341522
1400 : 297.2346598123984
1300 : 235.5744743347168
1200 : 184.50655317306519
1100 : 142.30013918876648
1000 : 105.01300644874573
900  : 76.81339359283447
800  : 54.9501428604126
700  : 36.10606527328491
600  : 22.770302295684814
500  : 12.975742101669312
400  : 6.611378192901611
300  : 2.736156463623047
200  : 0.8110463619232178
100  : 0.09700560569763184


'''

	
