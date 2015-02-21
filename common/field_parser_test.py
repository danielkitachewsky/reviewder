#! /usr/bin/python
# encoding: utf-8

from bs4 import BeautifulSoup
import unittest

from common import field_parser


INVESTIGATION_FIELDS = {u'City': u'Mexico City',
 u'Country': u'Mexico',
 u'Entered By': u'Daniel Kitachewsky',
 u'Entered By DCI Number': u'29870351',
 u'Entered Date': '2015-02-15',
 u'Event Type': u'Grand Prix',
 u'ID': u'5404',
 u'Incident Date': '2015-01-31',
 u'Infraction': u'Misrepresentation of game state or rule',
 u'REL': u'Competitive',
 u'Resolution': u'',
 u'Resolved By': u'',
 u'Sanctioning Number': u'15-01-5499598',
 u'Status': u'Submitted',
 u'Subject': u'Carlos Barrera',
 u'Subject DCI Number': u'1202634379',
 u'Subject Tournament Role': u'Player'}
REVIEW_FIELDS = {u'Areas for Improvement': u"STRESS AND CONFLICT MANAGEMENT\n <br/>\n During the Garruk scenario, you had great trouble keeping control - you seemed lost. You went in circles asking the same question over and over. While some of it can be attributed to the artificial setting of a role-play (and the fact that you knew you were being evaluated), it also shows you're not completely relaxed when answering a potentially messy judge call. You cited being more confident dealing with judges than belligerent players. This role-play was indeed a good show. Some tips below.\n <br/>\n <br/>\n INVESTIGATION\n <br/>\n During that same role play, you failed to ask even basic investigative questions to one of the player, who potentially was benefitting from the timing of the judge call. If the player had called a judge a moment prior, the ruling would have been greatly unfavorable to him, so his timing should have been seen as suspicious. At no moment did you question that.\n <br/>\n <br/>\n While judging competitive and professional events, you will be led to answer calls at difficult tables - with big name players who might be quite vocal, possibly on feature matches or on camera. These conditions might be as stressful as the L3 panel.\n <br/>\n <br/>\n Make sure you get the basics of judge calls right, even though you've answered hundreds of them. It's like swimming - you may have done thousands of laps, but still have an imperfect technique. Separate the phases of information collection, thinking/consulting, delivery of the ruling, and penalizing. Learn the tricks about protecting information - separate the players at the first sign of disagreement, so that they don't get a chance to talk and agree on a (false) turn of events. Interview the players aside from the table if it's simple or relates to body language; interview them at the table if you need to understand the board state either to establish what happened or what the motives of each player could be.\n <br/>\n <br/>\n On a side note, you've entered two DQs in the past which have led to no action by the suspension committee, meaning that they were either not DQable offenses or too hardline. Jan Zajac can talk to you about these if you haven't already done so.\n <br/>",
 u'City': u'Tanger',
 u'Comments': u'This review covers Fang\'s L3 panel at GP Tanger 2013.\n <br/>\n The panel was Tom Sawyer (lead), Gerrard Capashen, and Rabid Wombat (observer).\n <br/>\n Role-plays used: Unnaproved Disqualification, Garruks\n <br/>\n Garruk scenario is as follows:\n <br/>\n A player calls a judge complaining that his opponent had Garruk, Primal Hunter in play while himself had Garruk Relentless. Upon investigating, the candidate should discover that Garruk Relentless "fight" ability has just been activated to deal with a 3/3 beast and that Garruk Relentless is already in the graveyard. The judge should inquire the opponent as for whether and when he noticed that both Garruks were illegally in play. If questioned, the opponent should say they noticed some time ago, but thought it was fine under M14 rules. The correct resolution is to leave the game state as is since it\'s legal. Discussion can follow for the variant were Garruk Relentless is still in play with its ability on the stack.\n <br/>\n <br/>\n Determined minor deficiencies were Investigations and Stress &amp; Conflict Management, with all the rest being passes.\n <br/>\n <br/>\n Welcome to level 3, Fang. This is a well-deserved promotion that crowns a very good job done in Maghreb. This is by no means an end but rather the start of a new path. Don\'t hesitate to ask any question regarding your new level, including access to various resources (L3 forums, IRC, projects). Well done!\n <br/>',
 u'Comparison': u'Above Average',
 u'Country': u'Morocco',
 u'Entered': '2013-07-15',
 u'Entered By': u'Ul-Haq Qureshi',
 u'Event Type': u'Grand Prix',
 u'Exam ID': u'1012332',
 u'Exam Score': u'88 %',
 u'Existing Level': u'2',
 u'ID': u'49954',
 u'Language': u'English',
 u'New Level': u'3',
 u'Observed': '2010-07-02',
 u'Reviewer': u'Ul-Haq Qureshi',
 u'Reviewer Level': u'3',
 u'Reviewer Role': u'',
 u'Status': u'Submitted',
 u'Strengths': u"RULES AND POLICY KNOWLEDGE\n <br/>\n You scored 88% on the written test, which demonstrates excellent knowledge. While not a guru-level score, you are able to comfortably answer almost any question that could arise on a tournament. The speed with which you completed the test was also impressive. In the several discussions we've had over the week-end, your answers were quick and natural, showing you have real understanding of what's behind the rules rather than just surface knowledge of a collection of situations; this will prove valuable in explaining the rules to other judges.\n <br/>\n <br/>\n LEADERSHIP, PRESENCE &amp; CHARISMA\n <br/>\n You've successfully stepped up as a leader in Maghreb since Mohammed Ali reduced his activity. Many judges in that region now see you as their leader and players ask questions whenever you're not head judging an event. These elements demonstrate that you've established yourself as a reference and that judges will naturally seek your advice. Furthermore, two L3s, Chong Qing and Rudolph Underhill, have moved recently to the region. You've seen their coming as welcome help rather than competition, which is the right attitude. There is no set number of L3s a region should have; rather, there is space for everyone and not every L3 might have the same interests. Cooperation is the way to go.\n <br/>\n <br/>\n MENTORSHIP\n <br/>\n This is possibly your strongest point. You've certified a boatload of level 1s which is a great boost to the region. The next step is to train and certify L2s who in turn are able to certify other judges. Marrakech has a number of L2s a bit lower than desired (you ideally want one L2 for every 5 L1s), so that's certainly a project you'll take part in. You've also contributed a lot to growing Paul Baranay who is now one of the stronger L2s in your region and possibly a future L3 candidate. Keep it up!\n <br/>\n <br/>\n COMMUNICATION\n <br/>\n Your level of English is simply amazing. You manage to express ideas efficiently and in an interesting manner. The only downside is you're a bit verbose, but that's a very acceptable downside!\n <br/>\n <br/>\n JUDGE PROGRAM PHILOSOPHY\n <br/>\n Your description of levels 1, 2 and 3 are quite spot on. Furthermore, you highlighted one problem with the current levels and judging Grand Prix Trials. This shows that you don't merely know the definitions but also understand the reasons for their existence and their limitations.\n <br/>\n <br/>\n JUDGE ASSESSMENT\n <br/>\n Your reviews are good, they're well explained, hit both strengths and areas for improvement, and most of the time offer concrete advice on how to improve. A possible path to improvement is to make sure that advice is always present and relevant to the judge. Learn to tell apart judges who have a genuine desire to improve (and thus will listen to direct advice) and those who are satisfied with where they are (and might benefit from more indirect advice, such as supplemental activities). One of my own weak areas was understanding which points of a tournament were potential time bottlenecks. Rather than explaining that to me, my mentor asked me to write an article about critical moments in a tournament - I did it and learned much more about time-saving tricks than I could have form a good old school-like lesson.\n <br/>\n <br/>\n PENALTY/POLICY PHILOSOPHY\n <br/>\n You reached the correct conclusion in the Garruk scenario (see description of this scenario in the Comments as this is a non-standard one). You also did relevant analysis on the variations and also offered an interesting interpretation of it (the activation of Garruk was illegal as the player didn't hold priority at that point, so assessing a GRV and backing up to that point is sensible).\n <br/>\n <br/>\n You presented a seminar on Missed Triggers in the past which has been well-received and demonstrates good understanding of that policy. As long as you keep a critical view on policy rather than blindly accepting it, you will be doing fine on this Quality.\n <br/>\n <br/>\n TEAMWORK AND DIPLOMACY\n <br/>\n Your handling of the failing judge scenario was quite good. You understood well the social dynamics at hand and steered the various people into the right direction without being aggressive or confrontational - however bad the mistakes may be. You're generally reliable on events and know when to do just your job and when and it's ok to overstep boundaries and take initiative. Beware though of antagonistic reactions like your interaction with Ali Baba and Grand Prix Cairo. Even though you meant it as a joke, your refusal to perform a task left quite a negative impression on Ali - not to mention any lower-level judges who could have witnessed it. Actions speak for themselves, and that's even more true at higher levels when everything you do might undergo public scrutiny. We're positive that you're not going to repeat this kind of behavior in the future.\n <br/>\n <br/>\n SELF EVALUATION SKILLS\n <br/>\n You're able to correctly assess you strengths and weaknesses. The next step is to shift the prism from that of an L3 candidate to an L3 proper, and assess yourself against the latter standards. Make sure you always have one or two aspects you're working on, at least as a background activity. If at any point you find yourself unable to put anything in areas for improvement, I'd be very interested to hear it!\n <br/>\n <br/>\n ATTITUDE AND MATURITY\n <br/>\n We had concerns raised about your attitude by Bob in the recent months. This is a new phenomenon and is not alarming yet, but it's definitely a change from previous impressions on you. Make sure you keep inappropriate jokes at a minimum. As you're aware, being an L3 makes it so that everything you do (even when not judging) is liable to be seen and copied by others. We got the impression that you are able to adjust quickly and are confident that walking out of the panel you were already set, making this a pass rather than a minor deficiency.\n <br/>",
 u'Subject': u'Long Fang',
 u'Subject Role': u'',
 u'Type': u'Interview'}


class FieldParseTestCase(unittest.TestCase):
  def test_parse_investigation(self):
    filename = "common/testdata/case_complete.html"
    soup = BeautifulSoup(open(filename))
    investigation = field_parser.parse_summary_fields(soup)
    self.assertDictContainsSubset(INVESTIGATION_FIELDS, investigation)

  def test_parse_review(self):
    filename = "common/testdata/promotion.html"
    soup = BeautifulSoup(open(filename))
    review = field_parser.parse_summary_fields(soup)
    self.assertDictContainsSubset(REVIEW_FIELDS, review)

if __name__ == "__main__":
  unittest.main()
