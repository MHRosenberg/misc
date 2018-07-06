import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

MIN_NUM_FIELDS = 1
MAX_NUM_FIELDS = 5

# numFields = np.random.random_integers(MIN_NUM_FIELDS, MAX_NUM_FIELDS) # WIP: use this to randomize the number of grid fields generated
MAX_NUM_FIELDS = 10 # must be >= 2
ARENA_SIZE_IN_METERS = 5
MAX_ASYMMETRY_RATIO = 4

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
			###		elliptical
			# s = np.eye(2) * np.random.rand(2) -0.5 
			### 	circular
			# s = np.eye(2) # for circular fields
			### 	random
			s = np.random.rand(2,2) - 0.5
			### 	hardcoded
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
		zz = zz + field.pdf(xxyy) #+ k2.pdf(xxyy)

		# # reshape and plot image
		img = zz.reshape((xres,yres)) #################################### WHAT DOES THIS DO?
		plt.imshow(img);
		plt.hold()
	plt.show()


while True:
	makeFields(MAX_NUM_FIELDS, ARENA_SIZE_IN_METERS)
