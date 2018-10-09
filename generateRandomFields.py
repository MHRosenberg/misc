import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import seaborn as sns
import cv2
from scipy.ndimage import gaussian_filter
from random import randint

def checkAsymmetry(covMat): ### OBSOLETE NOW THAT I'M USING MM'S WHITE NOISE METHOD TO GENERATE FIELDS
    symmetricEnough = False
    w,v = np.linalg.eig(covMat)
    # print('eigenvalues: ' + str(w))
    if np.abs(w[0]/w[1]) < MAX_ASYMMETRY_RATIO and np.abs(w[1]/w[0]) < MAX_ASYMMETRY_RATIO:
        print('\nfield passed constraints\n')
        symmetricEnough = True
    else:
        print('\n\ntoo asymmetric --> computing a new field\n')
    print('\neigenvalues: {0}'.format(w))
    return symmetricEnough

def makeGaussianFields(MAX_NUM_FIELDS, ARENA_SIZE_IN_METERS): ### OBSOLETE NOW THAT I'M USING MM'S WHITE NOISE METHOD TO GENERATE FIELDS
    numFields = np.ceil(MAX_NUM_FIELDS * np.random.rand())
    randPositions = ARENA_SIZE_IN_METERS - ARENA_SIZE_IN_METERS * (np.random.rand(int(numFields),2))
    fields = []
    # for fieldInd in range(0,MAX_NUM_FIELDS):
    for randPosition in randPositions:
        print(randPosition)
        m = randPosition

        fieldPassesConstraints = False
        while fieldPassesConstraints == False:
            
            ### field shapes:
            ###        elliptical
            # s = np.eye(2) * np.random.rand(2) -0.5 
            ###     circular
            # s = np.eye(2) # for circular fields
            ###     random
            s = np.random.rand(2,2) - 0.5 ################################ WARNING: ARBITRARY VALUES --> replace with something principled
            ###     hardcoded
            # s = np.matrix('10 4; -4 1')
            s = np.dot(s,s.transpose())
            fieldPassesConstraints = checkAsymmetry(s) 

        
        k = multivariate_normal(mean=m, cov=s) ### makes the field        
        fields.append(k)
        
        ### WIP TESTING
        NUM_SPIKES = 100
        x, y = np.random.multivariate_normal(m, s,NUM_SPIKES).T ### makes the field
        plt.plot(x, y, 'x')
        plt.axis('equal')
        plt.show()

    # # create 2 kernels
    # # m1 = (-1,-1)
    # # s1 = np.eye(2)
    # # k1 = multivariate_normal(mean=m1, cov=s1)
    # # m2 = (1,1)
    # # s2 = np.eye(2)
    # # k2 = multivariate_normal(mean=m2, cov=s2)

    # create a grid of (x,y) coordinates at which to evaluate the kernels
    xlim = (0, ARENA_SIZE_IN_METERS)
    ylim = (0, ARENA_SIZE_IN_METERS)
    xres = 200
    yres = 200

    x = np.linspace(xlim[0], xlim[1], xres)
    y = np.linspace(ylim[0], ylim[1], yres)
    xx, yy = np.meshgrid(x,y)

    xxyy = np.c_[xx.ravel(), yy.ravel()]
    zz = fields[0].pdf(xxyy)
    for field in fields[1::]:
        print(field)
        # # evaluate kernels at grid points
        xxyy = np.c_[xx.ravel(), yy.ravel()]
        zz = zz + field.pdf(xxyy) #+ k2.pdf(xxyy) ################### is this the field?

        # # reshape and plot image
        img = zz.reshape((xres,yres)) #################################### WHAT DOES THIS DO?
        plt.imshow(img);
        plt.hold()
    plt.show()
    return fields

def viewFields(): ### OBSOLETE NOW THAT I'M USING MM'S WHITE NOISE METHOD TO GENERATE FIELDS
    while True:
        makeGaussianFields(MAX_NUM_FIELDS, ARENA_SIZE_IN_METERS)
        
#def lowPassFilterField(img, KERNEL_WIDTH):
def lowPassFilterField(img, width):
    lowPassField = gaussian_filter(img, sigma = width) ### START HERE
    lowPassFieldNormed = np.divide(lowPassField - np.min(np.min(lowPassField)), np.max(np.max(lowPassField)) - np.min(np.min(lowPassField))) 
    return lowPassFieldNormed

def thresholdField(img, THRESHOLD):
    for row in range(img.shape[0]):
        for column in range(img.shape[1]):
            if img[row,column] < THRESHOLD:
                img[row,column] = 0
    return img
    
