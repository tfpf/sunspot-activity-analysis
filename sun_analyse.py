#!/usr/bin/env python3

import astropy.units as u
import datetime
from sunpy.net import attrs
from sunpy.net import Fido

################################################################################

def sun_data_request(start_time, end_time):
	'''
	Download all SOHO/EIT data recorded in the given time interval.
	Save the downloaded images in the working directory.

	Args:
		start_time: start of aforementioned interval
		end_time: end of aforementioned interval

	Returns:
		None
	'''

	# read the time interval
	interval = attrs.Time(start_time, end_time)

	# query the data in the interval
	# download the images to the current directory
	result = Fido.search(interval, attrs.Instrument('eit'))
	Fido.fetch(result, path = 'downloaded/')

################################################################################

if __name__ == '__main__':

	the_date = datetime.date(2005, 1, 1)
	number_of_days = 10
	for i in range(number_of_days):
		start_time = str(the_date) + ' 00:10'
		end_time = str(the_date) + ' 00:15'
		sun_data_request(start_time, end_time)
		the_date += datetime.timedelta(days = 1)

	# start and end times between which data will be requested
	# start = '2005/01/01 00:10'
	# end = '2005/01/01 00:10'
	# attrs_time = attrs.Time('2005/01/01 00:10', '2005/01/01 00:40')
	# result = Fido.search(attrs_time, attrs.Instrument('eit'))
	# downloaded_files = Fido.fetch(result, path='/home/tfpf/Documents/projects/sunspot-activity-analysis/downloaded/')

