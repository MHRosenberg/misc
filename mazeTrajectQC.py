import numpy as np
import matplotlib.pyplot as plt
import sys
import copy

###load trajectories
deciding = True
while deciding == True:
    loadWhich = input('enter n to begin cleaning on all_traversals_maze_rawUncleaned.npy\nenter r to resume cleaning data by loading cleanedTrajectories.npy\n')
    if loadWhich.lower() == 'r':
        trajects_all = np.load('cleanedTrajectories.npy')[()] ### for loading partially cleaned data
        startAtFrame = int(input('start at frame index (starting at 0): \n'))
        deciding = False
    elif loadWhich.lower() == 'n':
        verify = input('this overwrites cleanedTrajectores.npy... are you sure? y for yes; n for no\n')
        if verify.lower() == 'y':
            trajects_all = np.load('all_traversals_maze_rawUncleaned.npy')[()] ### for loading raw data
            deciding = False
        startAtFrame = 0
    else:
        print('error: enter r or n')



### plot single excursion
#trajects_1session = trajects_all['FC1_3_15_18']
#excursionNum = 0
#traject = trajects_1session[excursionNum]
#session = 'FC3_3_15_18_1st30mins'
#trajects_1session = trajects_all[session]
#xPositions = traject[:,1] 
#yPositions = traject[:,2]
#plt.figure()
#plt.plot(xPositions, yPositions)
#plt.show()

### loop through excursion for a given dataset
trajects_all_cleaned = copy.deepcopy(trajects_all) ### uncomment to get a new copy of the original data for manual exclusions

plotNum = 0
for session in trajects_all:
    for excursionID, excursion in enumerate(trajects_all[session]):
    #    traject = trajects_1session[excursionNum]
#        if trajects_all_cleaned[session][excursionID] != []: ### skips if a trajectory was discarded cuz the excursion is set to None or []
        if len(trajects_all_cleaned[session][excursionID]) != 0: ### skips if a trajectory was discarded cuz the excursion is set to None or []
            print('\n\nplot num: ' + str(plotNum) + '; ' + session + '; excursion num: ' + str(excursionID) + '; duration in frames: ' + str(excursion.shape[0]))
            xPositions = excursion[:,1] 
            yPositions = excursion[:,2]
            
            plt.figure()
            plt.xlim(0,1)
            plt.ylim(0,1)
            plt.plot(xPositions, yPositions)
            plt.show(block = False)
            
            if plotNum >= startAtFrame:
                deciding = True
                while deciding == True:
                    decision = input('press enter to accept this trajectory, L then enter to discard it, and q then enter to exit\n')
                    if decision.lower() == '':
                        print('accepted\n')
                        deciding = False
                    elif decision.lower() == 'l':
                        print('discarding\n')
    
                        ###del trajects_all_cleaned[session][excursionId] ### introduces errors due to messing up the indices
                        trajects_all_cleaned[session][excursionID] = [] ### introduces errors due to messing up the indices
                        deciding = False
                    elif decision.lower() == 'q':
                        np.save('cleanedTrajectories.npy', trajects_all_cleaned)
                        deciding = False
                        sys.exit('data saved and loops exited')
                    else:
                        print('wrong key; try again!\n')
                    plt.close()
                    np.save('cleanedTrajectories.npy', trajects_all_cleaned)
        plotNum += 1
    np.save('cleanedTrajectories.npy', trajects_all_cleaned)
