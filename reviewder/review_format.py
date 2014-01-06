

import os

from reviewder import format


COLOR_YELLOW = "#ffff88"
COLOR_GREEN = "#aaffaa"
COLOR_PINK = "#ffaaaa"
COLOR_BLUE = "#ccccff"
COLOR_WHITE = "#ffffff"


def _get_template(name):
  """Finds the template with given name relative to this module."""
  # HACK to fall back on our feet when deployed through py2exe
  here = os.path.dirname(os.path.abspath(__file__))
  if "\\" in here:
    while "library.zip" in here:
      here = "\\".join(here.split("\\")[:-1])
  return os.path.join(here, "templates", name)


def _subject_level(review):
  """Returns a formatted level string for the target."""
  if _is_certification(review):
    return u"%s->%s" % (review.existing_level, review.new_level)
  else:
    return review.existing_level


def _is_recommendation(review):
  """Guess if the review is a recommendation towards L3."""
  text = review.comments.lower() + review.strengths.lower()
  rec_pos = text.find("recommend")
  while rec_pos >= 0:
    text_around = text[max(0, rec_pos - 15): min(rec_pos + 30, len(text) - 1)]
    if "level 3" in text_around \
          or "l3" in text_around \
          or "level three" in text_around \
          or "written" in text_around:
      return True
    rec_pos = text.find("recommend", rec_pos + 1)
  return False


def _is_self_review(review):
  return review.observer == review.subject


def _is_certification(review):
  return bool(review.new_level)


def _is_renewal(review):
  return review.type_ == "Renewal"


COLORINGS = [
  (_is_certification, "Certification", COLOR_YELLOW),
  (_is_recommendation, "(maybe) Recommendation", COLOR_GREEN),
  (_is_renewal, "Renewal", COLOR_BLUE),
  (_is_self_review, "Self-Review", COLOR_PINK),
  ]


def _bgcolor(review):
  for criterion, _, color in COLORINGS:
    if criterion(review):
      return color
  return COLOR_WHITE


def _make_legend(reviews):
  legends_needed = []
  for criterion, label, color in COLORINGS:
    if any(criterion(review) for review in reviews):
      legends_needed.append((label, color))
  if not legends_needed:
    return ''
  result = '<br/>Legend:'
  for label, color in legends_needed:
    result += (' <span style="background-color: %s">%s</span>'
               % (color, label))
  return result


def _exam_score(review):
  """Returns an HTML-formatted exam score, if applicable."""
  if review.type_ == "Evaluation":
    return u""
  return u"<p>Scored %s on written exam." % review.exam_score


def _reviewer_level(review):
  """Returns the formatted level of the reviewer, if known."""
  if review.type_ == "Renewal":
    # The reviewer's level is not present in these, so we don't show anything
    return ""
  return "(%s)" % review.reviewer_level


def _rated(review):
  """Returns the HTML-formatted rating, if present."""
  if review.type_ == "Renewal":
    # These don't include a rating, so we don't show anything
    return ""
  return '<p>Rated "%s."' % review.comparison


def render_review(review):
  return format.render_template(_get_template("review.html"),
                                review=review,
                                bgcolor=_bgcolor(review),
                                reviewer_level=_reviewer_level(review),
                                subject_level=_subject_level(review),
                                exam_score=_exam_score(review),
                                rated=_rated(review),
                                )


def render_reviews(reviews, title):
  rendered_reviews = [render_review(review) for review in reviews]
  full_html = format.render_template(
    _get_template("reviews.html"),
    intro=_make_legend(reviews),
    body="".join(rendered_reviews),
    title=title,
    all_review_ids="[%s]" % ",".join(str(r.id_) for r in reviews))
  return full_html.encode("utf-8")
