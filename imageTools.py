import numpy as np
import pandas as pd
from skimage import measure
from matplotlib import pyplot as plt


class Point():
    def __init__(self, x, y):
        self.X = x
        self.Y = y

class Point3():
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z
        

class Image:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.data = np.zeros((x * y))

    def readFromFile2D(self, fPath, fmt):
        self.data = np.fromfile(fPath, dtype=fmt, sep="")
        self.data = self.data.reshape(self.X, self.Y)
        
    def getNorm(self,norm='fro'):
        return np.linalg.norm(self.data,norm)


class LinePlot(Image, Point):
    def __init__(self,im, p1, p2):
        self.startPoint = p1
        self.endPoint = p2
        self.imData = im.data
        
    def getLineProfile(self):
        x1 = self.startPoint.X
        y1 = self.startPoint.Y
        x2 = self.endPoint.X
        y2 = self.endPoint.Y
        self.lpdata = measure.profile_line(self.imData,(y1,x1),(y2,x2))
        
    def drawLine(self,options):
        p1 = [self.startPoint.X,self.endPoint.X]
        p2 = [self.startPoint.Y,self.endPoint.Y]
        plt.plot(p1,p2,color = options['color'], linewidth = options['linewidth'])
        
    def getLength(self):
        x1 = self.startPoint.X
        y1 = self.startPoint.Y
        x2 = self.endPoint.X
        y2 = self.endPoint.Y
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    

def getLineProfiles(dirPath, fName, imX, imY, fmt, lineLims):
    ## Image params ##
    im = Image(imX,imY)
    ## Load image ##
    imPath = dirPath + '\\' + fName
    im.readFromFile2D(imPath,fmt)
    ################
    
    ## Read line limits for profiles ##
    #lpFilePath = dirPath + '\\' + lineProfFile
    #lineLims = pd.read_excel(lpFilePath)
    #print(lineLims)
    #lineLims = lineLims.to_numpy()
    print(lineLims)

    ## Process lineLims ##
    s = np.shape(lineLims)
    numRegions = s[0]
    print(numRegions)
    
    ## Initialize output list ##
    lp = []
    ###################################
    for i in range(numRegions):
        x1 = lineLims[i,0]
        y1 = lineLims[i,1]
        x2 = lineLims[i,2]
        y2 = lineLims[i,3]
    
        p1 = Point(x1,y1)
        p2 = Point(x2,y2)

        lp1 = LinePlot(im,p1,p2)
        lp1.getLineProfile()
        lp.append(lp1.lpdata)
     
    #df0 = pd.DataFrame(lp)
    #df0 = df0.T
    #return df0
    return lp

## This needs work ##
def readFromFile3D(im, X, Y, sliceNum, fPath, fmt):
    if (fmt == 'single'):
        numBytes = 4
    elif (fmt == 'uint16'):
        numBytes = 2
    elif (fmt == 'uint8'):
        numBytes = 1

    im = np.fromfile(fPath, dtype=fmt, count=X * Y, offset=X * Y * sliceNum * numBytes, sep="")
    im = im.reshape(X, Y)
    return im
#######################
