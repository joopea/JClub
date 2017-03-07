from django.utils.translation import ugettext as _
from apps.block.models import BlockByUser, BlockByCommunity


class WithAuthor(object):
    def get_author(self, instance):
        if not getattr(self, '_author', None):
            self._author = {'id': None}
            if self.cleaned_data and self.cleaned_data['author']:
                self._author['id'] = self.cleaned_data['author'].id
            else:
                self._author['id'] = instance.author_id
        return self._author


class WithTarget(object):
    def get_target(self, instance):
        if not getattr(self, '_target', None):
            self._target = {'id': None}
            if self.cleaned_data and self.cleaned_data['target']:
                self._target['id'] = self.cleaned_data['target'].id
            else:
                self._target['id'] = instance.target_id
        return self._target


class WithGenericForeignObjectAuthor(object):
    def get_owner(self, instance):
        if not getattr(self, '_owner', None):
            self._owner = {
                'id': instance.content_object.author_id
            }
        return self._owner


class WithOwnerIsNotSelfConstraint(WithAuthor, WithGenericForeignObjectAuthor):
    def clean(self, *args, **kwargs):
        cleaned_data = super(WithOwnerIsNotSelfConstraint, self).clean(*args, **kwargs)
        author = self.get_author(self.instance)
        owner = self.get_owner(self.instance)
        if author['id'] == owner['id']:
            self.add_error('__all__', 'You are not allowed to take this action on a resource created by yourself.')
        return cleaned_data


class WithAuthorNotBlockedByTarget(WithAuthor, WithTarget):
    def clean(self, *args, **kwargs):
        cleaned_data = super(WithAuthorNotBlockedByTarget, self).clean(*args, **kwargs)
        author = self.get_author(self.instance)
        target = self.get_target(self.instance)
        if BlockByUser.objects.filter(target=author['id'], author=target['id']).exists():
            self.add_error('__all__', 'You are blocked by this user.')
        return cleaned_data


class WithAuthorCanPostToWall(WithAuthor):
    def clean(self, *args, **kwargs):
        cleaned_data = super(WithAuthorCanPostToWall, self).clean(*args, **kwargs)
        author = self.get_author(self.instance)
        wall = self.data['object_id']
        if BlockByCommunity.objects.filter(target=author['id'], wall=wall).exists():
            self.add_error('__all__', 'You are blocked form this wall.')
        return cleaned_data
