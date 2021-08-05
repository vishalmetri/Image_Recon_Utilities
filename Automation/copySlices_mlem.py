#!/usr/bin/python3

from genericpath import isdir, isfile
import numpy as np
import pandas as pd
import json
import os
import shutil

# Script to copy slices to a common folder for easy download

###### USER INPUT #########
## Enter start and end iterations and gap
startIter = 25
endIter = 350
gapIter = 25
fNamePrefix = 'sliceMLEM'
fExtension = '.bin'
outFolder = 'outSlices'
###### USER INPUT ENDS #####

## List of files ##
numFiles = int((endIter - startIter)/gapIter + 1)
iterList = np.linspace(startIter, endIter, numFiles,dtype=np.uint16)

print('Number of files: ', numFiles )
print('File list: ',iterList)

## Output directory ##
if (not os.path.isdir(outFolder)):
	os.mkdir(outFolder)

## Get list of directory contents ##
fList = os.listdir()
currentList = len(fList)

for i in range(currentList):
	if (os.path.isdir(fList[i])):
		fList2 = os.listdir(fList[i])
		for j in iterList:
			fName = fNamePrefix + str(j) + fExtension
			if (fName in fList2):
				fPath2 = fList[i] + '/' + fName # Path of file to be copied
				print(fPath2)
				os.system('cp %s %s' % (fPath2,outFolder)) # Copy the file to output folder
				outFileName = fList[i] + '_' + fNamePrefix + str(j) + '.raw'
				os.chdir(outFolder)
				os.rename(fName, outFileName)
				os.chdir('../') 

print('Copying done')