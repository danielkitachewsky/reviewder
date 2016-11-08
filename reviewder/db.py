"""Database for reviews.
"""

import os
import sqlite3

from common import types


FIELD_DESCRIPTIONS = [
    ("observer", "TEXT"),
    ("subject", "TEXT"),
    ("strengths", "TEXT"),
    ("afi", "TEXT"),
    ("comments", "TEXT"),
    ("city", "TEXT"),
    ("comparison", "TEXT"),
    ("country", "TEXT"),
    ("event_type", "TEXT"),
    ("reviewer_level", "TEXT"),
    ("type_", "TEXT"),
    ("existing_level", "TEXT"),
    ("new_level", "TEXT"),
    ("exam_score", "TEXT"),
    ("entered_date", "TEXT"),
]

def make_table_creation_command(table_name, field_descriptions):
  fields = ["id_ INTEGER PRIMARY KEY"]
  for name, type_ in field_descriptions:
    field = "%s %s" % (name, type_)
    fields.append(field)
  return "CREATE TABLE %s(%s)" % (table_name, ", ".join(fields)) 


def tuple_from_expandable(expandable, field_descriptions):
  """Returns a tuple corresponding to the database order of fields."""
  list_ = [expandable.__dict__[name] for name, _ in field_descriptions]
  return tuple([expandable.id_] + list_)


def expandable_from_tuple(tuple_, field_descriptions):
  """Returns an Expandable filled with the values in tuple."""
  result = types.Expandable(tuple_[0])
  for (name, _), value in zip(field_descriptions, tuple_[1:]):
    result.__dict__[name] = value
  return result


def make_insertion_command(table_name, field_descriptions):
  placeholders = "?" * (len(field_descriptions) + 1)
  return "INSERT INTO %s VALUES(%s)" % (table_name, ", ".join(placeholders))


def make_select_command(table_name):
  return "SELECT * FROM %s" % table_name


class ReviewDatabase(object):
  """The database is indexed by review ID, which is supposed to be unique. This
  means that if you save a review which has the same ID as another one, it will
  overwrite it.
  """
  def __init__(self, filename):
    """filename is the absolute path to the database."""
    self._filename = filename
    if os.path.exists(filename):
      self._connect()
    else:
      self._create_database()

  def close(self):
    """Closes the database connection and makes it safe to manipulate the
    underlying file."""
    self._connection.close()

  def _connect(self):
    self._connection = sqlite3.connect(self._filename)

  def _create_database(self):
    """Creates an empty database."""
    self._connect()
    cursor = self._connection.cursor()
    cursor.execute(make_table_creation_command("reviews", FIELD_DESCRIPTIONS))
    self._connection.commit()

  def save_review(self, review):
    cursor = self._connection.cursor()
    cursor.execute(make_insertion_command("reviews", FIELD_DESCRIPTIONS),
                   tuple_from_expandable(review, FIELD_DESCRIPTIONS))
    self._connection.commit()

  def get_review(self, id_):
    """Returns the review with the given id, or None if it's not found."""
    cursor = self._connection.cursor()
    select_command = make_select_command("reviews")
    select_command += " WHERE id_ = ?"
    cursor.execute(select_command, (id_,))
    for row in cursor:
      return expandable_from_tuple(row, FIELD_DESCRIPTIONS)    
    return None
