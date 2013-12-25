#! /usr/bin/python

import format
import os
import random
import unittest


class FormatTestCase(unittest.TestCase):
  def test_rendering_text(self):
    text = "toto{%toto%}tata{%toto%}:{%titi%}"
    self.assertEqual("totoatataa:b",
                     format.render_text(text,
                                        toto="a", titi="b", tutu="c"))
    self.assertRaises(format.RenderingError,
                      format.render_text,
                      text,
                      toto="a")
  
  def test_tokens(self):
    pairs = [
        ("", set()),
        ("{%%}", set()),
        ("{%1%}", set()),
        ("{toto%}", set()),
        ("{%toto}", set()),
        ("{%to-to%}", set()),
        ("{%toto%}", {"toto"}),
        ("{%_1%}", {"_1"}),
        ("{%toto%}{%tata%}", {"toto", "tata"}),
        ("{%toto%}{%toto%}", {"toto"}),
        ]
    for text, tokens in pairs:
      self.assertEqual(format.collect_tokens(text), tokens)


class FormatFileTestCase(unittest.TestCase):
  def setUp(self):
    text = "toto{%toto%}tata{%toto%}:{%titi%}"
    self.filename = _make_random_filename()
    with open(self.filename, "wb") as f:
      f.write(text)

  def tearDown(self):
    os.remove(self.filename)

  def test_rendering_file(self):
    self.assertEqual("totoatataa:b",
                     format.render_template(self.filename,
                                            toto="a", titi="b", tutu="c"))
    self.assertRaises(format.RenderingError,
                      format.render_template,
                      self.filename,
                      toto="a")

def _make_random_filename():
  """Returns a filename with a random string.

  Follows the pattern "\.random_[0-9]+"."""
  rand_part = random.getrandbits(32)
  return ".random_%s" % rand_part

if __name__ == "__main__":
  unittest.main()

