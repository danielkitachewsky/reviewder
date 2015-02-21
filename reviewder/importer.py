#! /usr/bin/python

from bs4 import BeautifulSoup
from dateutil.parser import parse
import sys

from common import field_parser
from common import types


def make_review(field_dict):
  """Returns a types.Expandable filled from a parsed dictionary."""
  return types.Expandable(
    id_=int(field_dict["ID"]),
    # Renewal reviews don't have a Reviewer
    observer=field_dict.get("Reviewer", field_dict["Entered By"]),
    subject=field_dict["Subject"],
    strengths=field_dict["Strengths"],
    afi=field_dict["Areas for Improvement"],
    comments=field_dict["Comments"],
    city=field_dict["City"],
    comparison=field_dict.get("Comparison", ""),
    country=field_dict["Country"],
    event_type=field_dict.get("Event Type", "N/A"),
    reviewer_level=field_dict.get("Reviewer Level", ""),
    type_=field_dict["Type"],
    existing_level=field_dict["Existing Level"],
    new_level=field_dict.get("New Level", ""),
    exam_score=field_dict.get("Exam Score", ""),
    entered_date=field_dict.get("Entered", ""),
    )


def parse_html_review(html):
  soup = BeautifulSoup(html)
  return make_review(field_parser.parse_summary_fields(soup))


def main():
  # Here so that it can't be accessed from public-facing Windows build
  import glob
  import os
  from reviewder import review_format
  def save_to_file(reviews, name):
    filename = os.path.join(os.path.expanduser("~/Documents"), name)
    with open(filename, "wb") as f:
      f.write(review_format.render_reviews(reviews,
                                           title=u"Reviews"))
    print "Reviews saved in %s" % filename


  def review_from_file(filename):
    return parse_html_review(open(filename))

  reviews = [review_from_file(filename)
             for filename in glob.glob("reviewder/testdata/*.html")]
  save_to_file(reviews, "blah.html")


if __name__ == "__main__":
  main()
