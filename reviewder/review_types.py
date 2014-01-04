#! /usr/bin/python


class Error(Exception):
  """Base class for errors raised by this project."""


class Review(object):
  """Base class for all review types."""
  # TODO use DCI numbers instead of plain text
  def __init__(self, id_, **kwargs):
    self.id_ = id_
    for key, value in kwargs.iteritems():
      self.__dict__[key] = value

  def __eq__(self, other):
    if not other:
      return False
    if not isinstance(other, Review):
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
      return "Review(%s, %s)" % (self.id_, ", ".join(field_reprs))
    else:
      return "Review(%s)" % self.id_

  def __str__(self):
    return repr(self)

