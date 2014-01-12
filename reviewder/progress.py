# encoding: utf-8
"""Progress messages.

Print messages that overwrite each other.
"""

from __future__ import print_function
import os
import sys


class Error(Exception):
  """Raised when Messages are used incorrectly."""


class _Messages(object):
  """Abstract class to log progress messages."""
  def log(self, msg):
    """Display a message.

    The message should not contain any control characters and should be
    decoded (so that Unicode characters all have length 1).
    """
    raise NotImplementedError

  def finish(self, newline=True):
    """End the message display.

    If newline is True, leave the last message, otherwise erase it. The
    cursor will be at the start of an empty line in all cases.
    """
    raise NotImplementedError


class _SimpleMessages(_Messages):
  def log(self, msg):
    print(msg.encode(sys.stderr.encoding, 'replace'), file=sys.stderr)

  def finish(self, newline=True):
    # Since we always print a newline, there's nothing to do to finalize
    pass


class _ProgressMessages(_Messages):
  def __init__(self):
    self.last_message_length = 0
    self.finalized = False

  def log(self, msg):
    if self.finalized:
      raise
    print('\b' * self.last_message_length, end='', file=sys.stderr)
    print(' ' * self.last_message_length, end='', file=sys.stderr)
    print('\b' * self.last_message_length, end='', file=sys.stderr)
    self.last_message_length = len(msg)
    print(msg.encode(sys.stderr.encoding, 'replace'),
          end='', file=sys.stderr)

  def finish(self, newline=True):
    if newline:
      print('', file=sys.stderr)
    else:
      print('\b' * self.last_message_length, end='', file=sys.stderr)


Messages = _ProgressMessages if os.isatty(2) else _SimpleMessages
