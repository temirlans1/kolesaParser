# Parsing of kolesa.kz made by Smagulov Temirlan
# All of the parsed data is sorted by cities
# User can manipulate the range of parsing pages

import requests
from bs4 import BeautifulSoup
import json
import os
import sys

totalObjects = {}

# provide URL that needs to be parsed
def parseFromUrl(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'lxml')

  # all car detailes are enclosed in the div with id 'results'
  results = soup.find(id='results')
  cars = results.find_all('script', type='text/javascript')

  # there is a javascript script starting with "listing.items.push" which contains json object of the car
  validationString = "listing.items.push"

  for car in cars:
    temp = str(car)
    if validationString in temp:
      # extracting json object and appending it to the dictionary
      jsonString = temp[temp.find("{"):temp.rfind("}")+1]
      jsonObject = json.loads(jsonString)
      if jsonObject['city'] not in totalObjects:
        totalObjects[jsonObject['city']] = []
      totalObjects[jsonObject['city']].append(jsonObject)

# write all of the data into json files with appropriate filenames
def writeToFile():
  for data in totalObjects:
    filename = data + '.json'
    with open('./cities/' + filename, 'a') as outfile:
      json.dump(totalObjects[data], outfile, ensure_ascii=False, sort_keys=True, indent=4)

  outfile.close()

# parse from the provided range of pages (finish excluded)
def getFromPageRange(start, finish):
  URL = 'https://kolesa.kz/cars/?page='
  for i in range(start, finish):
    parseFromUrl(URL + str(i))
  
  writeToFile()
  

def main():
  if not os.path.exists('cities'):
    os.makedirs('cities')

  # change these variables in order to manipulate parsing range
  start = 1
  finish = 10
  getFromPageRange(start, finish)

if __name__ == '__main__':
  main()