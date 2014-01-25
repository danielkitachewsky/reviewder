#! /usr/bin/python
# encoding: utf-8

import os
import re
import sys

from reviewder import session
from reviewder import review_format


def get_review_bundle(dci_number, limit=0):
  """Get all reviews by and on single person."""
  reviews = (session.JudgeCenterSession()
             .add_filter_or("SubjectDCINumber", str(dci_number))
             .add_filter("ReviewerDCINumber", str(dci_number))
             .get_reviews(limit))
  return reviews


def prompt_review_bundle(limit=0):
  dci_number = raw_input(
    "Type a DCI number to get all reviews on and by that person\nDCI: ")
  if not re.match("^[1-9][0-9]{3,9}$", dci_number):
    print "This doesn't look like a DCI number. Aborting."
    sys.exit(1)
  reviews = get_review_bundle(dci_number, limit)
  name = "%s_reviews.html" % dci_number
  save_to_file(reviews, name)


def get_recos():
  """Get recommendation reviews."""
  reviews = (session.JudgeCenterSession()
             .add_filter("SubjectLevelCd", "2")
             .add_filter_or("Comments", "recommend")
             .add_filter("Strengths", "recommend")
             .get_reviews())
  return reviews


def save_to_file(reviews, name):
  filename = os.path.join(os.path.expanduser("~/Documents"), name)
  with open(filename, "wb") as f:
    f.write(review_format.render_reviews(reviews,
                                         title=u"Reviews"))
  print "Reviews saved in %s" % filename


def review_from_file(filename):
  from reviewder import importer
  return importer.parse_html_review(open(filename))

def main():
  print "Reviewder, the review downloader!"
  if len(sys.argv) > 1 and sys.argv[1] == "reco":
    reviews = get_recos()
    save_to_file(reviews, "recos.html")
  elif len(sys.argv) > 1:
    prompt_review_bundle(int(sys.argv[1]))
  else:
    prompt_review_bundle()
  if sys.platform == 'win32':
    raw_input("Press enter to close...")


if __name__ == "__main__":
  main()
