#! /usr/bin/python
# encoding: utf-8

import format
import os
import random
import unittest


class FormatTestCase(unittest.TestCase):
  def test_rendering_text(self):
    text = u"toto{%toto%}tata{%toto%}:{%titi%}"
    self.assertEqual(u"totoatataa:b",
                     format.render_text(text,
                                        toto=u"a", titi=u"b", tutu=u"c"))
    self.assertEqual(u"totoatataa:",
                     format.render_text(text,
                                        toto=u"a"))
  
  def test_tokens(self):
    pairs = [
        (u"", set()),
        (u"{%%}", set()),
        (u"{%1%}", set()),
        (u"{toto%}", set()),
        (u"{%toto}", set()),
        (u"{%toto.%}", set()),
        (u"{%to-to%}", set()),
        (u"{%toto%}", {u"toto"}),
        (u"{%toto.abc%}", {u"toto"}),
        (u"{%_1%}", {u"_1"}),
        (u"{%toto%}{%tata%}", {u"toto", u"tata"}),
        (u"{%toto%}{%toto%}", {u"toto"}),
        ]
    for text, tokens in pairs:
      self.assertEqual(set(format.collect_tokens(text)), tokens)

  def test_token(self):
    self.assertEqual(u"a", format.Token(u"a", u"").label)
    self.assertEqual(u"a", format.Token(u"a", None).label)
    self.assertEqual(u"a.abc", format.Token(u"a", u"abc").label)

  def test_member(self):
    class InClass(object):
      abc = u"foo"
    class InInit(object):
      def __init__(self):
        self.abc = u"foo"
    dict_like = {u"abc": u"foo"}
    text = u"{%a.abc%}"
    for var in [InClass(), InInit(), dict_like]:
      self.assertEqual(u"foo", format._get_member(var, u"abc"))
      self.assertEqual(u"foo", format.render_text(text, a=var))
    self.assertEqual(u"", format.render_text(text, a=1))
    text = u"{%a.abc%}{%a.def%}"
    dict_like = {u"abc": u"foo", u"def": u"bar"}
    self.assertEqual(u"foobar", format.render_text(text, a=dict_like))
    dict_like = {u"abc": u"гы-гы", u"def": 1}
    self.assertEqual(u"гы-гы1", format.render_text(text, a=dict_like))


class FormatFileTestCase(unittest.TestCase):
  def setUp(self):
    text = u"toto{%toto%}tata{%toto%}:{%titi%}"
    self.filename = _make_random_filename()
    with open(self.filename, "wb") as f:
      f.write(text.encode("utf-8"))

  def tearDown(self):
    os.remove(self.filename)

  def test_rendering_file(self):
    self.assertEqual(u"totoatataa:b",
                     format.render_template(self.filename,
                                            toto=u"a", titi=u"b", tutu=u"c"))
    self.assertEqual(u"totoatataa:",
                     format.render_template(self.filename,
                                            toto=u"a"))

def _make_random_filename():
  """Returns a filename with a random string.

  Follows the pattern "\.random_[0-9]+"."""
  rand_part = random.getrandbits(32)
  return ".random_%s" % rand_part

if __name__ == "__main__":
  unittest.main()

