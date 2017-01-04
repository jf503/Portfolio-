#!/usr/bin/python
import csv
import json
import pprint
from collections import Counter
import savReaderWriter

#generic string cleaner
def strclean(s):
	return s.encode('ascii', 'ignore').decode('ascii').replace('\n',' ')

#unicode string cleaner
def ustrclean(s):
	return unicode( s.replace('\n',' ') )
	
#spss title string cleaner
def title_strclean(s):
	return s.encode('ascii', 'ignore').decode('ascii').replace('\n',' ').replace('-','_').replace(' ','_').replace('/','_or_')

#returns whether the passed variable is numeric
def isnumeric(v):
	return isinstance(v, (int, long, float, complex))
	
def isrealstring(s):
	if not isinstance(s, (str, unicode)):
		return false #it's not a string
	if len(str) == 0:
		return false #it's empty
	#looks like it is a string, and it has contents
	return true
	
	
lines = [line.rstrip('\n') for line in open('yelp_academic_dataset_business.json')]
checkin_lines = [line.rstrip('\n') for line in open('yelp_academic_dataset_checkin.json')]

#this was used to investigate the category data, and is not used to create the actual csv
def scan_for_categories():
	catcount = Counter()
	max_cats = 0

	for line in lines:
		data = json.loads(line)
		cats = data["categories"]
		num_cats = len(cats)
		if num_cats > max_cats:
			max_cats = num_cats
		#if "Restaurants" in data["categories"]:# and "Food" in data["categories"]:
		#if "Food" in data["categories"]:
		#if "Restaurants" in cats and ("Food" in cats or "Fast Food" in cats):
		if True:
			catcount.update(data["categories"])

	print catcount
	print len(catcount.keys())

	print "Max cats: ", max_cats

#this was used to investigate the neighborhood data, and is not used to create the actual csv
def scan_for_neighborhoods():
	nhoodcount = Counter()
	max_nhoods = 0

	for line in lines:
		data = json.loads(line)
		nhoods = data["neighborhoods"]
		num_nhoods = len(nhoods)
		if num_nhoods > max_nhoods:
			max_nhoods = num_nhoods
		nhoodcount.update(nhoods)

	print nhoodcount
	print len(nhoodcount.keys())

	print "Max neighborhoods: ", max_nhoods

#this was used to investigate the attribute data, and is not used to create the actual csv
def scan_for_attributes():
	#attribcount = Counter()
	subattribcount = Counter()

	for test_attrib in get_nested_attrib_names():
		print test_attrib, ": "
		for line in lines:
			data = json.loads(line)
			attribs = data["attributes"]
			if test_attrib in attribs:
				subattribcount.update(attribs[test_attrib].keys())
				for subattribname in attribs[test_attrib].keys():
					if subattribcount[subattribname] == 1:
						print ',"%s"' % subattribname,
		
		#attribcount.update(attribs.keys())
		#for attribname in attribs.keys():
		#	if attribcount[attribname] == 1:
		#		if not isinstance( attribs[attribname], dict ):
		#			print ',"%s"' % attribname,
		#			#print attribname, ": ", attribs[attribname] 
			
	print
	
	#print attribcount
	#print len(attribcount.keys())
	#print subattribcount
	#print len(subattribcount.keys())

checkin_totals = {} # key is business_id, value is total number of checkins
def open_checkin_data():
	for line in checkin_lines:
		data = json.loads(line)
		business_id = data["business_id"]
		
		total_checkins = 0
		checkin_info = data["checkin_info"]
		
		for key in checkin_info:
			value = checkin_info[key]
			total_checkins = total_checkins + value
		
		checkin_totals[business_id] = total_checkins

def get_simple_attrib_names():
	simple_attribs = ["Take-out" ,"Drive-Thru" ,"Outdoor Seating" ,"Caters" ,"Noise Level" ,"Delivery" ,"Attire" ,"Has TV" ,"Price Range" ,"Takes Reservations" ,"Waiter Service" ,"Accepts Credit Cards" ,"Good for Kids" ,"Good For Groups" ,"Alcohol" ,"Happy Hour" ,"Good For Dancing" ,"Coat Check" ,"Smoking" ,"Wi-Fi" ,"Wheelchair Accessible" ,"Dogs Allowed" ,"BYOB" ,"Corkage" ,"BYOB/Corkage" ,"Order at Counter" ,"By Appointment Only" ,"Accepts Insurance" ,"Open 24 Hours" ,"Ages Allowed"]
	return simple_attribs
	
