#! /usr/bin/python


class Error(Exception):
  """Base class for errors raised by this project."""


class Review(object):
  """Base class for all review types."""
  # TODO use DCI numbers instead of plain text
  def __init__(self, id_, observer="", subject="",
               strengths="", afi="", comments=""):
    self.id_ = id_
    self.observer = observer
    self.subject = subject
    self.strengths = strengths
    self.afi = afi
    self.comments = comments

  def __eq__(self, other):
    if not other:
      return False
    if not isinstance(other, Review):
      return False
    if other.id_ != self.id_:
      return False
    if other.observer != self.observer:
      return False
    if other.subject != self.subject:
      return False
    if other.strengths != self.strengths:
      return False
    if other.afi != self.afi:
      return False
    if other.comments != self.comments:
      return False
    return True

  def __hash__(self):
    return (hash(self.id_) +
            hash(self.observer) +
            hash(self.subject) +
            hash(self.strengths) +
            hash(self.afi) +
            hash(self.comments))

