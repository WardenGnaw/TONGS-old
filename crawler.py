import sys
import re

from bs4 import BeautifulSoup
import urllib2
import requests
import json

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
def getProductReviews(asin, pageLimit=3):
   reviews = None

   # Get the first review page for product
   url = "http://www.amazon.com/product-reviews/" + str(asin) + "/?showViewpoints=0&sortBy=byRankDescending&pageNumber=1"
   
   # HTTP request to get content
   r = requests.get(url)

   # Check status to see if it succeeded
   if (r.status_code == 200): 
      reviews = []
      bs = BeautifulSoup(r.content)
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
         url = "http://www.amazon.com/product-reviews/" + str(asin) + "/?showViewpoints=0&sortBy=byRankDescending&pageNumber=" + str(idx)
         r = requests.get(url)
         for x in bs.findAll('div', {"class" : "review"}):
             review = Review(x.find('a', {"class" : "review-title"}).text.encode('utf-8'),
                             x.find('span', {"class" : "review-text"}).text.encode('utf-8'),
                             x.find('a', {"class" : "author"}).text.encode('utf-8'),
                             x.find('span', {"class" : "review-date"}).text.encode('utf-8'),
                             None, 
                             getNumStars(x), 
                             getHelpfulVotes(x))
             reviews.append(review)
             print review
         idx += 1

   else:
      print url + ' returned : ' + str(r.status_code)
   
   return reviews

def main():
   print getProductReviews('B00F3J4NSI')
   print getProductReviews('B00X4WHP5E')
   return 0

if __name__ == '__main__':
   sys.exit(main())
