#! /usr/bin/python
# encoding: utf-8

import os
import re
import sys

from reviewder import db
from reviewder import review_session
from reviewder import review_format


class ReviewderError(Exception):
  """Error raised during use of Reviewder."""


def get_review_bundle(dci_number, limit=0):
  """Get all reviews by and on single person."""
  reviews = (review_session.JudgeCenterReviewsSession()
             .add_filter_or("SubjectDCINumber", str(dci_number))
             .add_filter("ReviewerDCINumber", str(dci_number))
             .get(limit))
  return reviews


def get_on_review_bundle(dci_number, limit=0):
  """Get all reviews on a single person."""
  reviews = (review_session.JudgeCenterReviewsSession()
             .add_filter("SubjectDCINumber", str(dci_number))
             .get(limit))
  return reviews


def get_by_review_bundle(dci_number, limit=0):
  """Get all reviews by a single person."""
  reviews = (review_session.JudgeCenterReviewsSession()
             .add_filter("ReviewerDCINumber", str(dci_number))
             .get(limit))
  return reviews


def prompt_review_bundle(limit=0, mode="all"):
  """Prompt for a DCI number and get a review bundle for that person.

  mode can be:
  - "all": gets reviews on and by that person.
  - "on": gets reviews on that person.
  - "by": gets reviews by that person.
  """
  dci_number = raw_input(
    "Type a DCI number to get all reviews on and by that person\nDCI: ")
  if not re.match("^[1-9][0-9]{3,9}$", dci_number):
    print "This doesn't look like a DCI number. Aborting."
    sys.exit(1)
  if mode == "all":
    reviews = get_review_bundle(dci_number, limit)
  elif mode == "on":
    reviews = get_on_review_bundle(dci_number, limit)
  elif mode == "by":
    reviews = get_by_review_bundle(dci_number, limit)
  else:
    raise ReviewderError("Invalid mode %s" % mode)
  name = "%s_reviews.html" % dci_number
  save_to_file(reviews, name)


def get_recos(limit=0):
  """Get recommendation reviews."""
  reviews = (review_session.JudgeCenterReviewsSession()
             .add_filter("SubjectLevelCd", "2")
             .add_filter_or("Comments", "recommend")
             .add_filter("Strengths", "recommend")
             .add_filter("EnteredDate", "2013/12/31",
                         review_session.JudgeCenterReviewsSession.GREATER_THAN)
             .add_filter("ReviewerLevelCd", "2",
                         review_session.JudgeCenterReviewsSession.GREATER_THAN)
             .get(limit))
  return reviews


def get_panel_reviews(limit=0):
  """Get reviews on panels."""
  reviews = (review_session.JudgeCenterReviewsSession()
             .add_filter_or("SubjectLevelCd", "2")
             .add_filter("SubjectLevelCd", "3")
             .add_filter_or("NewLevelCd", "2")
             .add_filter("NewLevelCd", "3")
             .get(limit))
  return reviews


def read_reviews(from_, to):
  database = db.ReviewDatabase("reviews.db")
  return database.reviews_between(from_, to)


def save_to_file(reviews, name):
  filename = os.path.join(os.path.expanduser("~/Documents"), name)
  with open(filename, "wb") as f:
    f.write(review_format.render_reviews(reviews,
                                         title=u"Reviews"))
  print "Reviews saved in %s" % filename


def main():
  print "Reviewder, the review downloader!"
  if len(sys.argv) > 1 and sys.argv[1] == "reco":
    try:
      limit = int(sys.argv[2])
    except ValueError:
      limit = 0
    reviews = get_recos(limit)
    save_to_file(reviews, "recos.html")
  elif len(sys.argv) > 1 and sys.argv[1] == "panel":
    try:
      limit = int(sys.argv[2])
    except ValueError:
      limit = 0
    reviews = get_panel_reviews(limit)
    save_to_file(reviews, "panel.html")
  elif len(sys.argv) > 1 and sys.argv[1] == "read":
    try:
      from_ = int(sys.argv[2])
    except (ValueError, IndexError):
      from_ = 0
    try:
      to = int(sys.argv[3])
    except (ValueError, IndexError):
      to = 1000000
    reviews = read_reviews(from_, to)
    save_to_file(reviews[::-1], "db.html")
  elif len(sys.argv) > 1:
    try:
      limit = int(sys.argv[1])
      prompt_review_bundle(limit=limit)
    except ValueError:
      prompt_review_bundle(mode=sys.argv[1])
  else:
    prompt_review_bundle()
  if sys.platform == 'win32':
    raw_input("Press enter to close...")


if __name__ == "__main__":
  main()
