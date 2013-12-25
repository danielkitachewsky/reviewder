#! /usr/bin/python

import os
import re

import review_types

TOKEN_RE = re.compile("{%([a-zA-Z_][a-zA-Z0-9_]*)%}")


class RenderingError(review_types.Error):
  """Generic error raised during rendering of templates."""


def collect_tokens(text):
  """Returns the set of all tokens in given text."""
  result = set()
  search_result = TOKEN_RE.search(text)
  while search_result:
    result.add(search_result.group(1))
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
    given a value, a RenderingError is raised. Extra replacements don't have
    any effect.
  Returns:
    - string containing the rendered text.
  """
  tokens_to_replace = collect_tokens(text)
  missing_tokens = tokens_to_replace - set(kwargs)
  if missing_tokens:
    raise RenderingError("some tokens not given a value: " +
                         ",".join(missing_tokens))
  for token in tokens_to_replace:
    text = text.replace("{%" + token + "%}", kwargs[token])
  return text


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

