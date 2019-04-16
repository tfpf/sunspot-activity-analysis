#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys

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
				activity.append(np.nan)

			# some dates have an invalid number next to them
			# for those, use 'np.nan'
			try:
				activity.append(int(line[19 :].strip()))
			except ValueError:
				activity.append(np.nan)

			current_date += datetime.timedelta(days = 1)

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

