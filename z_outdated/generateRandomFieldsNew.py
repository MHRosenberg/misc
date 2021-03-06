import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import seaborn as sns
import cv2
from scipy.ndimage import gaussian_filter
from random import randint

        
#def lowPassFilterField(img, KERNEL_WIDTH):
def lowPassFilterField(img, width):
    lowPassField = gaussian_filter(img, sigma = width) ### START HERE
    lowPassFieldNormed = np.divide(lowPassField - np.min(np.min(lowPassField)), np.max(np.max(lowPassField)) - np.min(np.min(lowPassField))) 
    return lowPassFieldNormed

def thresholdField(img, THRESHOLD, SLOPE):
    xSig = np.linspace(-6,6,1001)
    x = np.linspace(0,1,1001)-(0.5-THRESHOLD)
    sigmoid = 1/(1+np.exp(-xSig))
    
    for row in range(img.shape[0]):
        for column in range(img.shape[1]):
            idx = (np.abs(x - img[row,column])).argmin() ### normalized to sigmoid betwen 0 and 1
            img[row,column] = sigmoid[idx]
    return img
    
def makeWhiteNoiseFields(THRESHOLD, ARENA_WIDTH_IN_METERS, BINS_PER_METER, FIELD_WIDTH, SLOPE):
    whiteNoiseShape = (ARENA_WIDTH_IN_METERS*BINS_PER_METER,ARENA_WIDTH_IN_METERS*BINS_PER_METER) ### 0.1 cm spatial bin size ### consider changing this to be more flexible/general
    whiteNoiseField = np.random.random(whiteNoiseShape)
    
    lowPassField = lowPassFilterField(whiteNoiseField.copy(), FIELD_WIDTH)
    
    threshedField = thresholdField(lowPassField.copy(), THRESHOLD, SLOPE)
    
    ### for debugging only
#    plt.imshow(threshedField) #, cmap='hot') #matplot lib way
    
#    if RUN.lower() == 'single':
#        plt.close('all')
#        plt.figure()
#        ax = sns.heatmap(whiteNoiseField)
#        plt.axis('equal')
#        plt.figure()
#        sns.heatmap(lowPassField)
#        plt.axis('equal')
#        plt.figure()
#        sns.heatmap(threshedField)
#        plt.axis('equal')
    return threshedField, lowPassField, whiteNoiseField

def getNumPixels(avgFR):
    numPixels = avgFR.shape[0] * avgFR.shape[1]
    if numPixels < 20:
        sys.exit('number of pixels too low; authors do not estimate autocorrelations from less than 20 pixels')
    return numPixels

def calculateGridScore(field):
    
    lags = range(0, field.shape[0]) ### offsets from 0 to the width of the arena in bin units
    
    ######################################################### TO DO: calculate max and min lags for each point!!!!!!!!!!!!!!!
    
    xLag = None ### place holder
    yLag = None
    
    autocor = getAutocorrelation(field, lag)
        
    gridScore = 0
    grid = False
    for annulusSize in range(8,22,2): ### DOUBLE CHECK THAT THIS ENDS AT 20!!!!!!!!!!!!!!!!!!!
        
        ### get center of frame        
        ### define a centered annulus with initial radius of 8 bins (what's the bin size?) ][ binSize is 2.5; 10 bins more than central peak radius to whatever num of bins is 10 cm less than box width in 1 bin increments cm .oO other source
        ### exclude central peak of autocorrelogram
            ### for loop over an increasing distance from the center stopping at either I or II whichever comes first
            ### I first local minimum in correlation(avgDistFromTheCenter)
            
            ### II first incidence where the correlation is negative
        
        
    ### rotate annulus in 30 deg increments a full 360 degrees (all in one direction in different directions?)
    ### calc interim gridness score
        
        ### a. get max of 30, 90, 150
        maxGrdScr = 0
        for rotation in [30, 90, 150]:
            thisGrdScr = [] ########################### Oo. ?
            if thisGrdScr > maxGrdScr:
                maxGrdScr = thisGrdScr
        
        ### b. get min of 0, 60, 120 (conflicting documents regarding 0 --> TRY BOTH!)
        minGrdScr = 1000 # or some crazy high value (is there a better way?)
        for rotation in [0, 60, 120]:
            thisGrdScr = [] ########################### Oo. ?
            if thisGrdScr < minGrdScr:
                minGrdScr = thisGrdScr ### CAREFUL ABOUT PASSING BY REF INSTEAD OF VALUE ERRORS!
            
        ### b - a ]r[ a - b ? conflicting documentations)
        interimGridScore = minGrdScr - maxGrdScr
        
        if interimGridScore > gridScore:
            gridScore = interimGridScore
           
    if gridScore > 0:
        grid = True 
        
    ### compute possibly different 95th confidence interval shuffled grid metric; shuffling requires shifting along the actual movement trajectory... <-- ???
    
    return grid, gridScore

