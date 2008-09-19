
import subprocess
import re
import time

class PrayerTime:

	def __init__(self, latitude, longitude, utc, method=5):
		self.latitude = latitude
		self.longitude = longitude
		self.utc = utc
		self.method = method

	def get_prayer_time(self):

		cmd = "ipraytime --latitude %f --longitude %f -a %d --utcdiff %d" % (self.latitude, self.longitude, self.method, self.utc)
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

		today = time.strftime("%d-%m-%Y")
		pattern = "\s+\[%s\]\s+.+" % today

		time_line = None
		for line in p.stdout:
			if re.match(pattern, line):
				time_line = line
				break
		
		if time_line:
			(date, subuh, fajar, dzuhur, ashar, maghrib, isya) = re.split(u'\s+', time_line.strip())
			return (subuh, fajar, dzuhur, ashar, maghrib, isya)

		else:
			return None

