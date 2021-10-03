#!/usr/bin/env python


"""IS 211 Week 2 Assignment"""

import urllib2
import csv
import datetime
import logging
import argparse
import sys

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("--url")
	args = parser.parse_args()
	url = args.url

	logger = logging.getLogger("assignment2")
	logger.setLevel(logging.ERROR)
	fh = logging.FileHandler('error.log')
	fh.setLevel(logging.ERROR)
	logger.addHandler(fh)

	format = "%d/%m/%Y"
	
	if url is None:
		sys.exit()
	else:

		def downloaddata(url):
			try:
				request = urllib2.urlopen(url)
			except:
				print "Download data error, check URL and try again"
				sys.exit()
			return request



		def processdata(data):
			readerdata = csv.reader(data)

			dictionary = {}
			line = 1
			birthday = datetime.datetime.strptime('04/13/2014',format)

			for row in readerdata:
				if(row[0] == 'id'):
					line += 1
				else:
					id = int(row[0])
					name = row[1]
					try:
						birthday = datetime.datetime.strptime(row[2],format)
					except:
						logger.error("ERROR:assignment2:Error processing line #%d for ID #%d", line, id)
						
					dictionary[id] = (name,birthday)
					
					line += 1
			return dictionary
		


		def displayPerson(id):
			try:
				print "Person #%d is %s with a birthday of %s" % (id, personData[id][0], datetime.datetime.strftime(personData[id][1],format))
			except:
				print "Display person error, retry ID number"
		
		csvData = downloaddata(url)
		personData = processdata(csvData)
		while(1):
			print "Enter ID?",
			id = raw_input()
			try:
				id = int(id)
			except:
				print "Please Enter a Number"
				continue
			if id <= 0:
				print "Input <= 0, Exiting Program"
				break
			else:
				displayPerson(id)

		
main()
