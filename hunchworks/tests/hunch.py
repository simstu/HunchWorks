#!/usr/bin/env python

from hunchworks.models import Hunch, Evidence, HunchEvidence, Vote
from hunchworks.tests.helpers import ViewTestHelpers, UnitTestHelpers
from django.test import TestCase


class HunchTest(TestCase, UnitTestHelpers):
  fixtures = ("test_users", "test_hunches")

  def setUp(self):
    self.hunch = Hunch.objects.get(pk=1)


  # helpers

  def _evidence(self, strong_refs, weak_refs, neutrals, weak_sups, strong_sups):
    evidence = Evidence.objects.create(creator=self._user().get_profile(), link="http://example.com")
    hunch_evidence = HunchEvidence.objects.create(hunch=self.hunch, evidence=evidence)
    self._vote(hunch_evidence, -2, strong_refs)
    self._vote(hunch_evidence, -1, weak_refs)
    self._vote(hunch_evidence, 0,  neutrals)
    self._vote(hunch_evidence, +1, weak_sups)
    self._vote(hunch_evidence, +2, strong_sups)

  def _vote(self, hunch_evidence, choice, times=1):
    for n in range(times):
      Vote.objects.create(
        hunch_evidence=hunch_evidence,
        user_profile=self._user().get_profile(),
        choice=choice)


  # actual tests

  def test_hunch_support_defaults_to_neutral(self):
    self.assertEqual(self.hunch.get_support_text(), "Neutral")

  def test_mild_hunch_support(self):
    self._evidence(0, 0, 0, 2, 0)
    self.assertEqual(self.hunch.get_support_text(), "Mildly Supported")

  def test_strong_hunch_support(self):
    self._evidence(2, 2, 0, 4, 20)
    self.assertEqual(self.hunch.get_support_text(), "Strongly Supported")

  def test_mild_hunch_refute(self):
    self._evidence(2 ,8 ,0 ,4 ,0)
    self.assertEqual(self.hunch.get_support_text(), "Mildly Refuted")

  def test_strong_hunch_refute(self):
    self._evidence(16 ,4 ,2 ,4 ,0)
    self.assertEqual(self.hunch.get_support_text(), "Strongly Refuted")


  def test_hunch_controversy_defaults_to_zero(self):
    self.assertEqual(self.hunch.get_controversy_text(), "Uncontroversial")

  def test_minimum_hunch_controversy(self):
    self._evidence(10, 0, 0, 0, 0)
    self.assertEqual(self.hunch.get_controversy_text(), "Uncontroversial")

  def test_low_hunch_controversy(self):
    self._evidence(10, 0, 0, 0, 1)
    self.assertEqual(self.hunch.get_controversy_text(), "Somewhat Controversial")

  def test_high_hunch_controversy(self):
    self._evidence(10, 0, 0, 0, 5)
    self._evidence(10, 0, 0, 0, 5)
    self.assertEqual(self.hunch.get_controversy_text(), "Controversial")

  def test_maximum_hunch_controversy(self):
    self._evidence(10, 0, 0, 0, 0)
    self._evidence(0, 0, 0, 0, 10)
    self.assertEqual(self.hunch.get_controversy_text(), "Very Controversial")


  def test_activity_defaults_to_inactive(self):
    self.assertEqual(self.hunch.get_activity_text(), "Inactive")

  def test_low_activity(self):
    self._evidence(0, 0, 1, 0, 0)
    self.assertEqual(self.hunch.get_activity_text(), "Active")

  def test_high_activity(self):
    self._evidence(2, 2, 2, 2, 2)
    self.assertEqual(self.hunch.get_activity_text(), "Very Active")




class HunchViewsTest(TestCase, ViewTestHelpers):
  fixtures = ("test_users", "test_hunches")

  def test_redirect_to_all_hunches(self):
    with self.login("one"):
      resp = self.get("hunches")
      self.assertRedirects(resp, "/hunches/all")

  def test_redirect_to_my_hunches(self):
    with self.login("two"):
      resp = self.get("hunches")
      self.assertRedirects(resp, "/hunches/my")

  def test_all_hunches(self):
    with self.login("one"):
      resp = self.get("all_hunches")
      self.assertQuery(resp, "article.hunch", count=2)

  def test_my_hunches(self):
    with self.login("two"):
      resp = self.get("my_hunches")
      self.assertQuery(resp, "article.hunch", count=1)
  
  def test_show_hunch(self):
    with self.login("one"):
      hunch = Hunch.objects.get(pk=1)
      resp = self.get("hunch", hunch_id=hunch.pk)
      self.assertContains(resp, hunch.title)

  def test_edit_hunch(self):
    with self.login("one"):
      old_hunch = Hunch.objects.get(pk=1)
      get_resp = self.get("edit_hunch", hunch_id=1)
      self.assertTemplateUsed(get_resp, "hunches/edit.html")

      post_resp = self.submit_form(get_resp, {
        "title": "Test Edit Hunch"
      })

      new_hunch = Hunch.objects.get(pk=1)
      self.assertEqual(new_hunch.title, "Test Edit Hunch")
      self.assertEqual(old_hunch.description, new_hunch.description)
      self.assertRedirects(post_resp, new_hunch.get_absolute_url())

  def test_follow_hunch(self):
    with self.login("two"):
      resp = self.get("my_hunches")
      self.assertQuery(resp, "article.hunch", count=1)

      old_hunch = Hunch.objects.get(pk=2)
      get_resp = self.get("follow_hunch", hunch_id=old_hunch.id)
 
      resp2 = self.get("my_hunches")
      self.assertQuery(resp2, "article.hunch", count=2)

  def test_unfollow_hunch(self):
    with self.login("two"):
      resp = self.get("my_hunches")
      self.assertQuery(resp, "article.hunch", count=1)

      old_hunch = Hunch.objects.get(pk=1)
      get_resp = self.get("unfollow_hunch", hunch_id=old_hunch.id)

      resp2 = self.get("my_hunches")
      self.assertQuery(resp2, "article.hunch", count=0)

#   def test_vote(self):
#     with self.login("two")
#       hunch = Hunch.objects.get(pk=1)
#       get_resp = self.get("hunch", hunch_id=hunch.pk)
#       
#       post_resp = self.submit_form(get_resp, {
#         "action": "vote",
#         "choice": 1
#       })
#       
#       vote = Vote.objects.get(pk=1)
#       
#       self.assertRedirects(post_resp, new_hunch.get_absolute_url())
#       