def get_nested_attrib_names():
	nested_attribs = ["Dietary Restrictions","Good For","Ambience","Parking" ] #,"Hair Types Specialized In"]
	return nested_attribs
	
def get_subattrib_names(attrib):
	if attrib == "Dietary Restrictions":
		return ["dairy-free" ,"gluten-free" ,"vegan" ,"kosher" ,"halal" ,"soy-free" ,"vegetarian"]
	if attrib == "Good For":
		return ["dessert" ,"latenight" ,"lunch" ,"dinner" ,"breakfast" ,"brunch"]
	if attrib == "Ambience":
		return ["romantic" ,"intimate" ,"classy" ,"hipster" ,"divey" ,"touristy" ,"trendy" ,"upscale" ,"casual"]
	if attrib == "Parking":
		return ["garage" ,"street" ,"validated" ,"lot" ,"valet"]
	if attrib == "Hair Types Specialized In":
		return ["coloring" ,"africanamerican" ,"curly" ,"perms" ,"kids" ,"extensions" ,"asian" ,"straightperms"]
	print "Unknown attrib"
	exit()
	
def create_csv():
	simple_attrib_names = get_simple_attrib_names()

	### CSV header
	
	#for fixed fields
	print '"business_id","city","full_address","latitude","longitude","name","open","review_count","stars","state"',
	#total checkins
	print ',"total checkins"',
	#for categories
	print ',"category1","category2","category3","category4","category5","category6","category7","category8","category9","category10"',
	#for neighborhoods
	print ',"neighborhood1","neighborhood2","neighborhood3"',
	#for simple attributes
	for attrib_name in simple_attrib_names:
		print ',"%s"' % attrib_name,
	#for nested attribs
	for nested_attrib_name in get_nested_attrib_names():
		for subattrib_name in get_subattrib_names(nested_attrib_name):
			print ',"%s %s"' % (nested_attrib_name, subattrib_name),
		
	#final newline
	print

	for line in lines:
		data = json.loads(line)
	
		### Print a single line for a single business
		
		business_id = data["business_id"]
		
		#for fixed fields
		print '"%s","%s","%s",%s,%s,"%s",%s,%s,%s,"%s"' % (
			strclean(data["business_id"]), 
			strclean(data["city"]),
			strclean(data["full_address"]),
			data["latitude"],
			data["longitude"],
			strclean(data["name"]),
			data["open"],
			data["review_count"],
			data["stars"],
			strclean(data["state"])
			),
		
		total_checkins = 0
		if business_id in checkin_totals:
			total_checkins = checkin_totals[business_id]
		print ',"%s"' % str(total_checkins),
			
		#for categories (max number of categories a business has is 10)
		cats = data["categories"]
		for icat in range(10):
			cat = ""
			if icat < len(cats):
				cat = cats[icat]
			print ',"%s"' % strclean(cat),
			
		#for neighborhoods (max number of neighborhoods a business has is 3)
		nhoods = data["neighborhoods"]
		for inhood in range(3):
			nhood = ""
			if inhood < len(nhoods):
				nhood = nhoods[inhood]
			print ',"%s"' % strclean(nhood),
			
		#for simple attributes
		attribs = data["attributes"]
		for attrib_name in simple_attrib_names:
			if attrib_name in attribs:
				print ',"%s"' % strclean(str(attribs[attrib_name])),
			else:
				print ',""',
		
		#for nested attributes
		for nested_attrib_name in get_nested_attrib_names():
			subattribs = {}
			if nested_attrib_name in attribs:
				subattribs = attribs[nested_attrib_name]
		
			for subattrib_name in get_subattrib_names(nested_attrib_name):
				if subattrib_name in subattribs:
					print ',"%s"' % strclean(str(subattribs[subattrib_name])),
				else:
					print ',""',
			
		#final newline
		print
		
		#pprint.pprint(data)
		#exit()

