

import inspect
import os

from reviewder import format


def _get_template(name):
  """Finds the template with given name relative to this module."""
  # HACK to fall back on our feet when deployed through py2exe
  here = os.path.dirname(os.path.abspath(__file__))
  if "\\" in here:
    while "library.zip" in here:
      here = "\\".join(here.split("\\")[:-1])
  return os.path.join(here, "templates", name)


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


def render_review(review):
  return format.render_template(_get_template("review.html"),
                                review=review,
                                target_level=_target_level(review),
                                bgcolor=_bgcolor(review),
                                exam_score=_exam_score(review))


def render_reviews(reviews, title):
  rendered_reviews = [render_review(review) for review in reviews]
  full_html = format.render_template(
    _get_template("reviews.html"),
    body="".join(rendered_reviews),
    title=title,
    all_review_ids="[%s]" % ",".join(str(r.id_) for r in reviews))
  return full_html.encode("utf-8")
