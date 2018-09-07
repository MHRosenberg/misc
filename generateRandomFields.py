import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

def checkAsymmetry(covMat):
    symmetricEnough = 0
    w,v = np.linalg.eig(covMat)
    # print('eigenvalues: ' + str(w))
    if np.abs(w[0]/w[1]) < MAX_ASYMMETRY_RATIO and np.abs(w[1]/w[0]) < MAX_ASYMMETRY_RATIO:
        print('\nfield passed constraints\n')
        symmetricEnough = 1
    else:
        print('\n\ntoo asymmetric --> computing a new field\n')
    print('\neigenvalues: \n')
    return symmetricEnough

def makeFields(MAX_NUM_FIELDS, ARENA_SIZE_IN_METERS):
    numFields = np.ceil(MAX_NUM_FIELDS * np.random.rand())
    randPositions = ARENA_SIZE_IN_METERS - ARENA_SIZE_IN_METERS * (np.random.rand(int(numFields),2))
    fields = []
    # for fieldInd in range(0,MAX_NUM_FIELDS):
    for randPosition in randPositions:
        print(randPosition)
        m = randPosition

        fieldPassesConstraints = 0
        while fieldPassesConstraints == 0:
            
            ### field shapes:
            ###        elliptical
            # s = np.eye(2) * np.random.rand(2) -0.5 
            ###     circular
            # s = np.eye(2) # for circular fields
            ###     random
            s = np.random.rand(2,2) - 0.5
            ###     hardcoded
            # s = np.matrix('10 4; -4 1')
            s = np.dot(s,s.transpose())
            fieldPassesConstraints = checkAsymmetry(s) 

        
        k = multivariate_normal(mean=m, cov=s)
        fields.append(k)

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

def viewFields():
    while True:
        makeFields(MAX_NUM_FIELDS, ARENA_SIZE_IN_METERS)

def getNumPixels(avgFR):
    numPixels = [] #############3 something like shape[0]*shape[1] of the avgFR
    if numPixels < 20:
        sys.exit('number of pixels too low; authors do not estimate autocorrelations from less than 20 pixels')
    return numPixels

def getAutocorrelation(avgFR): ### what's the range of offsets?
    
    ### determine reasonable x and y offset ranges
    
    n = getNumPixels(avgFR)
    ############################# sum over all n pixels in avgFR
    numeratorSum1 = []
    numeratorSum2 =[]
    numeratorSum3 =[]
    denominatorSum1 =[]
    denominatorSum2 =[]
    denominatorSum3 =[]
    denominatorSum4 =[]
    numerator = n * numeratorSum1 - (numeratorSum2 * numeratorSum3) # check the second term... I'm not sure about the summation order of operations }{ grouping etc
    denominator = np.sqrt(n*denominatorSum1 - np.square(denominatorSum2)) * np.sqrt(n*denominatorSum3 - np.square(denominatorSum4)) 
    autocorrelation = numerator / denominator
    
    return autocorrelation
        
def calculateGridScore(field):
    print('TO DO:')
    
    autocor = getAutocorrelation(field)
        
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
        grid = True ##### why is this a local variable?
        
    ### compute possibly different 95th confidence interval shuffled grid metric; shuffling requires shifting along the actual movement trajectory... 
    
    return grid, gridScore

################################################################## MAIN CODE EXECUTIION BELOW #############################################################
MIN_NUM_FIELDS = 3
MAX_NUM_FIELDS = 10

# numFields = np.random.random_integers(MIN_NUM_FIELDS, MAX_NUM_FIELDS) # WIP: use this to randomize the number of grid fields generated
MAX_NUM_FIELDS = 10 # must be >= 2
ARENA_SIZE_IN_METERS = 5
MAX_ASYMMETRY_RATIO = 4

### visually inspect random fields
#viewFields()

fields = makeFields(MAX_NUM_FIELDS, ARENA_SIZE_IN_METERS)

numGridCells = 0
gridScores = []
for field in fields:
    grid, gridScore = calculateGridScore(field)
    
    

    

