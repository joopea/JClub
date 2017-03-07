from django import forms

from apps.post.queries import PostDataView, PostShareCount
from apps.wall.forms import WallForm
from apps.notifications.models import Notification
from apps.follow.queries import FollowUserDataView


class ShareForm(forms.Form):
    post = forms.IntegerField()
    author = forms.CharField()

    def save(self, *args, **kwargs):
        post = PostDataView.by_id(self.cleaned_data.get('post', 0))
        creator_id = self.cleaned_data.get('author', 0)

        # store the post on all walls of all ppl that are following this user
        # followers_walls = FollowersWallDataView.list(user_id=creator_id)
        followers = FollowUserDataView.followers(creator_id)
        notifications = []
        for follower in followers:
            wall_form = WallForm(data={'post': post.id, 'author': follower.author_id})
            if wall_form.is_valid():  # If not, this means the post is already present on the wall
                wall_form.save()  # Put the post on the wall

                notifications.append(Notification(
                    subject=Notification.SHARE_POST,
                    owner_id=follower.author_id,
                    author_id=creator_id,
                    relation_1=post.pk
                ))

        # add to own wall
        wall_form = WallForm(data={'post': post.id, 'author': creator_id})
        if wall_form.is_valid():
            wall_form.save()

            notifications.append(Notification(
                subject=Notification.FOLLOWEE_SHARE_POST,
                owner=post.author,
                author_id=creator_id,
                relation_1=post.pk
            ))

        Notification.objects.bulk_create(notifications)

        PostShareCount.update(post)
