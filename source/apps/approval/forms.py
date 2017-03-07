from django import forms
from .models import PostApproval, CommentApproval


class WithApprovalCheck(object):
    def __init__(self, *args, **kwargs):
        super(WithApprovalCheck, self).__init__(*args, **kwargs)
        self.dis_approval_reasons = []

    def add_disapproval_reason(self, reason):
        self.dis_approval_reasons.append(reason)

    @property
    def has_disapproval_reasons(self):
        return True if self.dis_approval_reasons else False

    def get_disapproval_reasons(self):
        return ', '.join(self.dis_approval_reasons)

    def get_reason(self):
        return "\n\n".join(self.dis_approval_reasons)

    def check_published(self):
        return False

    def save(self, *args, **kwargs):
        instance = super(WithApprovalCheck, self).save(commit=False)
        instance.published = True

        if len(self.dis_approval_reasons):
            instance.published = self.check_published()

        instance.save(*args, **kwargs)
            
        return instance

    def after_save(self, response):

        if len(self.dis_approval_reasons):

            if self.instance.__class__.__name__ == 'Post':
                PostApproval(post=self.instance, is_approved=False, reason=self.get_reason()).save()

            if self.instance.__class__.__name__ == 'Comment':
                CommentApproval(comment=self.instance, is_approved=False, reason=self.get_reason()).save()

        else:  # Stops further business logic.
            # Todo: Mentions depend on after save to. But when this is send for approval we do not want any
            # notifications. The problem is a notification wil not be send after approval. Maybe this logic needs
            # to be moved to the model.save()
            response = super(WithApprovalCheck, self).after_save(response)

        return response
