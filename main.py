#! /usr/bin/python
# encoding: utf-8

import os

from reviewder import session
from reviewder import review_format
from reviewder import review_io


def save_review(review):
  if not os.path.isdir("data"):
    os.makedirs("data")
  review_io.save_review(review, "data")


def get_review_bundle(dci_number):
  """Get all reviews by and on single person."""
  reviews = (session.JudgeCenterSession()
             .add_filter_or("SubjectDCINumber", str(dci_number))
             .add_filter("ReviewerDCINumber", str(dci_number))
             .get_reviews())
  return reviews

def main():
  reviews = get_review_bundle("9300051073")  # Aurelie Violette
  for review in reviews:
    save_review(review)

  print review_format.render_reviews(reviews,
                                     title=u"Reviews")


if __name__ == "__main__":
  main()
