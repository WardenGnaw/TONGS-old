import sys
import re

from bs4 import BeautifulSoup
import urllib2
import requests
import json
from selenium import webdriver
import time

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
        self.reviewDate = reviewDate

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
       return votes.text
   else:
       return None

def getReviewComments(reviewComments):
   ret = []
   print reviewComments
   """
   for comment in reviewComments.findAll('div', {"class" : "review-comment"}):
       print "COMMENT FOUND"
       print comment
   """
def getProductReviews(asin, pageLimit=2):
   reviews = None

   # Get the first review page for product
   url = "http://www.amazon.com/product-reviews/" + str(asin) + "/?showViewpoints=0&sortBy=byRankDescending&pageNumber=1"

   browser=webdriver.Firefox()
   browser.get(url)
   for link in browser.find_elements_by_xpath("//a[contains(concat(' ',normalize-space(@class),' '),' a-link-expander ')]"):
      link.click()
      time.sleep(5)

   # More review comments button... Need to fix this.
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
      for link in browser.find_elements_by_xpath("//a[contains(concat(' ',normalize-space(@class),' '),' a-link-expander ')]"):
         link.click()
         time.sleep(5)
      bs = BeautifulSoup(browser.page_source)
      idx += 1
      time.sleep(30)
   
   browser.close()
   
   return reviews

def main():
   getProductReviews('B00F3J4NSI')
   getProductReviews('B00X4WHP5E')
   return 0

if __name__ == '__main__':
   sys.exit(main())
