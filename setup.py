
from distutils.core import setup
import py2exe

setup(console=["main.py"],
      data_files=[("templates", [
        "reviewder/templates/review.html",
        "reviewder/templates/reviews.html",
        ]),
                  ("icons", [
        "reviewder/icons/cake.png",
        "reviewder/icons/chart_down_color.png",
        "reviewder/icons/chart_line.png",
        "reviewder/icons/chart_up_color.png",
        "reviewder/icons/dashboard.png",
        "reviewder/icons/tick.png",
        ]),
                  ("", ["README.txt"]),
                  ])
