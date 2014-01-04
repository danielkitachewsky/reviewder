#! /usr/bin/python
# encoding: utf-8

import os
import re
import sys

from reviewder import session
from reviewder import review_format


def get_review_bundle(dci_number):
  """Get all reviews by and on single person."""
  reviews = (session.JudgeCenterSession()
             .add_filter_or("SubjectDCINumber", str(dci_number))
             .add_filter("ReviewerDCINumber", str(dci_number))
             .get_reviews())
  return reviews


def main():
  print "Reviewder, the review downloader!"
  dci_number = raw_input(
    "Type a DCI number to get all reviews on and by that person\nDCI: ")
  if not re.match("^[1-9][0-9]{3,9}$", dci_number):
    print "This doesn't look like a DCI number. Aborting."
    sys.exit(1)
  reviews = get_review_bundle(dci_number)
  filename = "%s_reviews.html" % dci_number
  with open(filename, "wb") as f:
    f.write(review_format.render_reviews(reviews,
                                         title=u"Reviews"))
  print "Reviews saved in %s" % filename


if __name__ == "__main__":
  main()
