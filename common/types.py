#! /usr/bin/python

import json
import os


class Expandable(object):
  """Generic class that can hold arbitrary fields."""
  def __init__(self, id_, **kwargs):
    self.id_ = id_
    for key, value in kwargs.iteritems():
      self.__dict__[key] = value

  def __eq__(self, other):
    if not other:
      return False
    if not isinstance(other, Expandable):
      return False
    if other.id_ != self.id_:
      return False
    if other.__dict__ != self.__dict__:
      return False
    return True

  def __hash__(self):
    result = 0
    for key in sorted(self.__dict__):
      result += hash(key) + hash(self.__dict__[key])
    return result

  def __repr__(self):
    field_reprs = ["%s=%s" % (key, repr(value))
                   for (key, value)
                   in self.__dict__.iteritems()]
    if field_reprs:
      # TODO should we subclass with meaningful names?
      return "Expandable(%s, %s)" % (self.id_, ", ".join(field_reprs))
    else:
      return "Expandable(%s)" % self.id_

  def __str__(self):
    return repr(self)

  def _to_json(self):
    """Gives a JSON representation of a expandable."""
    return json.dumps(self.__dict__)

  @classmethod
  def _from_json(cls, json_):
    """Returns an Expandable parsed from the json_."""
    return Expandable(**json.loads(json_))

def save(expandable, dir_):
  """Saves an expandable to disk.
  
  Args:
    - expandable is an Expandable
    - dir_ is the directory to save the expandable to. If it doesn't exist, the
    expandable is not saved.
  Returns:
    - True if the save was successful, False otherwise.
  """
  if not os.path.isdir(dir_):
    return False
  with open(os.path.join(dir_, str(expandable.id_)), "wb") as f:
    f.write(json.dumps(expandable._to_json()))
    f.write('\n')  # For nice behavior from terminal


def load(dir_, id_):
  """Loads an expandable from disk.

  Args:
    - dir_ is the directory holding the expandables.
    - id_ is the expandable's integer id.
  Returns:
    - an Expandable if successful, or None if not.
  """
  filename = os.path.join(dir_, str(id_))
  if not os.path.exists(filename):
    return None
  with open(filename, "rb") as f:
    review_json = json.loads(f.read())
  return Expandable._from_json(review_json)
