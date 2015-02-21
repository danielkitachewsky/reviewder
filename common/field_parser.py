#! /usr/bin/python

from bs4 import BeautifulSoup
from dateutil.parser import parse
import sys

from common import types


def parse_summary_fields(soup):
  """Parses the summary of a Judge Center object.

  Known to work for reviews and investigation cases. Must be extracted from the
  English version of the Judge Center, as the parsing relies on the textual name
  of the fields to determine the exact treatment of each.
  Args:
    - soup is a BeautifulSoup object containing the review's HTML markup.
  Returns:
    - a dictionary {attribute => contents} with human-readable values. The text
    fields of the review itself are HTML markup, the rest are simple strings.
    Dates are UTC.
  """
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
    elif name in (
        # For reviews
        "Entered",
        "Observed",
        # For investigations
        "Entered Date",
        "Incident Date",
        ):
      date = parse(contents_soup.text.strip().split('"')[1])
      contents = date.strftime("%Y-%m-%d")
    else:
      contents = contents_soup.text.strip()
    result[name] = contents
  return result
