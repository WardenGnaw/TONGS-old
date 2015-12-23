import sys
from bs4 import BeautifulSoup
import requests
import argparse
from amazonproduct import API
api = API(locale='us')

"""
Retrieves the html content of Amazon product given the ASIN.

param(asin): The Amazon Standard Identification Number to get the product page of
type(asin): string

returns: empty string if failed to get content or
         html of the product page
rtype: string
"""
def getSourcePageData(asin):
   # Create URL to the product page given ASIN
   url = "http://www.amazon.com/gp/product/" + asin

   # Make request and get the response
   response = requests.get(url)

   # Return content if the response code is good ( https://http.cat/200 )
   if int(response.status_code) == 200:
      return response.content
   # Return empty string if failed
   else:
      return ""

"""
Converts a html string into JSON strings

param(htmlData):
type(htmlData):

returns:
rtype:
"""
def getProductFeatureDataFromHTML(htmlData):
   bs = BeautifulSoup(htmlData, 'html.parser')
   wfbc = bs.find('div', {'id' : 'wayfinding-breadcrumbs_feature_div'})
   for i in wfbc.findAll('a'):
      print i.text.strip()

def getInfo(retryMax = 5):
   retry = True 
   retryCount = 0
   while(retry and retryCount < retryMax):
      try:
         data = getSourcePageData("B00OVBXJ5M")
         getProductFeatureDataFromHTML(data)
         retry = False
      except AttributeError:
         retryCount = retryCount + 1
         continue

"""
returns: tuple of 2 lists containing the known arguments and unknown arguments 
rtype: tuple of a map and a list of strings
"""
def parse_args():
   parser = argparse.ArgumentParser(description="Scraping Amazon Products for Features")
    
   results, unknown = parser.parse_known_args()
   return results, unknown

def main():
   results, unknown = parse_args()
   
   getInfo() 
   return 0

"""
Python Main
"""
if __name__ == "__main__":   
   sys.exit(main())
