#! /usr/bin/python

from __future__ import print_function

from bs4 import BeautifulSoup
import getpass
import requests
import re
import sys

from common import parse_util
from common import progress


# Credentials
USERNAME = None
PASSWORD = None

# Cookies used by the Judge Center
SESSION_COOKIE = "ASP.NET_SessionId"
AUTH_COOKIE = "JudgeCenter.AspxAuth"

# URLs
JUDGE_CENTER_URL = "https://judge.wizards.com/"
LOGIN_URL = JUDGE_CENTER_URL + "login.aspx"

# Constants for navigating around the Judge Center
BTN_FINISH = "btnFinish"
BTN_OR = "btnOr"
DROPDOWN_LIST = "columnDropDownList"
LINK_FIRST = "ucDataGridPagerLinksBottom.lkbFirst"
LINK_NEXT = "ucDataGridPagerLinksBottom.lkbNext"
RELATION_DROPDOWN = "relationTypeDropDownList"
TEXT_BOX = "userValueTextBox"
USER_DROPDOWN = "userValueDropDownList"
MANY_RESULTS_RE = re.compile("Results ([0-9]+)-([0-9]+) of ([0-9]+).")
FEW_RESULTS_RE = re.compile("([0-9]+) results?.")

# Javascript extractor tools
POSTBACK_RE = re.compile("javascript:__doPostBack\('([^']*)','([^']*)'\)")
TIMEOUT_POSTBACK_RE = re.compile(
  "javascript:setTimeout\("
  "'__doPostBack\(\\\\'([^']*)\\\\',\\\\'([^']*)\\\\'\)'")


def error(*args):
  import sys
  for arg in args[:-1]:
    print(arg, end=' ', file=sys.stderr)
  if args:
    print(args[-1], file=sys.stderr)


def get_password():
  """Returns the user's password.

  On first use the user is prompted for their password on the command line.
  """
  global PASSWORD  # pylint: disable=W0603
  if PASSWORD is None:
    PASSWORD = getpass.getpass("Judge Center Password: ")
  return PASSWORD


def get_username():
  """Returns the user's username, usually their DCI Number.

  On first use the user is prompted for their username on the command line.
  """
  global USERNAME  # pylint: disable=W0603
  if USERNAME is None:
    USERNAME = raw_input("Your DCI Number: ")
  return USERNAME


