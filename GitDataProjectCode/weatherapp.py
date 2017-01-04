#!/usr/local/bin/python
import urllib2
import json
import pprint

print "Content-Type: text/plain\r\n"

#page = urllib2.urlopen("https://api.forecast.io/forecast/d989f66c759772b206474e32a33748d0/42.472933,-71.6149959").read()
page = open('cached.txt', 'r').read()
data = json.loads(page)

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(data)

#TODO: Change timezone offset for daylight savings
timezone_offset = -4

# number of hours since 1970 for the first time in the result
base_hse_et = (data["hourly"]["data"][0]["time"] / 3600) + timezone_offset

#TODO: Compute min, max, and precipitation
invalid_number = 70000
min_temp = invalid_number
max_temp = -invalid_number
max_precip_intensity = 0

for this_hour in data["hourly"]["data"]:
	#print this_hour["time"]
	hours_since_epoch = this_hour["time"] / 3600
	hse_et = hours_since_epoch + timezone_offset # convert to eastern timezone
	hour_of_day = hse_et % 24
	hours_since_base = hse_et - base_hse_et
	# we only care about times between 0700 and 1600 local timezone, and within 24 hours from now
	if hour_of_day >= 7 and hour_of_day <= 16 and hours_since_base < 24:
		temp = this_hour["apparentTemperature"]
		precip_intensity = this_hour["precipIntensity"]
		
		if temp < min_temp:
			min_temp = temp
		if temp > max_temp:
			max_temp = temp
		if precip_intensity > max_precip_intensity:
			max_precip_intensity = precip_intensity
		#print this_hour["time"], hours_since_epoch, hse_et, hour_of_day, hours_since_base

#print "min_temp: ", min_temp
#print "max_temp: ", max_temp
#print "max_precip_intensity: ", max_precip_intensity

#handle all the temperature cases
msg = ""
if max_temp < 40:
	msg = "Wear a heavy cost & scarf & gloves"
elif min_temp < 40:
	msg = "Wear a coat and pants"
elif max_temp < 60:
	msg = "Wear pants & a jacket"
elif max_temp > 80:
	msg = "Wear shorts and bring water"
elif max_temp > 75:
	msg = "Wear shorts & a T-shirt"
elif min_temp < 55:
	msg = "Wear a sweatshirt & pants"
elif min_temp < 65:
	msg = "Wear a sweatshirt & pants or shorts"
else:
	msg = "Wear shorts & a T-shirt"

#handle precipitation
precip_type = "None"
if max_precip_intensity >= 0.017:
	if min_temp > 40:
		precip_type = "Rain"
		msg = msg + ". Also, bring an umbrella"
	else:
		precip_type = "Snow"
		msg = msg + ". Also, be ready for snow"

#print "msg: ", msg
#print msg


#print "Low: ", int(min_temp), "  High: ", int(max_temp), "  Precipitation: ", precip_type, "  Clothes: ", msg

#print "Low,High,Precipitation,Clothes\r\n";
#print int(min_temp), ",", int(max_temp), ",", precip_type, ",", msg
		
print "<h2>Low: ", int(min_temp), "<br>  High: ", int(max_temp), "<br>  Precipitation: ", precip_type, "<br>  Clothes: ", msg		
		
#A very rough guide is that a value of 
#0 in./hr. corresponds to no precipitation, 
#0.002 in./hr. corresponds to very light precipitation, 
#0.017 in./hr. corresponds to light precipitation, 
#0.1 in./hr. corresponds to moderate precipitation, and 
#0.4 in./hr. corresponds to heavy precipitation.
	
	
	