def getAutocorrelation(avgFR): ### what's the range of offsets/lags????????????????????????? from 0 to size of the arena/failure?
    
    
    ###### create sums req'd for autocorrelation over all n pixels in avgFR
    n = getNumPixels(avgFR)
    autocorrelation = np.full(avgFR.shape, np.nan)
    for xLagInd in range(0, avgFR.shape[0]):
        for yLagInd in range(0, avgFR.shape[1]):
            numeratorSum_left = 0
            numeratorSum_mid = 0
            numeratorSum_right = 0
            denominatorSum1 = 0
            denominatorSum2 = 0
            denominatorSum3 = 0
            denominatorSum4 = 0
            for xPos in range(0, avgFR.shape[0]):
                for yPos in range(0, avgFR.shape[1]):
                    xLag = xPos-xLagInd
                    yLag = yPos-yLagInd
                    if  xLag > 0 and xLag < avgFR.shape[0] and yLag > 0 and yLag < avgFR.shape[1]:
                        print('xPos: {0}, yPos: {1}, xLag: {2}, yLag: {3}'.format(xPos,yPos, xLag, yLag))                        
                        numeratorSum_left += avgFR[xPos, yPos] * avgFR[xLag, yLag]
                        numeratorSum_mid += avgFR[xPos, yPos]
                        numeratorSum_right += avgFR[xLag, yLag]
                        denominatorSum1 += np.square(avgFR[xPos, yPos])
                        denominatorSum2 += avgFR[xPos, yPos]
                        denominatorSum3 += np.square(avgFR[xLag, yLag])
                        denominatorSum4 += avgFR[xLag, yLag]           
                        numerator = n * numeratorSum_left - (numeratorSum_mid * numeratorSum_right)
                        if np.isnan(numerator):
                            sys.exit('error: nan in numerator')
                        denominator = np.sqrt(n*denominatorSum1 - np.square(denominatorSum2)) * np.sqrt(n*denominatorSum3 - np.square(denominatorSum4)) ### ERROR HERE: sqrt's go negative!
                        if np.isnan(denominator):
                            print('warning: nan in denominator')
                            print('ERROR HERE: sqrts are probably going negative')
                            zzFirst = n*denominatorSum1 - np.square(denominatorSum2)
                            zzSecond = n*denominatorSum3 - np.square(denominatorSum4)
                            zzSec1stTerm = n*denominatorSum3
                            zzSec2ndTerm = np.square(denominatorSum4)
                            if zzFirst < 0:
                                print('left denom diff went neg')
                            elif zzSecond < 0:
                                print('right denom diff went neg')
                                print('1st term: {0}\n2nd term: {1}'.format(zzSec1stTerm,zzSec2ndTerm))
                            else:
                                print('unexpected error')
                            sys.exit('ERROR: nan in denominator')
                        autocorrelation[xLagInd,yLagInd] = numerator / denominator
    
    return autocorrelation


################################################################## MAIN CODE EXECUTIION BELOW #############################################################
#MIN_NUM_FIELDS = 3
#MAX_NUM_FIELDS = 10
#


RUN = 'single' ### 'single' to plot a one field at a time; 'multiple' to several at once
REUSE_AUTOCORR = True

ARENA_WIDTH_IN_METERS = 1
BINS_PER_METER = 100 ### following deepmind supplement ("32x32 bins sqr grid spanning the environment")

###### plot single field at a time
FIELD_WIDTH = 3
THRESHOLD = 0.7 ### proportion of image to drop since values are normed between 0 and 1
SLOPE = 1
if RUN.lower() == 'single':
    field, lowPassField, whiteNoiseField = makeWhiteNoiseFields(THRESHOLD, ARENA_WIDTH_IN_METERS, BINS_PER_METER, FIELD_WIDTH, SLOPE) ### make random field
    if REUSE_AUTOCORR == False:
        autocorr = getAutocorrelation(field)

#    plt.figure()
#    ax = sns.heatmap(lowPassField)
#    plt.axis('equal')
#    ax.plot()
    
    
MAX_FIELD_WIDTH = 75
MIN_FIELD_WIDTH = 25
MAX_THRESHOLD = 0.8
MIN_THRESHOLD = 0.3
NUM_FIELDS = 25 ### make this something with an integer sqrt
fieldLst = []

if RUN.lower() == 'multiple':
    ### set up figure assuming the sine is present
    numRows = int(np.sqrt(NUM_FIELDS))
    numCols = numRows        
    figSize = (numRows, numCols)
    fig = plt.figure(figsize = figSize)
    rowPosition = 0
    columnPosition = 0
    for ind in range(0,NUM_FIELDS):    
        ### choose field parameters randomly within bounds
        fieldWidth = randint(MIN_FIELD_WIDTH, MAX_FIELD_WIDTH)
        threshold = MIN_THRESHOLD + np.random.random() * (MAX_THRESHOLD - MIN_THRESHOLD)
        
        field, lowPassField, whiteNoiseField = makeWhiteNoiseFields(threshold, ARENA_WIDTH_IN_METERS, BINS_PER_METER, fieldWidth) ### make random field
        fieldLst.append(field)
        
        ### plot random field
        print('plot: {4} of {5}\nsubplot row: {2}\nsubplot col: {3}\nmaking field with:\nthreshold: {0}\nfield width (sigma in Gaussian kernel): {1}\n\n'.format(threshold, fieldWidth, rowPosition, columnPosition, ind, 1+NUM_FIELDS))
        plt.subplot2grid((numRows, numCols), (rowPosition,columnPosition))
        plt.title('thresh: {0}; sigma: {1}'.format(threshold, fieldWidth))
        ax = sns.heatmap(field)
        plt.axis('equal')
        ax.plot()
        
        autocorr = getAutocorrelation(field)
        plt.figure()
        ax.sns.heatmap(autocorr)
        plt.axist('equal')
        ax.plot()
        if rowPosition < numRows-1:
            rowPosition += 1
        else:
            rowPosition = 0
            columnPosition += 1


    plt.show()


### TO DO: calculate grid scores and do stats here!!!!!!!!!!!!!!
#numGridCells = 0
#gridScores = []
#for field in fields:
#    grid, gridScore = calculateGridScore(field)
    
    

    

