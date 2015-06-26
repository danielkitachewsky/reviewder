
from common import session
from reviewder import importer

REVIEW_URL = session.JUDGE_CENTER_URL + "reviews.aspx"

ONLY_ME_FILTER_TEXT = "Entered By DCI Number is equal to {0}," \
    " or Reviewer DCI Number is equal to {0}," \
    " or Subject DCI Number is equal to {0}"


class JudgeCenterReviewsSession(session.JudgeCenterSession):
  """Handle a session with the Judge Center for downloading reviews."""

  def _get_base_url(self):
    return REVIEW_URL

  def _post_make_session_hook(self):
    """Sets the session to review select mode."""
    review_home_req = self.session.get(REVIEW_URL)
    fields = session._get_fields(review_home_req.text)
    self.select_tab(fields, 3)
    self._remove_filter(ONLY_ME_FILTER_TEXT.format(session.get_username()))

  def _item_parser(self):
    return importer.parse_html_review

  def _item_repr(self, item):
    return u"Downloading review of %s on %s..." % (item.observer, item.subject)

  def _end_message(self):
    return u"Downloaded %s reviews."


# Review filter values
REVIEW_FILTERS = {
    "ReviewID": "ID",
    "EnteredByDisplayName": "Entered By",
    "EnteredByFirstName": "Entered By First Name",
    "EnteredByLastName": "Entered By Last Name",
    "EnteredByDCINumber": "Entered By DCI Number",
    "EnteredDate": "Entered",
    "ReviewDate": "Observed",
    "LanguageName": "Language",
    "ReviewerDisplayName": "Reviewer",
    "ReviewerFirstName": "Reviewer First Name",
    "ReviewerLastName": "Reviewer Last Name",
    "ReviewerDCINumber": "Reviewer DCI Number",
    "ReviewerLevelCd": "Reviewer Level",
    "ReviewerTournamentRoleName": "Reviewer Role",
    "ReviewerLanguageName": "Reviewer Language",
    "ReviewTypeName": "Type",
    "ReviewStatusName": "Status",
    "ReviewRatingName": "Comparison",
    "RecommendAdvancement": "Advancement",
    "EventTypeName": "Event Type",
    "EventLocation": "City",
    "CountryName": "Country",
    "ExamID": "Exam ID",
    "ExamScore": "Exam Score",
    "SubjectPersonID": "Subject Person ID",
    "SubjectDisplayName": "Subject",
    "SubjectFirstName": "Subject First Name",
    "SubjectLastName": "Subject Last Name",
    "SubjectDCINumber": "Subject DCI Number",
    "SubjectLevelCd": "Existing Level",
    "SubjectTournamentRoleName": "Subject Role",
    "NewLevelCd": "New Level",
    "Strengths": "Strengths",
    "Weaknesses": "Areas for Improvement",
    "Comments": "Comments",
    }
