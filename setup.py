
from distutils.core import setup
import py2exe

setup(console=["main.py"],
      data_files=[("templates", [
        "reviewder/templates/review.html",
        "reviewder/templates/reviews.html",
        ])],
      )
