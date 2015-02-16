#! /usr/bin/python
# encoding: utf-8

import tempfile
import shutil
import unittest

from common import types


class SerializationTestCase(unittest.TestCase):
  def setUp(self):
    self.dir_ = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.dir_)

  def test_review_save_load(self):
    review_id = 1
    review = types.Expandable(review_id,
                              observer=u"Daniel",
                              subject=u"Pepito",
                              strengths=u"Zéro.",
                              afi=u"Nada.",
                              comments=u"гы-гы")
    types.save(review, self.dir_)
    self.assertEqual(review, types.load(self.dir_, review_id))
    for field in ["observer",
                  "subject",
                  "strengths",
                  "afi",
                  "comments"]:
      old_value = review.__dict__[field]
      review.__dict__[field] = "lol"
      self.assertNotEqual(review, types.load(self.dir_, review_id))
      review.__dict__[field] = old_value
      self.assertEqual(review, types.load(self.dir_, review_id))
      
if __name__ == "__main__":
  unittest.main()