class JudgeCenterSession(object):
  """Handle a session with the Judge Center and make requests.

  Because the JudgeCenter webpage is stateful using form variables and not only
  cookies, order of calling the forms is important. The public interface
  shouldn't require any unintuitive order and should be kept that way.
  Resetting filters is more easily done by starting a new session altogether.
  """

  # Constants for form input. Need to be exposed in subclasses.
  EQUALS = "Equals"
  LESS_THAN = "LessThan"
  GREATER_THAN = "GreaterThan"

  def __init__(self):
    self.text = ""  # The current HTML content of the select page.
    self.session = None
    self.page = 1
    self._make_session()
    self._post_make_session_hook()
    # TODO make a hook to navigate to appropriate page.

  def _get_base_url(self):
    """Gives the base page's URL for this type of session."""
    raise NotImplementedError

  def _make_session(self):
    """Initiates a new session with the Judge Center.

    Unless it expires, a single session is enough for any number of requests.
    """
    self.session = requests.Session()
    session_req = self.session.get(LOGIN_URL,
                                   params={"ReturnUrl": "/home.aspx"})
    fields = _get_fields(session_req.text)
    _add_login_info(fields)
    self.session.post(LOGIN_URL,
                      params={"ReturnUrl": "/home.aspx"},
                      data=fields)

  def _post_make_session_hook(self):
    """Override to have behavior just after the session is created."""
    pass

  def add_filter(self, filter_name, value, relation=None):
    """Adds a filter to the select page and submits with "Finish".

    Can be used to finish a partial filter.
    Args:
      - filter_name is the backend name of the filter.
      - value is the string value as typed in the text field.
      - relation is the relation to the value. One of EQUALS, LESS_THAN,
        GREATER_THAN.
    """
    if relation is None:
      relation = self.EQUALS
    self._add_filter_name(filter_name)
    self._input_value(value, relation)
    return self

  def add_filter_or(self, filter_name, value, relation=None):
    """Adds a filter to the select page and submits with "Or...".

    The filter should then be finished with optional other calls to
    add_filter_or() and one call to add_filter().
    Args:
      - filter_name is the backend name of the filter.
      - value is the string value as typed in the text field.
      - relation is the relation to the value. One of EQUALS, LESS_THAN,
        GREATER_THAN.
    """
    if relation is None:
      relation = self.EQUALS
    self._add_filter_name(filter_name)
    self._input_value_or(value, relation)
    return self

  def get(self, item_limit=0):
    """Returns items corresponding to the current filters.

    Navigates to next page as needed. Returns to page 1 after all items
    have been consumed.
    Args:
      - item_limit is the maximum number of items to extract (no limit if 0)
    Returns:
      - a list of types.Expandable
    """
    result = []
    if item_limit:
      item_total = min(item_limit, _get_result_count(self.text))
    else:
      item_total = _get_result_count(self.text)
    messages = progress.Messages()
    for i, html_item in enumerate(self._get_html_items()):
      item = self._item_parser()(html_item)
      messages.log(u"(%s/%s) %s" %
                   (i + 1, item_total, self._item_repr(item)))
      result.append(item)
      if item_limit and i + 1 >= item_limit:
        self._navigate_to_page_1()
        break
    messages.log(self._end_message() % item_total)
    messages.finish()
    return result

  def _item_parser(self):
    """Returns a function that can parse an html_item into an item."""
    raise NotImplementedError

  def _item_repr(self, item):
    """Returns a human-readable message for progress on downloading item."""
    raise NotImplementedError

  def _end_message(self):
    """Returns a human-readable message for successful end of downloading.

    Should include a single placeholder for the number of items.
    """
    raise NotImplementedError

  def _get_html_items(self):
    """Yields items corresponding to the current filters.

    Navigates to next page as needed. Returns to page 1 after all items
    have been consumed.
    Yields:
      - HTML representation of an item.
    """
    self.page = 1
    error("%s results" % _get_result_count(self.text))
    for item in self._get_items_on_page():
      yield item
    next_page_link = _get_next_page_link(self.text)
    while next_page_link:
      fields = _extract_postback_args(self.text, next_page_link['href'])
      self._post_form(fields)
      self.page += 1
      for item in self._get_items_on_page():
        yield item
      next_page_link = _get_next_page_link(self.text)
    self._navigate_to_page_1()

  def _navigate_to_page_1(self):
    if self.page == 1:
      return
    first_page_link = _get_first_page_link(self.text)
    if not first_page_link:
      error("No first page link")
    else:
      fields = _extract_postback_args(self.text, first_page_link['href'])
      self.page = 1
      self._post_form(fields)

  def _remove_filter(self, filter_text):
    """Removes the filter given its text.

    Does nothing if filter wasn't active.
    """
    filter_tag = self._get_filter(filter_text)
    if filter_tag is None:
      error("No filter tag")
      # The filter wasn't present, nothing to do
      return
    filter_button = filter_tag.previous_sibling.find('a')
    if not filter_button:
      error("No button")
      return
    fields = _extract_postback_args(self.text, filter_button['href'])
    self._post_form(fields)

  def _get_filter(self, filter_text):
    """Returns filter element by the text displayed next to the filter."""
    soup = BeautifulSoup(self.text)
    for td_tag in soup.find_all('td'):
      if td_tag.string is None:
        continue
      if td_tag.string.strip() == filter_text:
        return td_tag
    return None

  def _get_items_on_page(self):
    """Yields displayed items, without navigating to other pages."""
    soup = BeautifulSoup(self.text)
    for tr_tag in soup.find_all('tr'):
      if tr_tag.get('onclick') is None:
        continue
      fields = _extract_postback_args(self.text, tr_tag['onclick'])
      yield self._post_form_stateless(fields)

  def _add_filter_name(self, filter_name):
    """Adds a filter to the select page.

    The returned page is ready to receive a value for the filter and be
    submitted with "Finish" or "Or..." to continue the filter.
    It is safe to call this no matter the current value in the filter
    dropdown. It is also safe to use it for a continuation filter.
    Args:
      - filter_name is the backend name of the filter.
    """
    fields = _get_fields(self.text)
    filter_dropdown = _get_filter_dropdown(self.text)
    if filter_dropdown is None:
      error("No filter dropdown")
      return
    fields = _extract_postback_args(self.text, filter_dropdown['onchange'])
    fields[filter_dropdown['name']] = filter_name
    self._post_form(fields)

  def _input_value(self, value, relation):
    """Inputs the given value into the appropriate text box.

    The select page should curently have a filter selected.
    Submits the form with "Finish".
    Args:
      - value is a textual value.
      - relation is the relation to the value. One of EQUALS, LESS_THAN,
        GREATER_THAN.
    """
    self._input_value_with_btn(value, relation, BTN_FINISH)

  def _input_value_or(self, value, relation):
    """Inputs the given value into the appropriate text box.

    The select page should curently have a filter selected.
    Submits the form with "Or...". The response should then receive a new filter
    with add_filter().
    Args:
      - value is a textual value.
      - relation is the relation to the value. One of EQUALS, LESS_THAN,
        GREATER_THAN.
    """
    self._input_value_with_btn(value, relation, BTN_OR)

  def _input_value_with_btn(self, value, relation, btn_name):
    """Inputs the given value into the appropriate text box.

    The select page should curently have a filter selected.
    Submits the form.
    Args:
      - value is a textual value.
      - relation is the relation to the value. One of EQUALS, LESS_THAN,
        GREATER_THAN.
      - btn_name is the name of the button to submit with.
    """
    self.page = 1
    value_box = _get_user_value_box(self.text)
    if value_box is None:
      value_box = _get_user_value_dropdown(self.text)
      if value_box is None:
        error("No value box")
        return
    fields = _get_fields(self.text, btn_name)
    fields[value_box['name']] = value
    if relation != self.EQUALS:
      relation_box = _get_user_relation_box(self.text)
      if relation_box is None:
        error("No relation box but relation different from EQUALS requested.")
      fields[relation_box['name']] = relation
    self._post_form(fields)

  def _post_form(self, fields):
    """Posts completed form."""
    resp = self.session.post(self._get_base_url(), data=fields)
    self.text = resp.text.encode(resp.encoding)

  def _post_form_stateless(self, fields):
    """Posts completed form and returns HTML instead of modifying state."""
    resp = self.session.post(self._get_base_url(), data=fields)
    return resp.text.encode(resp.encoding)

  def select_tab(self, fields, tab_number):
    """Simulate a click on one of the tabs (view, select, etc.).

    tab_number is 1-base.
    """
    fields["___dpmt__mt_ts_State__"] = tab_number
    _add_postback_args(fields, "_dpmt$_mt$ts", "%d" % tab_number)
    self._post_form(fields)


