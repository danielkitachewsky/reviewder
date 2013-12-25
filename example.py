#! /usr/bin/python
# encoding: utf-8

import format
import review_types


def main():
  review_id = 1
  review = review_types.Review(review_id,
                               observer=u"Daniel",
                               subject=u"Pepito",
                               strengths=u"Zéro.",
                               afi=u"Nada.",
                               comments=u"гы-гы")
  text = format.render_template("review.html", review=review)
  print text.encode("utf-8")


if __name__ == "__main__":
  main()
