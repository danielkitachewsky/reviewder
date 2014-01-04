#! /usr/bin/python

import json
import os

from reviewder import review_types


def save_review(review, dir_):
  """Saves a review to disk.
  
  Args:
    - review is a review_types.Review
    - dir_ is the directory to save the review to. If it doesn't exist, the
    review is not saved.
  Returns:
    - True if the save was successful, False otherwise.
  """
  if not os.path.isdir(dir_):
    return False
  with open(os.path.join(dir_, str(review.id_)), "wb") as f:
    f.write(json.dumps(_json_from_review(review)))
    f.write('\n')  # For nice behavior from terminal


def load_review(dir_, id_):
  """Loads a review from disk.

  Args:
    - dir_ is the directory holding the reviews.
    - id_ is the review's integer id.
  Returns:
    - a review_types.Review if successful, or None if not.
  """
  filename = os.path.join(dir_, str(id_))
  if not os.path.exists(filename):
    return None
  with open(filename, "rb") as f:
    review_json = json.loads(f.read())
  return _review_from_json(review_json)


def _json_from_review(review):
  """Gives a JSON representation of a review."""
  return json.dumps(review.__dict__)


def _review_from_json(json_):
  """Returns a review_types.Review parsed from the json_."""
  return review_types.Review(**json.loads(json_))
