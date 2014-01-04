#! /usr/bin/python

from __future__ import print_function

from bs4 import BeautifulSoup
from dateutil.parser import parse
import sys

from reviewder import review_types


def parse_fields(html):
  """Parses an html representation of a Judge Center review.

  The review must be extracted from the English version of the Judge Center, as
  the parsing relies on the textual name of the fields to determine the exact
  treatment of each.
  The fields in a review are:
    - Areas for Improvement
    - City
    - Comments
    - Comparison  # Average/Below/Above/Outstanding
    - Country
    - Entered  # Date
    - Entered By
    - Event Type
    - Existing Level  # Subject's level
    - ID
    - Language
    - Observed  # Date
    - Reviewer
    - Reviewer Level
    - Reviewer Role
    - Status  # Draft, submitted...
    - Strengths
    - Subject
    - Subject Role
    - Type  # Interview or review
  In addition, interviews have:
    - Exam ID
    - Exam Score
    - New Level
  Args:
    - html is a string containing the review's HTML markup or a file handle to
    the HTML markup.
  Returns:
    - a dictionary {attribute => contents} with human-readable values. The text
    fields of the review itself are HTML markup, the rest are simple strings.
    Dates are UTC.
  """
  soup = BeautifulSoup(html)
  review_soup = soup.find(id="summary")
  result = {}
  for b_tag in review_soup.find_all("b"):
    name = b_tag.string.strip().strip(":")
    contents_soup = b_tag.parent
    b_tag.extract()
    if name in ("Strengths", "Areas for Improvement", "Comments"):
      contents_soup.attrs = {}
      tag_length = len(contents_soup.name)
      contents = contents_soup.prettify()[tag_length+4:-tag_length-5]
    elif name in ("Entered", "Observed"):
      date = parse(contents_soup.text.strip().split('"')[1])
      contents = date.strftime("%Y-%m-%d")
    else:
      contents = contents_soup.text.strip()
    result[name] = contents
  print("%s on %s" % (result["Reviewer"], result["Subject"]), file=sys.stderr)
  return result


def make_review(field_dict):
  """Returns a review_types.Review filled from a parsed dictionary."""
  return review_types.Review(
    id_=int(field_dict["ID"]),
    observer=field_dict["Reviewer"],
    subject=field_dict["Subject"],
    strengths=field_dict["Strengths"],
    afi=field_dict["Areas for Improvement"],
    comments=field_dict["Comments"],
    city=field_dict["City"],
    comparison=field_dict["Comparison"],
    country=field_dict["Country"],
    event_type=field_dict["Event Type"],
    reviewer_level=field_dict["Reviewer Level"],
    type_=field_dict["Type"],
    existing_level=field_dict["Existing Level"],
    new_level=field_dict.get("New Level", ""),
    exam_score=field_dict.get("Exam Score", ""),
    entered_date=field_dict.get("Entered", ""),
    )


def parse_html_review(html):
  return make_review(parse_fields(html))
