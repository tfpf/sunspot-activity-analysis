#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
#import scipy
################################################################################

def create_window(n):
	'''
	Create a sampling window.

	Args:
		n: odd positive integer

	Returns:
		array with maximum value in the middle and small elements towards the end
	'''

	# check if 'n' is odd
	if n % 2 == 0 or n < 0:
		raise ValueError('Only odd-length windows can be created.')

	centre = (n - 1) / 2
	window = [(n - np.abs(i - centre)) / n ** 2 for i in range(n)]

	return window


################################################################################

def moving_correlation(big, small, centre):
	'''
	Calculate the correlation of a window sequence with a chunk of a big sequence.

	Args:
		big: main sequence
		small: window sequence
		centre: int indicating where to overlap 'small' with 'big'
	'''

	window_size = len(small)

	# slice 'big' to obtain a sequence as long as 'small'
	# where to slice it depends on 'centre'
	# slice it in such a way that 'big[centre]' is the middle element of 'arr'
	arr = big[centre - (window_size - 1) // 2 : centre + (window_size - 1) // 2 + 1]

	# correlate them
	return np.dot(arr, small)

################################################################################

if __name__ == '__main__':

	with open('status', 'w') as status_file:
		print('Last Run: {}'.format(sys.argv), file = status_file)
		print('Arguments: {}'.format(len(sys.argv)), file = status_file)

	# plot the training data

	# set up the starting date and the activity numbers
	current_date = datetime.date(2005, 1, 1)
	activity = []

	# read the file for activity numbers by date
	with open('bright_patches.dat') as data_file:
		for line in data_file:

			# each line begins with a string containing the date
			# read the line and find out what the date is
			y = int(line[3 : 7])
			m = int(line[7 : 9])
			d = int(line[9 : 11])

			# some dates are missing in 'data_file'
			# so, keep incrementing 'current_date' until a mathc is found
			while current_date != datetime.date(y, m, d):
				current_date += datetime.timedelta(days = 1)
				activity.append(0)

			# some dates have an invalid number next to them
			# for those, use 'np.nan'
			try:
				activity.append(int(line[19 :].strip()))
			except ValueError:
				activity.append(0)

			current_date += datetime.timedelta(days = 1)

	# create a window to correlate
	window_size = 31
	gaussian_window = create_window(window_size)

	# to make correlation calculation easy, place 365 zeros in front of 'activity'
	spots = np.concatenate([np.zeros(365), activity])

	# find the shift from 1st January which gives the best correlation
	best_correlation = 0
	best_prediction = -100

	# 'prediction' is the shift from 1st January
	# it indicates the shift 'gaussian_window' must be given before correlating
	# for each shift, calculate the weighted average of of the correlation with each major spike
	# the best shift will have the greatest weighted average
	for prediction in range(-100, 100):
		correlation = np.average([moving_correlation(spots, gaussian_window, i + prediction) for i in [365, 1085, 1450, 1826]] , axis = None, weights= [0.1,0.2,0.3,0.4])
		if correlation > best_correlation:
			best_correlation = correlation
			best_prediction = prediction
	print('Predicted day for first spike '+str(best_prediction))

	# predict the second spike
	# the minor spikes seem to be linear
	# the gaps betwen them are approximately constant
	# hence, use linear polynomial interpolation
	# first, locate all these minor spikes
	someday = []
	i = 100
	while i < len(activity):
		if 20 <= activity[i] <= 30:
			someday.append(i)
			i += 300
		i += 1

	# find the linear polynomial which best fits these points
	coeffs = np.polyfit(range(5),someday,1)

	# evaluate the polynomial at the next point
	# that is the predicted location of the next spike
	predicted = int(np.polyval(coeffs,5)-1826)
	print('Predicted day for second spike '+str(predicted))

	# open a window to plot the training data
	plt.style.use('classic')
	fig = plt.figure()
	fig.canvas.set_window_title('Variation of Solar Activity')
	ax = fig.add_subplot(1, 1, 1)
	ax.axhline(linewidth = 1.6, color = 'k')
	ax.axvline(linewidth = 1.6, color = 'k')
	ax.plot(activity, 'r-', label = 'number of bright solar regions')
	with open('status', 'a') as status_file:
		print('training data: {}'.format(len(activity)), file = status_file)

	# beautification
	ax.grid(True, linewidth = 0.4)
	ax.legend()
	ax.set_xlabel('time')
	ax.set_xlim(0, 1826)
	ax.set_xticks([0, 365, 720, 1085, 1451])
	# ax.set_xticklabels(['2005', '2006', '2007', '2008', '2009'])
	ax.set_ylabel('solar activity')
	ax.set_ylim(0, 80)
	ax.set_title('Variation of Solar Activity, 2005 to 2009')

	# plt.show()

	########################################

	# plot the testing data

	# set up the starting date and the activity numbers
	current_date = datetime.date(2010, 1, 1)
	activity = []

	# read the file for activity numbers by date
	with open('training.dat') as data_file:
		for line in data_file:

			# each line begins with a string containing the date
			# read the line and find out what the date is
			y = int(line[3 : 7])
			m = int(line[7 : 9])
			d = int(line[9 : 11])

			# some dates are missing in 'data_file'
			# so, keep incrementing 'current_date' until a mathc is found
			while current_date != datetime.date(y, m, d):
				current_date += datetime.timedelta(days = 1)
				activity.append(np.nan)

			# some dates have an invalid number next to them
			# for those, use 'np.nan'
			try:
				activity.append(int(line[19 :].strip()))
			except ValueError:
				activity.append(np.nan)

			current_date += datetime.timedelta(days = 1)

	# open a window to plot the testing data
	plt.style.use('classic')
	fig = plt.figure()
	fig.canvas.set_window_title('Variation of Solar Activity')
	ax = fig.add_subplot(1, 1, 1)
	ax.axhline(linewidth = 1.6, color = 'k')
	ax.axvline(linewidth = 1.6, color = 'k')
	ax.plot(activity, 'r-', label = 'number of bright solar regions')
	with open('status', 'a') as status_file:
		print('testing data: {}'.format(len(activity)), file = status_file)

	# beautification
	ax.grid(True, linewidth = 0.4)
	ax.legend()
	ax.set_xlabel('time')
	ax.set_xlim(0, 243)
	ax.set_xticks([0, 31, 59, 90, 120, 151, 181, 212, 243])
	# ax.set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'])
	ax.set_ylabel('solar activity')
	ax.set_ylim(0, 80)
	ax.set_title('Variation of Solar Activity, 2010')

	plt.show()


	# open a window to plot the testing data

