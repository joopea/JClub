from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.users.base_models import AbstractBaseUser
from lib.utils.managers import ActiveManager

from apps.block.queries import BlockByCommunityDataView, BlockByUserDataView
from apps.save.queries import SavedByUserDataView
from apps.language.models import Language


class User(AbstractBaseUser):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    username = models.CharField(_('Username'), max_length=255, unique=True)
    profile_colour = models.CharField(_('Profile Color'), max_length=16)
    language = models.ForeignKey('language.Language', limit_choices_to={'status': 'act'}, to_field='name')

    security_question_1 = models.CharField(_('security question 1'), max_length=255, help_text=_("Recovering your password is only possible with a security question. Make sure to remember your answer."))
    security_question_2 = models.CharField(_('security question 2'), max_length=255)

    security_answer_1 = models.CharField(_('security answer 1'), max_length=255)
    security_answer_2 = models.CharField(_('security answer 2'), max_length=255)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._cache_authors = {}
        self._cache_communities = {}

    def get_absolute_url(self):
        return reverse("wall:detail", kwargs={"pk": self.pk})

    def is_blocked(self, user=None, author=None, community=None):
        if author is not None:
            return self.is_blocked_by_user(user=user, author=author)
        if community is not None:
            return self.is_blocked_by_community(user=user, community=community)

    def is_blocked_by_user(self, author):
        return BlockByUserDataView.is_blocked(user=self, author=author)

    def is_blocked_by_community(self, community):
        return BlockByCommunityDataView.is_blocked(user=self, community=community)

    def is_post_saved_by_user(self, post):
        return SavedByUserDataView.is_saved(user=user, post=post)

    def is_following(self, author):
        return BlockByCommunityDataView.is_blocked(user=self, community=community)

    def check_security_answer_1(self, answer):
        return self.check_security_answers(answer, self.security_answer_1)

    def check_security_answer_2(self, answer):
        return self.check_security_answers(answer, self.security_answer_2)

    @classmethod
    def check_security_answers(cls, raw_answer, encoded_answer):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        return check_password(raw_answer, encoded_answer)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Username(models.Model):
    username = models.CharField(_('username'), max_length=250, unique=True)
    active = models.BooleanField(_('active'), default=True, help_text=_('max of 100 active usernames allowed'))

    objects = ActiveManager()

    def __unicode__(self):
        return unicode(self.username)

    def delete(self, **kwargs):
        self.active = False
        self.save()

    class Meta:
        verbose_name = _('username')
        verbose_name_plural = _('usernames')
        ordering = ['username']


class UsernameVariation(models.Model):
    username = models.ForeignKey('users.Username')
    username_variation = models.CharField(_('Username variation'), max_length=255, unique=True)
    username_variation_no = models.IntegerField(_('Username variation number'))

    def __unicode__(self):
        return unicode(self.username_variation_no)  # Do not change, this will break select field display values #ugly

    class Meta:
        verbose_name = _('username variation')
        verbose_name_plural = _('username variations')
        ordering = ['username_variation']


class SecurityQuestion(models.Model):
    question = models.CharField(_('question'), max_length=255)

    def __unicode__(self):
        return unicode(self.question)
