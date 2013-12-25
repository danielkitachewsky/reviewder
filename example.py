#! /usr/bin/python
# encoding: utf-8

import format
import review_types


LOREM_IPSUM = u"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum et urna non urna pretium congue. Ut pretium urna dapibus laoreet rhoncus. Duis semper at neque ut tempus. Mauris eget felis risus. Ut accumsan ullamcorper nunc quis rhoncus. Morbi sem felis, lacinia quis risus in, vestibulum mattis libero. Proin tortor turpis, cursus ac cursus ut, vestibulum non sapien. Curabitur eget pulvinar lorem, at suscipit enim. Duis sollicitudin magna auctor feugiat malesuada. Mauris viverra libero ut metus scelerisque venenatis. In elit diam, tincidunt et placerat sit amet, adipiscing ut sapien. Cras aliquet, tellus a congue suscipit, urna odio fermentum tellus, et aliquam risus purus at tortor.<br/>
<br/>
Donec mi eros, rutrum a ultricies sed, convallis quis nulla. Integer pretium laoreet laoreet. Nullam sed ullamcorper sem. Donec iaculis a mi eleifend dapibus. Maecenas vulputate massa vitae mauris laoreet imperdiet. Proin metus tellus, venenatis vitae blandit in, euismod nec lorem. Nulla id sagittis ligula, at egestas velit. Mauris sit amet eros vel purus pharetra tempor. Sed sit amet massa luctus tortor sollicitudin volutpat non blandit dolor. Sed dapibus leo a sodales volutpat. Nullam dignissim eros vitae velit ultricies porta. Pellentesque at ante sapien.<br/>
<br/>
Morbi nec erat et nibh sollicitudin mattis. Donec accumsan urna tempor velit consectetur venenatis. Cras dui tellus, luctus quis turpis a, luctus lobortis ipsum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Maecenas faucibus iaculis leo, a eleifend dui suscipit quis. Maecenas quis sagittis ipsum. Phasellus at tellus venenatis, feugiat ipsum tincidunt, mollis augue. Curabitur hendrerit dolor vel magna varius, sed adipiscing ante tincidunt. Donec feugiat lorem neque, ac fermentum ligula euismod sit amet. Maecenas rutrum pretium eros. Vestibulum vehicula mattis ornare.<br/>
"""

def main():
  reviews = [
    review_types.Review(
      1,
      observer=u"Daniel",
      subject=u"Pépito",
      strengths=u"Zéro.",
      afi=u"Nada.",
      comments=u"гы-гы"),
    review_types.Review(
      2,
      observer=u"Daniel",
      subject=u"Sito",
      strengths=u"Bike.",
      afi=u"Knee.",
      comments=LOREM_IPSUM),
    review_types.Review(
      3,
      observer=u"Daniel",
      subject=u"Jens",
      strengths=u"Surgery.",
      afi=u"Presence.",
      comments=u"Grüß Gott"),
    review_types.Review(
      4,
      observer=u"Sauron",
      subject=u"Daniel",
      strengths=u"Roolz.",
      afi=u"Javascript.",
      comments=u"Lorem ipsum"),
    ]

  rendered_reviews = [
    format.render_template("review.html", review=review)
    for review in reviews]
  full_html = format.render_template(
    "reviews.html", body="".join(rendered_reviews), title="Reviews")
  print full_html.encode("utf-8")


if __name__ == "__main__":
  main()
