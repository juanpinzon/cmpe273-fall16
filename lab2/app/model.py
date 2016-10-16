from datetime import datetime, time
from address import AddressParser, Address
import re

class CrimeReport(object):
	crimes = []
	total_crime = 0
	dangerous_streets = {}
	the_most_dangerous_streets = []
	crime_type_count = {}
	event_time_count = {"12:01am-3am" : 0,
       					"3:01am-6am" : 0,
    					"6:01am-9am" : 0,
    					"9:01am-12noon" : 0,
    					"12:01pm-3pm" : 0,
    					"3:01pm-6pm" : 0,
    					"6:01pm-9pm" : 0,
    					"9:01pm-12midnight" : 0
    					}

	def __init__(self, json_data):
		self.crimes = json_data['crimes']
		#Reset dictionaries
		self.crime_type_count = {}
		self.event_time_count.update((k, 0) for k,v in self.event_time_count.iteritems())
		self.process_data()

	def process_data(self):		
		self.total_crime = len(self.crimes)		
		for record in self.crimes:
			self.increment_crime(record["type"])
			date_time = record["date"].split(' ')
			self.increment_time(date_time[1], date_time[2])
			self.increment_dangerous_streets(record["address"])

		#Reverse sort dictionary dangerous_streets by value, then get first 3 elements
		sorted_dangerous_streets_list = sorted(self.dangerous_streets, key=lambda x: self.dangerous_streets[x], reverse=True)		
		self.the_most_dangerous_streets = sorted_dangerous_streets_list[:3]


	def increment_crime(self, crime_type):
		if crime_type in self.crime_type_count:
			self.crime_type_count[crime_type] += 1
		else:
			self.crime_type_count[crime_type] = 1


	def increment_time(self, my_time, my_am_pm):		
		time_am_pm = my_time + " " + my_am_pm
		crime_time = datetime.strptime(time_am_pm, '%I:%M %p')

		#Check time ranges			
		if datetime.strptime("00:01", "%H:%M") <= crime_time <= datetime.strptime("03:00", "%H:%M"):
			self.event_time_count["12:01am-3am"] += 1			
		if datetime.strptime("03:01", "%H:%M") <= crime_time <= datetime.strptime("06:00", "%H:%M"):		
			self.event_time_count["3:01am-6am"] += 1			
		if datetime.strptime("06:01", "%H:%M") <= crime_time <= datetime.strptime("09:00", "%H:%M"):
			self.event_time_count["6:01am-9am"] += 1		
		if datetime.strptime("09:01", "%H:%M") <= crime_time <= datetime.strptime("12:00", "%H:%M"):
			self.event_time_count["9:01am-12noon"] += 1
		if datetime.strptime("12:01", "%H:%M") <= crime_time <= datetime.strptime("15:00", "%H:%M"):					
			self.event_time_count["12:01pm-3pm"] += 1
		if datetime.strptime("15:01", "%H:%M") <= crime_time <= datetime.strptime("18:00", "%H:%M"):
			self.event_time_count["3:01pm-6pm"] += 1
		if datetime.strptime("18:01", "%H:%M") <= crime_time <= datetime.strptime("21:00", "%H:%M"):		
			self.event_time_count["6:01pm-9pm"] += 1
		if datetime.strptime("21:01", "%H:%M") <= crime_time <= datetime.strptime("23:59", "%H:%M") or crime_time == datetime.strptime("00:00", "%H:%M"):
			self.event_time_count["9:01pm-12midnight"] += 1


	def increment_dangerous_streets(self, input_address):
		ap = AddressParser()
		address = ap.parse_address(input_address)
		street = ""
		if address.street_prefix is not None:
			pre = str(address.street_prefix)
			pre = pre[:-1]
			street =  pre + " "
		if address.street is not None:
			street = street + str(address.street) + " "
		if address.street_suffix is not None:
			su = str(address.street_suffix)
			su = su[:-1]
			street = street + su
		
		#another way to process the input data--> just getting rid of the numbers at the beginning
		#street = input_address.lstrip('0123456789.- ')	  
		if street in self.dangerous_streets:
			self.dangerous_streets[street] += 1
		else:
			self.dangerous_streets[street] = 1