def makeWhiteNoiseFields(THRESHOLD, ARENA_WIDTH_IN_METERS, BINS_PER_METER, FIELD_WIDTH):
    whiteNoiseShape = (ARENA_WIDTH_IN_METERS*BINS_PER_METER,ARENA_WIDTH_IN_METERS*BINS_PER_METER) ### 0.1 cm spatial bin size ### consider changing this to be more flexible/general
    whiteNoiseField = np.random.random(whiteNoiseShape)
    
    lowPassField = lowPassFilterField(whiteNoiseField.copy(), FIELD_WIDTH)
    
    threshedField = thresholdField(lowPassField.copy(), THRESHOLD)
    
    blurredThresh = lowPassFilterField(threshedField, FIELD_WIDTH)
    
    ### for debugging only
#    plt.imshow(threshedField) #, cmap='hot') #matplot lib way
    
    if RUN.lower() == 'single':
        plt.close('all')
        plt.figure()
        ax = sns.heatmap(whiteNoiseField)
        plt.axis('equal')
        plt.figure()
        sns.heatmap(lowPassField)
        plt.axis('equal')
        plt.figure()
        sns.heatmap(threshedField)
        plt.axis('equal')
        plt.figure()
        sns.heatmap(blurredThresh)
        plt.axis('equal')
        plt.show()
    return blurredThresh, threshedField, lowPassField, whiteNoiseField

def getNumPixels(avgFR):
    numPixels = avgFR.shape[0] *avgFR.shape[1]
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
    numeratorSum_left = 0
    numeratorSum_mid = 0
    numeratorSum_right = 0
    denominatorSum1 = 0
    denominatorSum2 = 0
    denominatorSum3 = 0
    denominatorSum4 = 0
    for xPos in range(0, avgFR.shape[0]):
        for yPos in range(0, avgFR.shape[1]):
            for xLagInd in range(0, avgFR.shape[0]):
                for yLagInd in range(0, avgFR.shape[1]):
                    xLag = xPos-xLagInd
                    yLag = yPos-yLagInd
                    if not xLag == 0 and yLag == 0:                        
                        numeratorSum_left += avgFR[xPos,yPos] * avgFR[xPos- xLag, yPos - yLag]
                        numeratorSum_mid += avgFR[xPos,yPos]
                        numeratorSum_right += avgFR[xPos-xLag,yPos-yLag]
                        denominatorSum1 += np.square(avgFR[xPos,yPos])
                        denominatorSum2 += numeratorSum2
                        denominatorSum3 += np.square(avgFR[xPos-xLag,yPos-yLag])
                        denominatorSum4 += numeratorSum3
    ######        
    
    numerator = n * numeratorSum1 - (numeratorSum2 * numeratorSum3) ###################### check the second term... I'm not sure about the summation order of operations }{ grouping etc
    sys.exit('fix prior line!!!!')
    denominator = np.sqrt(n*denominatorSum1 - np.square(denominatorSum2)) * np.sqrt(n*denominatorSum3 - np.square(denominatorSum4)) 
    autocorrelation = numerator / denominator
    
    return autocorrelation


################################################################## MAIN CODE EXECUTIION BELOW #############################################################
#MIN_NUM_FIELDS = 3
#MAX_NUM_FIELDS = 10
#
## numFields = np.random.random_integers(MIN_NUM_FIELDS, MAX_NUM_FIELDS) # WIP: use this to randomize the number of grid fields generated
#

#MAX_ASYMMETRY_RATIO = 4
#
#### visually inspect random fields
#viewFields()

### select type of field here
#MAX_NUM_FIELDS = 10 # must be >= 2
#fields = makeGaussianFields(MAX_NUM_FIELDS, ARENA_SIZE_IN_METERS)

RUN = 'single' ### 'single' to plot a one field at a time; 'multiple' to several at once

ARENA_WIDTH_IN_METERS = 1
BINS_PER_METER = 32 ### following deepmind supplement ("32x32 bins sqr grid spanning the environment")

###### plot single field at a time
FIELD_WIDTH = 4
THRESHOLD = 0.75 ### proportion of image to drop since values are normed between 0 and 1
if RUN.lower() == 'single':
    field, threshField, lowPassField, whiteNoiseField = makeWhiteNoiseFields(THRESHOLD, ARENA_WIDTH_IN_METERS, BINS_PER_METER, FIELD_WIDTH) ### make random field

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
        
        field, threshField, lowPassField, whiteNoiseField = makeWhiteNoiseFields(threshold, ARENA_WIDTH_IN_METERS, BINS_PER_METER, fieldWidth) ### make random field
        fieldLst.append(field)
        
        ### plot random field
        print('plot: {4} of {5}\nsubplot row: {2}\nsubplot col: {3}\nmaking field with:\nthreshold: {0}\nfield width (sigma in Gaussian kernel): {1}\n\n'.format(threshold, fieldWidth, rowPosition, columnPosition, ind, 1+NUM_FIELDS))
        plt.subplot2grid((numRows, numCols), (rowPosition,columnPosition))
        plt.title('thresh: {0}; sigma: {1}'.format(threshold, fieldWidth))
        ax = sns.heatmap(field)
        plt.axis('equal')
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
    
    

    

