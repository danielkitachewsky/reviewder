#! /usr/bin/python
# encoding: utf-8

import format
import importer
import review_types


def main():
  reviews = [
    importer.parse_html_review(open("brefka.html")),
    importer.parse_html_review(open("hiller.html")),
    ]

  rendered_reviews = [
    format.render_template("review.html", review=review)
    for review in reviews]
  full_html = format.render_template(
    "reviews.html", body="".join(rendered_reviews), title="Reviews",
    all_review_ids="[%s]" % ",".join(str(r.id_) for r in reviews))
  print full_html.encode("utf-8")


if __name__ == "__main__":
  main()
