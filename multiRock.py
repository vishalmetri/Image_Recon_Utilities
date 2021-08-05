#!/usr/bin/python3

import numpy as np
import pandas as pd
import json
import os
import shutil

##### Usage: Execute this file in a python env of choice. From the command line you can type 
##### python3 multiRock.py, hit enter.
##### The input excel file with parameters is hardcoded, you can change this.
##### The code takes a few input parameters. First, you are asked for a list of parameter names separated by spaces
##### These can be the parameters that we are varying in the input excel file
##### If no parameter is given, then the folder name is simply the first column of the input excel
##### A unique folder number is asked for. This is a number that uniquely identifies the folder
##### Algorithm: Currently fdk and mlem are supported
##### runscript: The name of the script used to initiate the job

## Read excel file #####
paramData = pd.read_excel('paramsMLEM_1to10.xlsx')
########################

## Read user input for folder names ##
print('Enter folder string separated by spaces')
inString = input()
print(inString)

# Enter first folder number #
print("Enter first folder number")
firstNum = int(input())

# Enter algorithm to use
print('Enter algorithm')
algo = input()

# Enter runscript
print('Enter runscript')
runScript = input()

## After input reading, process them ##

# Generate param json filename
outJson = 'params_' + str(algo) + '.json'

# Generate executable name
execFile = str(algo) + 'reconstructioncuda'

# Split string #
strParts = inString.split(' ')
print(strParts)
numStrParts = len(strParts)
#######################################

numRocks = paramData.shape[0]
print('Number of entries: ',numRocks)

cols = list(paramData.columns.values) # Column name list
print(cols)

z = paramData.iloc[0,:]
print(z)

for i in range(numRocks):
	z = paramData.iloc[i,:]
	outStr = ""
	## Output folder string ##
	if (numStrParts > 0): # user input blank
		for j in range(numStrParts):
			ind = cols.index(strParts[j]) # column number from column name
			outStr += str(strParts[j]) + "_" + str(z[ind]) + "_"
	else:
		outStr = z[0]
	
	outStr += str(firstNum)
	firstNum += 1
	print(outStr) # outStr is now the name of the output folder

	## Dump the row into a param json file ##
	jsonString = z.to_json(outJson,indent=1)

	## System calls ##
	os.mkdir(outStr)
	shutil.copy(outJson,outStr)
	shutil.copy(execFile,outStr)
	shutil.copy(runScript,outStr)

	## Change into subdirectory and submit the job ##
	os.chdir(outStr)
	os.system('bsub -gpu "num=8:gmodel=TeslaV100_PCIE_16GB" < %s ' % runScript)
	os.chdir('../')
	


