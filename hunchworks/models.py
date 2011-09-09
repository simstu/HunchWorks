#!/usr/bin/env python

import datetime
import hunchworks_enums
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

GENDER_CHOICES = (
  ('M', 'Male'),
  ('F', 'Female'),
)


class Album(models.Model):
  """Class representing a collection of pictures in an album"""
  name = models.CharField(max_length=45)


class Attachment(models.Model):
  """Class representing an attachment for a hunch"""
  attachment_type = models.IntegerField()
  file_location = models.CharField(max_length=100)
  albums = models.ManyToManyField('Album', through='AlbumAttachments')


class AlbumAttachments(models.Model):
  """Many to Many model joining Album and attachments"""
  album = models.ForeignKey(Album)
  attachment = models.ForeignKey(Attachment)


class Class(models.Model):
  """Class representing a educational class taken that may or may not have
  been at a college"""
  name = models.CharField(max_length=45)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)


class Education(models.Model):
  """Class representing a degree or qualification obtained by a user."""
  school = models.CharField(max_length=255)
  qualification = models.CharField(max_length=100)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)


class Language(models.Model):
  """Class representing a language supported by the application.

  This table is provided during development to ease integration of i18n and
  translation features. It provides a mapping from a purported language code to
  the actual language code to use. This allows us to use English by default
  everywhere, whilst plumbing in the i18n architecture from the beginning.

  Languages are coded per the Django global_settings module
  (http://goo.gl/sp5OI), rather than the full i18n values (http://goo.gl/DgmM).
  Django uses one level language tags generally, in this application these map
  to:
  1. en: en-US (use US English)
  2. es: es-ES (use Iberian Spanish)
  3. fr: fr-FR
  4. de: de-DE
  5. zh-cn: zh-cn (use simplified Chinese)
  """
  name = models.CharField(unique=True, max_length=45)

  def __unicode__(self):
    return self.name


class Location(models.Model):
  """Class representing a location used by the application.

  These locations are derived from either:
  1. Open Street Map Nominatim API (
     http://wiki.openstreetmap.org/wiki/Nominatim)
  2. Google Maps Geocoding API (
     http://code.google.com/apis/maps/documentation/geocoding/#JSON)

  That decision is still TBD, so for now this class is a stub.
  """
  name = models.CharField(unique=True, max_length=45)

  def __unicode__(self):
    return self.name


class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)

  """Class representing a hunchworks user."""
  title = models.IntegerField(
    choices=hunchworks_enums.UserTitle.GetChoices(), default=0)
  show_profile_reminder = models.IntegerField(default=0)
  privacy = models.IntegerField(
    choices=hunchworks_enums.PrivacyLevel.GetChoices(), default=0)
  bio_text = models.TextField(blank=True)
  phone = models.CharField(max_length=20, blank=True)
  skype_name = models.CharField(max_length=30, blank=True)
  website = models.CharField(max_length=100, blank=True)
  profile_picture = models.CharField(max_length=100, blank=True)
  screen_name = models.CharField(max_length=45, blank=True)
  messenger_service = models.IntegerField(null=True, blank=True,
    choices=hunchworks_enums.MessangerServices.GetChoices(), default=0)
  default_language = models.ForeignKey(Language, default=0)
  
  # Removed for now, since these should be:
  #  (a) linekd to the django auth user
  #  (b) implicit via symmetry
  #
  #skills = models.ManyToManyField('Skill', through='SkillConnections', blank=True)
  #education = models.ManyToManyField(
  #  'Education', through='EducationConnections')
  #classes = models.ManyToManyField('Class', through='EducationConnections')
  #location_interests = models.ManyToManyField(
  #  'Location', through='LocationInterests')
  #roles = models.ManyToManyField('Role', through='UserRoles')
  #hunches = models.ManyToManyField('Hunch', through='HunchConnections')
  #groups = models.ManyToManyField('Group', through='GroupConnections', blank=True)
  #collaborators = models.ManyToManyField('self', through='UserConnections', blank=True, symmetrical=False)


class EducationConnections(models.Model):
  """Many to Many model representing a user's education and/or classes"""
  user = models.ForeignKey(User)
  education = models.ForeignKey(Education, null=True, blank=True)
  class_field = models.ForeignKey(Class, null=True, blank=True)


class Hunch(models.Model):
  """Class representing a Hunch."""
  creator = models.ForeignKey(User, related_name='%(class)s_creator_id' )
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  status = models.IntegerField(choices=hunchworks_enums.HunchStatus.GetChoices(), default=2)
  title = models.CharField(max_length=100)
  privacy = models.IntegerField(choices=hunchworks_enums.PrivacyLevel.GetChoices(), default=0)
  hunch_strength = models.IntegerField(default=0)
  language = models.ForeignKey(Language)
  location = models.ForeignKey(Location, null=True, blank=True)
  description = models.TextField()
  skills = models.ManyToManyField('Skill', through='SkillConnections')
  hunch_tags = models.ManyToManyField('Tag', through='TagConnections', blank=True)
  invited_users = models.ManyToManyField(
    'InvitedUser', through='HunchConnections')

  def save(self, *args, **kwargs):
    now = datetime.datetime.today()

    # for new records.
    if not self.hunch_id:
      self.time_created = now

    self.time_modified = now
    super(Hunch, self).save(*args, **kwargs)

  def is_editable_by(self, user):
    """Return True if this Hunch is editable by `user` (a Django auth user)."""
    return (self.creator.user == user)

  def is_viewable_by(self, user):
    """Return True if this Hunch is viewable by `user` (a Django auth user)."""

    if self._is_hidden():
      return (self.creator.user == user)

    # Otherwise, if the hunch is OPEN or CLOSED, anyone (even anonymous) can
    # view it. The only distinction between the levels is in the editing.
    return True

  def _is_hidden(self):
    """Return True if this Hunch is hidden."""
    return (self.privacy == hunchworks_enums.PrivacyLevel.HIDDEN)


