from .models import Notification


class WithMentionNotification(object):
    notification_type = 'MENTION'

    def get_notification_type(self):
        choice = self.notification_type
        try:
            if self.comment:
                return getattr(Notification, str(choice) + '_COMMENT')
        except AttributeError:
            if self.post:
                return getattr(Notification, str(choice) + '_POST')

    def get_notification_data(self, instance):
        data = dict()
        data['author'] = self.cleaned_data['author']
        data['owner'] = instance.target
        data['subject'] = self.get_notification_type()
        data['relation_1'] = self.post
        return data

    def save(self, *args, **kwargs):
        instance = super(WithMentionNotification, self).save(*args, **kwargs)
        notification = Notification(**self.get_notification_data(instance))
        notification.save()
        return instance
