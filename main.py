#! /usr/bin/python
# encoding: utf-8

import os

from reviewder import format
from reviewder import session
from reviewder import review_io


def _target_level(review):
  """Returns a formatted level string for the target."""
  if review.new_level:
    return u"%s->%s" % (review.existing_level, review.new_level)
  else:
    return review.existing_level


def _is_recommendation(review):
  """Guess if the review is a recommendation towards L3."""
  text = review.comments.lower() + review.strengths.lower()
  rec_pos = text.find("recommendation")
  while rec_pos >= 0:
    text_around = text[max(0, rec_pos - 15): min(rec_pos + 30, len(text) - 1)]
    if "level 3" in text_around \
          or "l3" in text_around \
          or "level three" in text_around:
      return True
    rec_pos = text.find("recommendation", rec_pos + 1)
  return False


def _bgcolor(review):
  if review.new_level:  # Certification review
    return "#ffff88"  # Light yellow
  if _is_recommendation(review):
    return "#aaffaa"  # Light green
  return "#ffffff"  # White


def _exam_score(review):
  """Returns an HTML-formatted exam score, if applicable."""
  if review.type_ == "Evaluation":
    return u""
  return u"<p>Scored %s on written exam." % review.exam_score


def save_review(review):
  if not os.path.isdir("data"):
    os.makedirs("data")
  review_io.save_review(review, "data")


def get_review_bundle(dci_number):
  """Get all reviews by and on single person."""
  reviews = (session.JudgeCenterSession()
             .add_filter_or("SubjectDCINumber", str(dci_number))
             .add_filter("ReviewerDCINumber", str(dci_number))
             .get_reviews())
  return reviews

def main():
  reviews = get_review_bundle("9300051073")  # Aurelie Violette
  for review in reviews:
    save_review(review)

  rendered_reviews = [
    format.render_template("templates/review.html",
                           review=review,
                           target_level=_target_level(review),
                           bgcolor=_bgcolor(review),
                           exam_score=_exam_score(review))
    for review in reviews]
  full_html = format.render_template(
    "templates/reviews.html", body="".join(rendered_reviews), title="Reviews",
    all_review_ids="[%s]" % ",".join(str(r.id_) for r in reviews))
  print full_html.encode("utf-8")


if __name__ == "__main__":
  main()
