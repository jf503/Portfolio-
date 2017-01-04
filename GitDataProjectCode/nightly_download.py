#!/usr/local/bin/python
import urllib2
import json
import pprint

page = urllib2.urlopen("https://api.darksky.net/forecast/d989f66c759772b206474e32a33748d0/42.472933,-71.6149959").read()
print page
