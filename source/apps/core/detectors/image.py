from django.utils.translation import ugettext_lazy as _

class WithImageApprovalCheck(object):
    def save(self, *args, **kwargs):
        instance = super(WithImageApprovalCheck, self).save(*args, **kwargs)
        if hasattr(instance, 'image') and instance.image:
            instance.published = False
            self.add_disapproval_reason('Image attached') # Do not translate!
        return instance
