#!/usr/bin/env python


"""IS 211 Week 2 Assignment"""

import argparse
import datetime
import logging
import shutil
import sys
import tempfile
import urllib.request


def downloadData(url):
    with urllib.request.urlopen(url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
    return tmp_file.name


def processData(birthdayfile):
    birthdict = dict()
    with open(birthdayfile) as csvfile:
        for i, line in enumerate(csvfile):
            line = line.strip().split(',')
            try:
                birthdict[line[0]] = (line[1], datetime.datetime.strptime(line[2], "%d/%m/%Y").date())
            except:
                logging.error('Error processing line #{0} for ID #{1}'.format(i + 1, line[0]))
    return birthdict


def displayPerson(id, personData):
    print(personData.get(str(id), "No user with the id located"))


def assignment2():
    logging.basicConfig(filename='error.log', level=logging.ERROR, filemode='w')


def main():
    #parser = argparse.ArgumentParser()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")
    
    parser.add_argument("--url url", help='The url you wish to use to find the birthday csv file', type=str)
    args = parser.parse_args()
    assignment2()  # function for initializing logger
    try:
        csvData = downloadData(args.url)
    except:
        logging.critical('{0}:  unable to resolve URL {1}'.format(sys.exc_info(), args.url))
        print('An error has occurred, Please see error log.')
        exit()
    try:
        csvData = processData(csvData)
    except:
        logging.critical('{0}:  Unresolvable processing error with file {1}'.format(sys.exc_info(), csvData))
        print('An error has occurred, Please see error log.')
        exit()

    while True:
        idlookup = int(input("Please enter a ID to lookup, or type 0 or a negative number to quit: "))
        displayPerson(idlookup, csvData) if idlookup > 0 else exit()


main()
