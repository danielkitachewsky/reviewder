#! /usr/bin/python
# encoding: utf-8

import format
import importer
import session


def _target_level(review):
  """Returns a formatted level string for the target."""
  if review.new_level:
    return u"%s->%s" % (review.existing_level, review.new_level)
  else:
    return review.existing_level


def _exam_score(review):
  """Returns an HTML-formatted exam score, if applicable."""
  if review.type_ == "Evaluation":
    return u""
  return u"<p>Scored %s on written exam." % review.exam_score


def save_review(review):
  import os
  import review_io
  if not os.isdir("data"):
    os.makedirs("data")
  review_io.save_review(review, "data")


def main():
  jcs = session.JudgeCenterSession()
  jcs.add_filter_or("SubjectDCINumber", "1206181211")
  jcs.add_filter("ReviewerDCINumber", "1206181211")
  reviews = [importer.parse_html_review(text)
             for text in jcs.get_reviews()]
  for review in reviews:
    save_review(review)
  # reviews = [
  #   importer.parse_html_review(open("brefka.html")),
  #   importer.parse_html_review(open("hiller.html")),
  #   ]

  rendered_reviews = [
    format.render_template("review.html", review=review,
                           target_level=_target_level(review),
                           exam_score=_exam_score(review))
    for review in reviews]
  full_html = format.render_template(
    "reviews.html", body="".join(rendered_reviews), title="Reviews",
    all_review_ids="[%s]" % ",".join(str(r.id_) for r in reviews))
  print full_html.encode("utf-8")


if __name__ == "__main__":
  main()
