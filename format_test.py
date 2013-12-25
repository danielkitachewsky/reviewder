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
        ("{%toto.%}", set()),
        ("{%to-to%}", set()),
        ("{%toto%}", {"toto"}),
        ("{%toto.abc%}", {"toto"}),
        ("{%_1%}", {"_1"}),
        ("{%toto%}{%tata%}", {"toto", "tata"}),
        ("{%toto%}{%toto%}", {"toto"}),
        ]
    for text, tokens in pairs:
      self.assertEqual(set(format.collect_tokens(text)), tokens)

  def test_token(self):
    self.assertEqual("a", format.Token("a", "").label)
    self.assertEqual("a", format.Token("a", None).label)
    self.assertEqual("a.abc", format.Token("a", "abc").label)

  def test_member(self):
    class InClass(object):
      abc = "foo"
    class InInit(object):
      def __init__(self):
        self.abc = "foo"
    dict_like = {"abc": "foo"}
    text = "{%a.abc%}"
    for var in [InClass(), InInit(), dict_like]:
      self.assertEqual("foo", format._get_member(var, "abc"))
      self.assertEqual("foo", format.render_text(text, a=var))
    self.assertEqual("", format.render_text(text, a=1))


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

