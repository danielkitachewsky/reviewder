
import base64
import os

from reviewder import format


COLOR_YELLOW = "#ffff88"
COLOR_GREEN = "#aaffaa"
COLOR_PINK = "#ffaaaa"
COLOR_BLUE = "#ccccff"
COLOR_WHITE = "#ffffff"


def _get_file_by_name(dir_, name):
  """Finds the file with given name relative to this module."""
  # HACK to fall back on our feet when deployed through py2exe
  here = os.path.dirname(os.path.abspath(__file__))
  if "\\" in here:
    while "library.zip" in here:
      here = "\\".join(here.split("\\")[:-1])
  return os.path.join(here, dir_, name)


def _get_template(name):
  """Finds the template with given name relative to this module."""
  return _get_file_by_name("templates", name)


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


def _is_no_promotion(review):
  return review.new_level == review.existing_level


def _is_promotion(review):
  return review.new_level and review.new_level > review.existing_level


def _is_demotion(review):
  return review.new_level and review.new_level < review.existing_level


def _is_renewal(review):
  return review.type_ == "Renewal"


def _get_icon(name):
  filename = _get_file_by_name("icons", name)
  filetype = name.split(".")[-1]
  with open(filename, "rb") as f:
    binary_data = f.read()
  encoded_data = base64.b64encode(binary_data)
  src = "data:image/%s;base64,%s" % (filetype, encoded_data)
  return '<img class="noprint icon" src="%s">' % src


REVIEW_TYPES = [
  (_is_promotion, "Certification", _get_icon("chart_up_color.png")),
  (_is_no_promotion, "Certification", ""),
  (_is_demotion, "Certification", _get_icon("chart_down_color.png")),
  (_is_recommendation, "(maybe) Recommendation", _get_icon("tick.png")),
  (_is_renewal, "Renewal", _get_icon("cake.png")),
  (_is_self_review, "Self-Review", _get_icon("dashboard.png")),
  ]


def _type_icon(review):
  for criterion, _, icon_html in REVIEW_TYPES:
    if criterion(review) and icon_html:
      return icon_html
  return '<span class="no-icon"></span>'


def _make_legend(reviews):
  legends_needed = []
  for criterion, label, icon_html in REVIEW_TYPES:
    if any(criterion(review) for review in reviews):
      legends_needed.append((label, icon_html))
  if not legends_needed:
    return ''
  result = '<div class="noprint"><br>Legend:'
  for label, icon_html in legends_needed:
    result += ('<br>%s%s'
               % (icon_html, label))
  return result + "</div>"


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


RATINGS = {
  "Average": "",
  "Above Average": "above",
  "Outstanding": "outstanding",
  "Below Average": "below",
  }


def _rated_class(review):
  """Returns a CSS class according to the rating."""
  if review.type_ == "Renewal":
    # These don't include a rating, so we don't show anything
    return ""
  return RATINGS[review.comparison]


def render_review(review):
  return format.render_template(_get_template("review.html"),
                                review=review,
                                type_icon=_type_icon(review),
                                reviewer_level=_reviewer_level(review),
                                subject_level=_subject_level(review),
                                exam_score=_exam_score(review),
                                rated=_rated(review),
                                rated_class=_rated_class(review),
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
