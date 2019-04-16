#!/usr/bin/env python3

import astropy.units as u
import datetime
from matplotlib import pyplot as plt
import numpy as np
import os
from scipy import ndimage
import shutil
import sunpy.map
from sunpy.net import attrs
from sunpy.net import Fido
import sys

################################################################################

# the directory in which downloaded images have been saved
dldir = 'downloaded/'

################################################################################

def count_bright_regions(fits_image):
	'''
	Process the image provided.
	Hard-threshold the image pixels to determine the brightest pixels.
	These pixels will not form a continuous region.
	Hence, perform Gaussian filtering on the image.
	Count the number of continuous bright regions.

	Args:
		fits_image: string which is the name of a file of MIME type image/fits

	Returns:
		None
	'''

	# there is a tendency to stop because of KeyError
	# hence this block
	try:

		# read original image and find a mask for the dark pixels
		img = sunpy.map.Map(fits_image).data
		mask = img < 2000

		# filter the image so that bright regions are continuous
		# count the number of these bright regions
		smooth_img = ndimage.gaussian_filter(img * ~mask, 16)
		labels, n = ndimage.label(smooth_img)

		return n

	except:
		return np.nan

	# display the plots of the above three if required
	# to do so, just comment out the above 'return' statemtent
	fig = plt.figure()
	fig.canvas.set_window_title('Solar Image Analysis')
	axes = [fig.add_subplot(1, 3, i) for i in range(1, 4)]

	# plot one image on each
	axes[0].imshow(img, cmap = 'gray')
	axes[0].set_title('Original Image')
	axes[1].imshow(mask, cmap = 'gray')
	axes[1].set_title('Bright Pixels')
	axes[2].imshow(smooth_img, cmap = 'gray')
	axes[2].set_title('Bright Regions')

	# hide the pixel numbers
	for i in range(3):
		axes[i].set_xticks([])
		axes[i].set_yticks([])

	# display the images
	plt.show()

	return n

################################################################################

if __name__ == '__main__':

	with open('training.dat', 'a') as data_file:
		for fits_img in sorted(os.listdir(dldir)):
			print('{} {}'.format(fits_img, count_bright_regions(dldir + fits_img)), file = data_file)
			data_file.flush()