def _get_fields(text, multi_submit_name=""):
  """Extract fields from HTML text.

  If multiple submit buttons exist and multi_submit_name is set to a regexp,
  all matching submits will be added.
  If multiple submit buttons exist and multi_submit_name is "",
  no submits are added.
  """
  soup = BeautifulSoup(text)
  field_dico = {}
  submit_dico = {}
  for input_ in soup.findAll("input"):
    key = input_.get('name', input_.get('id'))
    if key is None:
      error("Wrong input field", repr(input_))
      continue
    if input_.get('type') == "submit":
      submit_dico[key] = input_.get('value', '')
    else:
      field_dico[key] = input_.get('value', '')
  for select in soup.findAll("select"):
    key = select.get('name', select.get('id'))
    if key is None:
      error("Wrong input field", repr(select))
      continue
    for option in select.find_all('option'):
      if option.get('selected'):
        field_dico[key] = option.get('value', '')
        break
  if len(submit_dico) == 1:
    field_dico.update(submit_dico)
  elif len(submit_dico) > 1 and multi_submit_name:
    for key in submit_dico.keys():
      if not re.search(multi_submit_name, key):
        del submit_dico[key]
    field_dico.update(submit_dico)
  return field_dico


def _add_login_info(field_dico):
  field_dico['ctl00$phMainContent$DCINumberTextBox'] = get_username()
  field_dico['ctl00$phMainContent$PasswordTextBox'] = get_password()
  field_dico['TimeZoneOffset'] = '-60'


def _extract_postback_args(text, script):
  """Return form fields corresponding to execution of given javascript."""
  javascript = TIMEOUT_POSTBACK_RE.search(script)
  if javascript is None:
    javascript = POSTBACK_RE.search(script)
    if javascript is None:
      error("Wrong button", script)
      return
  fields = _get_fields(text)
  _add_postback_args(fields, javascript.group(1), javascript.group(2))
  return fields


def _add_postback_args(fields, target, arg):
  """Fill the form fields with arguments from __doPostBack."""
  fields["__EVENTTARGET"] = target
  fields["__EVENTARGUMENT"] = arg


def _get_filter_dropdown(text):
  return parse_util.get_tag_by_field(text, 'select', 'id', DROPDOWN_LIST)


def _get_user_value_box(text):
  return parse_util.get_tag_by_field(text, 'input', 'id', TEXT_BOX)


def _get_user_value_dropdown(text):
  return parse_util.get_tag_by_field(text, 'select', 'id', USER_DROPDOWN)


def _get_user_relation_box(text):
  return parse_util.get_tag_by_field(text, 'select', 'id', RELATION_DROPDOWN)


def _get_next_page_link(text):
  return parse_util.get_tag_by_field(text, 'a', 'href', LINK_NEXT)


def _get_first_page_link(text):
  return parse_util.get_tag_by_field(text, 'a', 'href', LINK_FIRST)


def _get_result_count(text):
  div_count = parse_util.get_tag_by_field(text, 'div', 'class', "results")
  if not div_count:
    error("No results tag found.")
    return 0
  match = MANY_RESULTS_RE.match(div_count.stripped_strings.next())
  if match:
    return int(match.group(3))
  match = FEW_RESULTS_RE.match(div_count.stripped_strings.next())
  if match:
    return int(match.group(1))
  return 0
