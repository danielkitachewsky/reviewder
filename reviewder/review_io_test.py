#! /usr/bin/python
# encoding: utf-8

import tempfile
import review_io
import shutil
import unittest

from reviewder import review_types


class ReviewIOTestCase(unittest.TestCase):
  def setUp(self):
    self.dir_ = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.dir_)

  def test_review_save_load(self):
    review_id = 1
    review = review_types.Review(review_id,
                                 observer=u"Daniel",
                                 subject=u"Pepito",
                                 strengths=u"Zéro.",
                                 afi=u"Nada.",
                                 comments=u"гы-гы")
    review_io.save_review(review, self.dir_)
    self.assertEqual(review, review_io.load_review(self.dir_, review_id))
    for field in ["observer",
                  "subject",
                  "strengths",
                  "afi",
                  "comments"]:
      old_value = review.__dict__[field]
      review.__dict__[field] = "lol"
      self.assertNotEqual(review, review_io.load_review(self.dir_, review_id))
      review.__dict__[field] = old_value
      self.assertEqual(review, review_io.load_review(self.dir_, review_id))
      
if __name__ == "__main__":
  unittest.main()
