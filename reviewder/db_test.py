
import os
import tempfile
import shutil
import unittest

from reviewder import db
from reviewder import importer


FIELDS = [
  ("foo", "BLOB"),
  ("bar", "TEXT"),
]


class DBTestCase(unittest.TestCase):
  def setUp(self):
    self.dir_ = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.dir_)

  def test_creation_command(self):
    self.assertEqual(
        "CREATE TABLE baz(id_ INTEGER PRIMARY KEY, foo BLOB, bar TEXT)",
        db.make_table_creation_command("baz", FIELDS))

  def test_insertion_command(self):
    self.assertEqual("INSERT INTO baz VALUES(?, ?, ?)",
                     db.make_insertion_command("baz", FIELDS))

  def test_full(self):
    db_filename = os.path.join(self.dir_, "tmp.db")
    filename = "reviewder/testdata/promotion.html"
    review = importer.parse_html_review(open(filename))
    database = db.ReviewDatabase(db_filename)
    try:
      database.save_review(review)
    finally:
      database.close()
    database = db.ReviewDatabase(db_filename)
    try:
      read_review = database.get_review(review.id_)
      self.assertEqual(review.id_, read_review.id_)
      self.assertEqual(review.observer, read_review.observer)
      self.assertEqual(review.subject, read_review.subject)
      self.assertEqual(review.strengths, read_review.strengths)
      self.assertEqual(review.afi, read_review.afi)
      self.assertEqual(review.comments, read_review.comments)
      self.assertEqual(review.city, read_review.city)
      self.assertEqual(review.comparison, read_review.comparison)
      self.assertEqual(review.country, read_review.country)
      self.assertEqual(review.event_type, read_review.event_type)
      self.assertEqual(review.reviewer_level, read_review.reviewer_level)
      self.assertEqual(review.type_, read_review.type_)
      self.assertEqual(review.existing_level, read_review.existing_level)
      self.assertEqual(review.new_level, read_review.new_level)
      self.assertEqual(review.exam_score, read_review.exam_score)
      self.assertEqual(review.entered_date, read_review.entered_date)
    finally:
      database.close()
