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

# the directory in which downloaded images will be saved
dldir = 'downloaded/'

################################################################################

def sun_data_request(start_time, end_time):
	'''
	Download all SOHO/EIT data recorded in the given time interval.
	Save the downloaded images in the working directory.
	Data is stored at intervals of 12 minutes. Hence, straddle a 12-minute mark for each file you need.
	For instance, use the following
		start_time = '2005-01-01 00:10'
		end_time = '2005-01-01 01:10'
	to get 5 images captured at 00:12, 00:24, 00:36, 00:48 and 01:00 on 1st January 2005.

	Args:
		start_time: string indicating start of time interval
		end_time: string indicating end of time interval

	Returns:
		None
	'''

	# read the time interval
	interval = attrs.Time(start_time, end_time)

	# query the images captured in the time interval
	# download the images to the current directory
	result = Fido.search(interval, attrs.Instrument('eit'))
	Fido.fetch(result, path = dldir)

################################################################################

def download_multiple_images(s_date, number_of_days):
	'''
	Download all SOHO/EIT images for each day in the period specified.

	Args:
		s_date: datetime.date object indicating the date of the first image to download
		number_of_days: number of days for which images have to be downloaded

	Returns:
		None
	'''

	# download the image captured at 00:12 on each day in the period
	for _ in range(number_of_days):
		start_time = str(s_date) + ' 00:10'
		end_time = str(s_date) + ' 00:15'
		sun_data_request(start_time, end_time)
		s_date += datetime.timedelta(days = 1)

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

	# read original image and find a mask for the dark pixels
	img = sunpy.map.Map(fits_image).data
	mask = img < 2000

	# filter the image so that bright regions are continuous
	# count the number of these bright regions
	smooth_img = ndimage.gaussian_filter(img * ~mask, 16)
	labels, n = ndimage.label(smooth_img)

	return n

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

	# check for arguments
	# if the number of days is mentioned, remove the downloaded files (if any)
	# and then download the files the user wants
	try:
		number_of_days = int(sys.argv[1])
		s_date = datetime.date(2005, 1, 1)
		if os.path.exists(dldir) and os.path.isdir(dldir):
			shutil.rmtree(dldir)
		download_multiple_images(s_date, number_of_days)
	except (IndexError, ValueError):
		print('Number of days either not specified or invalid. Using existing data.')


	# find out how many bright regions are present in each image
	n_bright_regions = [count_bright_regions(dldir + file) for file in os.listdir(dldir)]
	print(n_bright_regions)
	'''
	# process each image that has been downloaded
	for file in os.listdir(dldir):

		# read the image
		img = sunpy.map.Map(dldir + file).data
		plt.figure().canvas.set_window_title('Original Image')
		plt.imshow(img, cmap = 'gray')
		plt.show()

		# mask off dark pixels
		mask = img < 2000
		plt.figure().canvas.set_window_title('Bright Pixels')
		plt.imshow(mask, cmap = 'gray')
		plt.show()

		# filter the image to get continuous bright regions
		smooth_img = ndimage.gaussian_filter(img * ~mask, 16)
		plt.figure().canvas.set_window_title('Bright Regions')
		plt.imshow(smooth_img, cmap = 'gray')
		plt.show()

		# count the number of continuous bright regions
		labels, n = ndimage.label(smooth_img)
		print(n)
	'''
