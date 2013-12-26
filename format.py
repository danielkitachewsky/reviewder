#! /usr/bin/python

from collections import defaultdict
import os
import re

import review_types

TOKEN_RE = re.compile("{%([a-zA-Z_][a-zA-Z0-9_]*)(\.[a-zA-Z0-9_]+)?%}")


class RenderingError(review_types.Error):
  """Generic error raised during rendering of templates."""


class Token(object):
  """A token-replacement spec"""
  def __init__(self, text, member):
    self.text = text
    self.member = member
    # suppress initial dot coming from parsing
    if self.member and self.member[:1] == ".":
      self.member = self.member[1:]

  @property
  def label(self):
    """Returns the string that represents this token."""
    if not self.member:
      return self.text
    return "%s.%s" % (self.text, self.member)

  def __eq__(self, other):
    return self.text == other.text and self.member == other.member

  def __hash__(self):
    return hash(self.text) + hash(self.member)


def collect_tokens(text):
  """Returns a dict of all tokens in given text.

  The dict is {text => [Token...]}.
  """
  result = defaultdict(set)
  search_result = TOKEN_RE.search(text)
  while search_result:
    token = Token(search_result.group(1), search_result.group(2))
    result[search_result.group(1)].add(token)
    search_result = TOKEN_RE.search(text, search_result.end())
  return result


def render_template(filename, **kwargs):
  """Get a template from a file and replace tokens.

  Args:
    - filename is the relative or absolute path of a template file, which can
    be any text file format with optional {%tokens%}. Tokens must be valid
    Python identifiers. If the file doesn't exist, an empty string is returned.
    - **kwargs are the values to replace the tokens with. If a token isn't
    given a value, a RenderingError is raised. Extra replacements don't have
    any effect.
  Returns:
    - string containing the rendered template.
  """
  template_text = _get_text_from_file(filename)
  return render_text(template_text, **kwargs)


def render_text(text, **kwargs):
  """Replace tokens in the given text.

  Args:
    - text is a string with optional {%tokens%}. Tokens must be valid Python
    identifiers.
    - **kwargs are the values to replace the tokens with. If a token isn't
    given a value, it's replaced by the empty string. Extra replacements don't
    have any effect.
  Returns:
    - string containing the rendered text.
  """
  tokens_to_replace = collect_tokens(text)
  for token_set in tokens_to_replace.itervalues():
    for token in token_set:
      if token.member:
        value = _get_member(kwargs.get(token.text, {}), token.member)
      else:
        value = kwargs.get(token.text, u"")
      text = text.replace(u"{%%%s%%}" % token.label, unicode(value))
  return text


def _get_member(var, name):
  """Returns the member named name from var.

  This can be a dictionary member or a class member, i.e. if var is a dict,
  it returns var[name], and if var is a class, it returns var.name.
  If member isn't present or wrong type, returns an empty string.
  """
  try:
    return var[name]
  except KeyError:
    return ""
  except TypeError:
    pass
  try:
    return var.__getattribute__(name)
  except KeyError:
    return ""
  except AttributeError:
    return ""
  # Shouldn't happen
  raise RenderingError("Wrong type %s" % type(var))

def _get_text_from_file(filename):
  """Return the text contents of the given filename.

  If the file doesn't exist, returns an empty string."""
  if not os.path.exists(filename):
    return ""
  with open(filename) as f:
    return f.read()


def main():
  pass

if __name__ == "__main__":
  main()

