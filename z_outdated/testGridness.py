from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from skimage import data, img_as_float

def hardThresholdField(img, THRESHOLD):
    for row in range(img.shape[0]):
        for column in range(img.shape[1]):
            if img[row,column] < THRESHOLD:
                img[row,column] = 0
    return img

## exclude nans
test = autocorr
test = test[:,~np.all(np.isnan(test), axis=0)]
test = test[~np.all(np.isnan(test), axis=1),:]

autocorr = test


THRESHOLD = 0.1 ## pg 4 of Sargolini
autocorr_thresh = hardThresholdField(autocorr, THRESHOLD)

plt.figure()
ax = sns.heatmap(autocorr_thresh)
plt.axis('equal')
ax.plot()


#### get peaks (from http://scikit-image.org/docs/dev/auto_examples/segmentation/plot_peak_local_max.html)
im = autocorr_thresh

im_neg = 1 - im 



# Comparison between image_max and im to find the coordinates of local maxima
coordinates = peak_local_max(im_neg, min_distance=1, threshold_abs = THRESHOLD, exclude_border = False)



# display results
fig, axes = plt.subplots(1, 3, figsize=(8, 3), sharex=True, sharey=True)
ax = axes.ravel()
ax[0].imshow(im, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('Original')

ax[1].imshow(image_max, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('Maximum filter')

ax[2].imshow(im, cmap=plt.cm.gray)
ax[2].autoscale(False)
ax[2].plot(coordinates[:, 1], coordinates[:, 0], 'r.')
ax[2].axis('off')
ax[2].set_title('Peak local max')

fig.tight_layout()

plt.show()



