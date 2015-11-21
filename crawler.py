import sys
import re

from bs4 import BeautifulSoup
import urllib2
import requests
import json

from datetime import datetime
from selenium import webdriver
import time
import argparse
from random import randint


class Review:
    def __init__(self, title, reviewText, author, reviewDate, reviewComments, stars, helpfulVotes):
        self.title = title
        self.reviewText = reviewText
        self.author = author
        self.reviewDate = reviewDate
        self.reviewComments = reviewComments
        self.stars = stars
        self.helpfulVotes = helpfulVotes

    def __str__(self):
       return json.dumps(self.__dict__)

class ReviewComments:
    def __init__(self, author, reviewText, reviewDate):
        self.author = author
        self.reviewText = reviewText
        self.reviewDate = datetime.strptime(reviewDate[3:], "%b %d, %Y").isoformat()

def getNumStars(review):
     if (review.find('i', {"class" : "review-rating", "class" : "a-star-0"})):
         return 0
     if (review.find('i', {"class" : "review-rating", "class" : "a-star-1"})):
         return 1
     if (review.find('i', {"class" : "review-rating", "class" : "a-star-2"})):
         return 2
     if (review.find('i', {"class" : "review-rating", "class" : "a-star-3"})):
         return 3
     if (review.find('i', {"class" : "review-rating", "class" : "a-star-4"})):
         return 4
     if (review.find('i', {"class" : "review-rating", "class" : "a-star-5"})):
         return 5

def getHelpfulVotes(review):
   votes = review.find('span', {"class" : "review-votes"})
   if (votes):
       votes_ = votes.text.split(' ')
       return {'num_helpful': int(votes_[0]), 'num_total': int(votes_[2]), 'pct_helpful': float(votes_[0])/int(votes_[2])}
   else:
       return {'num_helpful': None, 'num_total': None, 'pct_helpful': None}

def getReviewComments(reviewComments):
   # TODO: Do something meaningful with sub comments
   ret = []
   print reviewComments
   """
   for comment in reviewComments.findAll('div', {"class" : "review-comment"}):
       print "COMMENT FOUND"
       print comment
   """
def getProductReviews(asin, subcomments, pageLimit):
   reviews = None

   # Get the first review page for product
   url = "http://www.amazon.com/product-reviews/" + str(asin) + "/?showViewpoints=0&sortBy=byRankDescending&pageNumber=1"

   browser=webdriver.Firefox()
   browser.get(url)
   if subcomments:
       for link in browser.find_elements_by_xpath("//a[contains(concat(' ',normalize-space(@class),' '),' a-link-expander ')]"):
          link.click()
          time.sleep(5)

   # TODO: More review comments button... Need to fix this.
   # Only currently getting the top subcomments per comment
   """
   while True:
       data = browser.find_elements_by_xpath("//span[contains(concat(' ',normalize-space(@class),' '),' more-comments-button ')]")
       if not data:
           break
       else:
           for link in data:
               link.click()
   """

   reviews = []
   bs = BeautifulSoup(browser.page_source)
   maxPageNum = 0

   # Find number of review pages
   for x in bs.findAll('li', {"class" : "page-button"}):

      #Remove ugly commas in page numbers e.g. 1,000
      pageNum = int(x.text.replace(',', ''))

      if maxPageNum < pageNum:
        maxPageNum = pageNum

   #Loop through all the review pages and get the reviews
   idx = 1
   while (idx < (maxPageNum + 1) and idx < pageLimit):
      for x in bs.findAll('div', {"class" : "review"}):
          review = Review(x.find('a', {"class" : "review-title"}).text.encode('utf-8'),
                         x.find('span', {"class" : "review-text"}).text.encode('utf-8'),
                         x.find('a', {"class" : "author"}).text.encode('utf-8'),
                         x.find('span', {"class" : "review-date"}).text.encode('utf-8'),
                         None,
                         getNumStars(x),
                         getHelpfulVotes(x))
          reviews.append(review)

      url = "http://www.amazon.com/product-reviews/" + str(asin) + "/?showViewpoints=0&sortBy=byRankDescending&pageNumber=" + str(idx)
      browser.get(url)
      if subcomments:
          for link in browser.find_elements_by_xpath("//a[contains(concat(' ',normalize-space(@class),' '),' a-link-expander ')]"):
             link.click()
             # Wait between 5 to 20 seconds between clicks
             time.sleep(randint(5, 20))
      bs = BeautifulSoup(browser.page_source)
      idx += 1
      # Wait 30 to 90 seconds per review page
      time.sleep(randint(30, 90))

   browser.close()

   return reviews

def main():
   parser = argparse.ArgumentParser(description='Scraping Amazon Reviews\nNOTE: Slow because we do not want to spam Amazon.com')
   parser.add_argument('-f', action="store", dest="filename", help="Read ASINS from a file")
   parser.add_argument('-o', action="store", dest="output", help="Output results to a file")
   parser.add_argument('-subcomments', action="store_true", default=False, dest="subcomments", help="Enable reading comment's comments")
   parser.add_argument('-asins', action='append', default=[], dest='asins', help="List of asins to scrape")
   parser.add_argument('-n', action='store', default=5, dest='numPages', help="Number of pages to read (default 5)")

   results, unknown = parser.parse_known_args()

   list_reviews = []
   if results.filename:
      print "NOT IMPLEMENTED YET"
   elif results.asins:
       for asin in results.asins:
           list_reviews.append(getProductReviews(asin, results.subcomments, results.numPages))
           # Wait between 30 to 90 seconds
           time.sleep(randint(30, 90))
   else:
       for asin in unknown:
           list_reviews.append(getProductReviews(asin, results.subcomments, results.numPages))
           # Wait between 30 to 90 seconds
           time.sleep(randint(30, 90))

   file = None
   if results.output:
      file = open(results.output, 'w')

   # list_reviews is a list of reviews
   for reviews in list_reviews:
       for review in reviews:
          # Write to file
          if file:
             file.write(str(review) + '\n')
          # Print to standard out
          else:
             print review
   return 0

if __name__ == '__main__':
   sys.exit(main())
