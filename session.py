#! /usr/bin/python

from bs4 import BeautifulSoup
import getpass
import requests
from urllib import quote_plus

# Credentials
USERNAME = "29870351"
PASSWORD = None

# Cookies used by the Judge Center
SESSION_COOKIE = "ASP.NET_SessionId"
AUTH_COOKIE = "JudgeCenter.AspxAuth"

# URLs
JUDGE_CENTER_URL = "http://judge.wizards.com/"
LOGIN_URL = JUDGE_CENTER_URL + "login.aspx"
REVIEW_URL = JUDGE_CENTER_URL + "reviews.aspx"


def getPassword():
  global PASSWORD
  if PASSWORD is None:
    PASSWORD = getpass.getpass()
  return PASSWORD


class JudgeCenterSession(object):
  """Handle a session with the Judge Center and make requests."""
  def __init__(self):
    self._make_session()

  def _make_session(self):
    """Initiates a new session with the Judge Center.

    Unless it expires, a single session is enough for any number of requests.
    """
    self.session = requests.Session()
    session_req = self.session.get(LOGIN_URL,
                                   params={"ReturnUrl": "/home.aspx"})
    self.session_id = session_req.cookies[SESSION_COOKIE]
    fields = _get_fields(session_req.text)
    _add_login_info(fields)
    login_resp = self.session.post(LOGIN_URL,
                                   params={"ReturnUrl": "/home.aspx"},
                                   data=fields)
    self.auth = login_resp.cookies[AUTH_COOKIE]

  def get_review_html(self, review_id):
    """Download a review by its ID."""
    req = requests.Request("GET", REVIEW_URL, params={"id": str(review_id)})
    resp = self.session.get(REVIEW_URL, params={"id": str(review_id)})
    return resp.text.encode(resp.encoding)


def _get_fields(text):
  """Extract fields from HTML text."""
  soup = BeautifulSoup(text)
  field_dico = {}
  for input_ in soup.findAll("input"):
    key = input_.get('name', input_['id'])
    field_dico[key] = input_.get('value', '')
  return field_dico


def _add_login_info(field_dico):
  field_dico['ctl00$phMainContent$DCINumberTextBox'] = USERNAME
  field_dico['ctl00$phMainContent$PasswordTextBox'] = getPassword()
  field_dico['TimeZoneOffset'] = '-60'

