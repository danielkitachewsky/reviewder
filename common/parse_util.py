"""Utility functions to work with HTML pages."""

from bs4 import BeautifulSoup


def get_tag_by_field(text_or_soup, tag_name, field, expr):
  """Returns HTML tag in text if expr is in its field.

  If not found, returns None.
  """
  if isinstance(text_or_soup, BeautifulSoup):
    soup = text_or_soup
  else:
    soup = BeautifulSoup(text_or_soup)
  for tag in soup.find_all(tag_name):
    if expr in tag.get(field, ''):
      return tag
  return None
