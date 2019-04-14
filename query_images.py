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

if __name__ == '__main__':

	# check arguments
	if(len(sys.argv)) < 2:
		print('usage:')
		print('\t./query_images.py <number of images to download>')
		raise SystemExit

	# read the number of images
	try:
		number_of_days = int(sys.argv[1])
	except ValueError:
		print('Invalid number of images specified.')
		raise SystemExit

	# starting date from when images have to be downloaded
	s_date = datetime.date(2007, 12, 31)
	download_multiple_images(s_date, number_of_days)

