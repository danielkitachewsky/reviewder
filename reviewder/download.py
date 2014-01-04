#! /usr/bin/python

from reviewder import review_types


class DownloadError(review_types.Error):
  """Generic error raised during downloading of reviews."""


def download_reviews(ids):
  """Downloads the reviews with the given set of ids.
  
  ids correspond to the review id in the Judge Center.
  Permissions or other issues may cause some of the reviews not to download.
  In that case, the corresponding ok flag will be False, but no exception will
  be raised.
  Args:
    - ids is a list of integer ids.
  Returns:
    - a list or pairs [(review, ok)] where review is a review_types.Review and ok
    is either True for successful download and False in case of error. In case
    of error review will be None.
  """
  result = []
  for id_ in ids:
    try:
      review = download_review(id_)
      result.append((review, True))
    except DownloadError:
      result.append((None, False))


def download_review(id_):
  """Downloads the reviews with the given id_.
  
  id_ corresponds to the review id in the Judge Center. Permissions or other
  issues may cause the review not to download. In that case, DownloadError
  will be raised.
  Args:
    - id_ is an integer id.
  Returns:
    - a review_types.Review.
  """
  # TODO implement
  return review_types.Review(1, observer="Daniel", subject="Pepito",
                             strengths="None", afi="All",
                             comments="Lorem ipsum")