def create_sav(savFileName):
	records = [] #[ [b'Test1', 1, 1], [b'Test2', 2, 1] ]
	varNames = [] #['var1', 'v2', 'v3']
	varTypes = {} #{'var1': 5, 'v2': 0, 'v3': 0}
	
	simple_attrib_names = get_simple_attrib_names()

	#Fixed field names
	varNames.append(u"business_id")
	varNames.append(u"city")
	varNames.append(u"full_address")
	varNames.append(u"latitude")
	varNames.append(u"longitude")
	varNames.append(u"name")
	varNames.append(u"open")
	varNames.append(u"review_count")
	varNames.append(u"stars")
	varNames.append(u"state")

	#total checkins
	varNames.append(u"total_checkins")
	
	#for simple attributes
	for attrib_name in simple_attrib_names:
		varNames.append( title_strclean( attrib_name ) )
	#for nested attribs
	for nested_attrib_name in get_nested_attrib_names():
		for subattrib_name in get_subattrib_names(nested_attrib_name):
			varNames.append( title_strclean( "%s_%s" % (nested_attrib_name, subattrib_name) ) )

	#for categories
	varNames.extend( [ u"category1",u"category2",u"category3",u"category4",u"category5",u"category6",u"category7",u"category8",u"category9",u"category10" ] )
	#for neighborhoods
	varNames.extend( [ u"neighborhood1",u"neighborhood2",u"neighborhood3" ] )
		
	for line in lines:
		data = json.loads(line)
	
		### Create a single record for a single business
		
		business_id = data["business_id"]
		
		record = []
		record.append( ustrclean(data["business_id"]) )
		record.append( ustrclean(data["city"]) )
		record.append( ustrclean(data["full_address"]) )
		record.append( data["latitude"] )
		record.append( data["longitude"] )
		record.append( ustrclean(data["name"]) )
		record.append( data["open"] )
		record.append( data["review_count"] )
		record.append( data["stars"] )
		record.append( ustrclean(data["state"]) )

		total_checkins = 0
		if business_id in checkin_totals:
			total_checkins = checkin_totals[business_id]
		record.append( total_checkins )
						
		#for simple attributes
		attribs = data["attributes"]
		for attrib_name in simple_attrib_names:
			if not (attrib_name in attribs):
				record.append( "" )
				continue
				
			attrib = attribs[attrib_name]
			if isnumeric( attrib ):					
				record.append( attrib )
			else:
				record.append( ustrclean(attrib) )

		#for nested attributes
		for nested_attrib_name in get_nested_attrib_names():
			subattribs = {}
			if nested_attrib_name in attribs:
				subattribs = attribs[nested_attrib_name]
		
			for subattrib_name in get_subattrib_names(nested_attrib_name):
				if not subattrib_name in subattribs:
					record.append( "" )
					continue

				subattrib = subattribs[subattrib_name]
				if isnumeric( subattrib ):
					record.append( subattrib )
				else:
					record.append( ustrclean( subattrib) )
		
		#for categories (max number of categories a business has is 10)
		cats = data["categories"]
		for icat in range(10):
			cat = ""
			if icat < len(cats):
				cat = cats[icat]
			record.append( ustrclean(cat) )
			
		#for neighborhoods (max number of neighborhoods a business has is 3)
		nhoods = data["neighborhoods"]
		for inhood in range(3):
			nhood = ""
			if inhood < len(nhoods):
				nhood = nhoods[inhood]
			record.append( ustrclean(nhood) )
		
		#Append the record to the list of records
		
		records.append( record )
	
	#find column types
	for column in range(len(varNames)):
		#type=0 means numeric
		#otherwise type = max length of string
		type = 0
		max_str_len = 0
		for record in records:
			#check if the column is actually numeric
			if isnumeric(record[column]):
				type = 0
				max_str_len = 0
				break
		
			#keep looking for max string length
			str_len = len(record[column])
			if str_len > max_str_len:
				max_str_len = str_len
			
		type = max_str_len
		
		#add to dictionary
		varTypes[ varNames[ column ] ] = type

	print "varNames"
	pprint.pprint(varNames)
	print "varTypes"
	pprint.pprint(varTypes)

	# write out the data		
	with savReaderWriter.SavWriter(savFileName, varNames, varTypes, ioUtf8=True) as writer:
		for record in records:
			writer.writerow(record)

#run main function

#these are for investigating the data while deciding how to flatten
#scan_for_categories()
#scan_for_neighborhoods()
#scan_for_attributes()

#this opens the checkins data
open_checkin_data()

#this actually creates the csv
#create_csv()

#this creates the spss sav
create_sav("business_data_test.sav")