class Evidence(models.Model):
  """Class representing a response to the hunch"""
  evidence_strength = models.IntegerField(default=0)
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  evidence_description = models.TextField(blank=True)
  hunch = models.ForeignKey(Hunch)
  creator = models.ForeignKey(User)
  albums = models.ManyToManyField('Album', through='EvidenceAlbums')
  attachments = models.ManyToManyField(
    'Attachment', through='EvidenceAttachments')
  evidence_tags = models.ManyToManyField('Tag', through='TagConnections')

  def save(self, *args, **kwargs):
    now = datetime.datetime.today()

    # for new records.
    if not self.evidence_id:
      self.time_created = now

    self.time_modified = now
    super(Evidence, self).save(*args, **kwargs)


class EvidenceAlbums(models.Model):
  """Many to Many model joining Evidence and Album together"""
  album = models.ForeignKey(Album)
  evidence = models.ForeignKey(Evidence)


class EvidenceAttachments(models.Model):
  """Many to Many model joining evidence and attachments."""
  attachment = models.ForeignKey(Attachment)
  evidence = models.ForeignKey(Evidence)


class Group(models.Model):
  """Class representing a logical grouping of hunchworks users."""
  name = models.CharField(unique=True, max_length=100)
  group_type = models.IntegerField(choices=hunchworks_enums.GroupType.GetChoices(), default=0)
  privacy = models.IntegerField(choices=hunchworks_enums.PrivacyLevel.GetChoices(), default=0)
  logo = models.CharField(max_length=100, blank=True)
  location = models.ForeignKey(Location, null=True, blank=True)

  def __unicode__(self):
    return self.name

  @models.permalink
  def get_absolute_url(self):
    return ("group", [self.pk])


class GroupConnections(models.Model):
  """Many to Many model joining groups and users with users."""
  access_level = models.IntegerField()
  status = models.IntegerField()
  user = models.ForeignKey(User, related_name='%(class)s_user_id')
  group = models.ForeignKey(Group)


class InvitedUser(models.Model):
  """Class representing a master list of all users ever invited to the system
  and their respective user id's if they created an account."""
  email = models.CharField(max_length=45)
  status = models.IntegerField()
  created_user = models.ForeignKey(User, related_name='created_user_id',
    blank=True)
  invited_by = models.ForeignKey(User, related_name='invited_by_id')


class HunchConnections(models.Model):
  """Many to Many model joining Hunch and User,Group,InvitedUser together"""
  status = models.IntegerField()
  hunch = models.ForeignKey(Hunch)
  user = models.ForeignKey(User, null=True, blank=True)
  invited_email = models.ForeignKey(InvitedUser, null=True, blank=True)


class LocationInterests(models.Model):
  """Many to Many model joining User and Location together for their list
  of locations they are interested in"""
  user = models.ForeignKey(User)
  location = models.ForeignKey(Location)


class Organization(models.Model):
  """Class representing an external organization (UNDP etc.)."""
  name = models.CharField(max_length=125)
  abbreviation = models.CharField(max_length=7)
  group = models.ForeignKey(Group)
  location = models.ForeignKey(Location, null=True, blank=True)


class Role(models.Model):
  """Class representing a role held by a given user."""
  organization = models.ForeignKey(Organization)
  title = models.CharField(max_length=40)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  description = models.TextField(blank=True)


class Skill(models.Model):
  """Class representing a skill possessed by a user, e.g. HTML."""
  name = models.CharField(unique=True, max_length=100)
  is_language = models.IntegerField()
  is_technical = models.IntegerField()

  def __unicode__(self):
    return self.name


class SkillConnections(models.Model):
  """Many to Many model joining hunches, user and skills.

  This model represents the skill-set required to progress a hunch and the
  skill level needed for each skill. It also has the skillset of a user, and
  the level for each skill.
  """
  skill = models.ForeignKey(Skill)
  level = models.IntegerField()
  hunch = models.ForeignKey(Hunch, null=True, blank=True)
  user = models.ForeignKey(User, null=True, blank=True)


class UserRoles(models.Model):
  """Many To many model representing a user's roles or positions."""
  user = models.ForeignKey(User)
  role = models.ForeignKey(Role)


class Tag(models.Model):
  """Class representing tags you can add to Evidence and Hunches for searching
  easability"""
  name = models.CharField(max_length=40)


class TagConnections(models.Model):
  """Many to Many connector for Hunch, Evidence, and Tag classes"""
  tag = models.ForeignKey(Tag)
  hunch = models.ForeignKey(Hunch, blank=True, null=True)
  evidence = models.ForeignKey(Evidence, blank=True, null=True)


class UserConnections(models.Model):
  """Class representing a many to many relationship between users"""
  status = models.IntegerField()
  user = models.ForeignKey(User, related_name='conn_user_id')
  other_user = models.ForeignKey(User, related_name='other_user_id')


def create_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user, sender=User)