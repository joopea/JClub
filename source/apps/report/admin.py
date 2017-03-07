from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from apps.custom_admin.admin import ButtonableAdmin, ImprovedRawIdFields
from apps.users.queries import UserDataView
from apps.notifications.queries import NotificationDataView
from apps.report.forms import AdminReportForm
from apps.share.queries import ShareDataView
from apps.community.queries import CommunityDataView
from apps.post.queries import PostDataView
from apps.comment.queries import CommentDataView
from apps.like.queries import LikePostDataView, LikeCommentDataView

from .models import Report


class ReportAdmin(ButtonableAdmin, ImprovedRawIdFields):
    return_url = reverse_lazy("admin:report_report_changelist")
    search_fields = ['message', 'author__username']
    list_display = ['message', 'get_reported_user', 'get_reported_object', 'approve_show', 'disapprove_show', 'author', 'created']
    readonly_fields = []
    raw_id_fields = ['comment', 'post']
    form = AdminReportForm

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
        return super(ReportAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_reported_user(self, obj):
        return obj.reported_user

    get_reported_user.short_description = _('Reported')

    def get_reported_object(self, obj):
        return obj.reported_object

    get_reported_object.short_description = _('Comment/ Post')

    @method_decorator(staff_member_required)
    def approve(self, request, obj):
        obj.approve()
        subject = NotificationDataView.get_approved_report_subject(obj)
        NotificationDataView.approval_notification(request.user, obj.reported_user, subject, message=obj.message, to_self=True)
        return redirect(self.return_url)

    approve.short_description = _('Approve this Report')

    @method_decorator(staff_member_required)
    def disapprove(self, request, obj):
        obj.disapprove()
        subject = NotificationDataView.get_disapproved_report_subject(obj)
        NotificationDataView.approval_notification(request.user, obj.author, subject, relation_id=obj.get_post_id(), to_self=True)
        return redirect(self.return_url)

    disapprove.short_description = _('Disapprove this Report')

    def approve_show(self, obj):
        return u'<a class="addlink" href="{0}/approve">Approve</a>'.format(obj.id)

    approve_show.allow_tags = True
    approve_show.short_description = _("Approve")

    def disapprove_show(self, obj):
        return u'<a class="deletelink" href="{0}/disapprove">Disapprove</a>'.format(obj.id)

    disapprove_show.allow_tags = True
    disapprove_show.short_description = _("Disapprove")

    """
    Declare your admin buttons here!
    """
    buttons = [(approve.func_name, approve.short_description), (disapprove.func_name, disapprove.short_description), ]


admin.site.register(Report, ReportAdmin)


class ReportView(TemplateView):
    template_name = None
    time_span = 30

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()
        context['subject'] = self.subject
        return context


class UserReportView(ReportView):
    template_name = "report/admin/report_view_user.html"
    subject = 'User'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()
        # A Manager can view Reports of number of Users
        context['count'] = UserDataView.get_active_user_count()
        # A Manager can view Reports of growth of number of Users
        context['growth_by_day'] = UserDataView.get_active_users_by_day(time_span=self.time_span)
        # A Manager can View a Report of the Rate of Growth of Users
        total = 0
        for item in context['growth_by_day']:
            total += item['created_count']
        context['growth_rate_per_day'] = round((1.0 * total) / self.time_span, 2)
        return context


class ShareReportView(ReportView):
    template_name = "report/admin/report_view_share.html"
    subject = 'Share'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()
        # A Manager can view Reports of number of Shares
        context['count'] = ShareDataView.get_count()
        # A Manager can view Reports of growth of number of Shares
        context['growth_by_day'] = ShareDataView.growth_by_day(time_span=self.time_span)
        # A Manager can View a Report of the Rate of Growth of Shares
        total = 0
        for item in context['growth_by_day']:
            total += item['created_count']
        context['growth_rate_per_day'] = round((1.0 * total) / self.time_span, 2)
        # A Manager can view a Report on number of Shares per Community
        context['count_by_community'] = ShareDataView.get_count_per_community()
        # A Manager can View a Report of the Rate of Growth of Shares per Community
        context['growth_by_day_by_community'] = ShareDataView.growth_by_day_per_community(
            context['count_by_community'],
            time_span=self.time_span)

        context['growth_rate_per_day_by_community'] = {}
        for community, days in context['growth_by_day_by_community'].iteritems():
            total = 0
            for day in days:
                total += day.get('count', 0)
            context['growth_rate_per_day_by_community'][community] = round((1.0 * total) / self.time_span, 2)

        return context


class FollowersReportView(ReportView):
    template_name = 'report/admin/report_view_followers.html'
    subject = 'Followers'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()
        # A Manager can View a Report of the Rate of Growth of Followers per Community
        context['growth_rate_by_community'] = CommunityDataView.growth_rate_followers(time_span=self.time_span)
        return context


class PostReportView(ReportView):
    template_name = 'report/admin/report_view_post.html'
    subject = 'Post'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()

        context['count'] = PostDataView.count()
        context['rate_of_growth'] = PostDataView.rate_of_growth(time_span=self.time_span)
        context['count_per_community'] = CommunityDataView.number_of_posts_per_community()
        context['rate_of_growth_per_community'] = CommunityDataView.\
            rate_of_growth_of_posts_per_community(time_span=self.time_span)

        return context


class CommentReportView(ReportView):
    template_name = 'report/admin/report_view_comment.html'
    subject = 'Comment'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()

        context['count'] = CommentDataView.count()
        context['count_per_community'] = CommunityDataView.number_of_comments_per_community()
        context['rate_of_growth_per_community'] = CommunityDataView.\
            rate_of_growth_of_comments_per_community(time_span=self.time_span)
        context['rate_of_growth'] = CommentDataView.rate_of_growth(time_span=self.time_span)

        return context


class LikeReportView(ReportView):
    template_name = 'report/admin/report_view_like.html'
    subject = 'Like'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()

        context['post_count'] = LikePostDataView.count()
        context['comment_count'] = LikeCommentDataView.count()

        context['post_growth_rate_per_day'] = LikePostDataView.rate_of_growth(time_span=self.time_span)
        context['comment_growth_rate_per_day'] = LikeCommentDataView.rate_of_growth(time_span=self.time_span)

        context['post_count_per_community'] = LikePostDataView.count_per_community()
        context['comment_count_per_community'] = LikeCommentDataView.count_per_community()

        context['post_growth_by_day'] = LikePostDataView.growth_by_day(time_span=self.time_span)
        context['comment_growth_by_day'] = LikeCommentDataView.growth_by_day(time_span=self.time_span)

        context['post_growth_rate_per_day_per_community'] = LikePostDataView.\
            rate_of_growth_per_community(time_span=self.time_span)
        context['comment_growth_rate_per_day_per_community'] = LikeCommentDataView.\
            rate_of_growth_per_community(time_span=self.time_span)

        return context


class AlertsReportView(ReportView):
    template_name = 'report/admin/report_view_alert.html'
    subject = 'Alert'
    alert_count = 15

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data()

        context['users'] = UserDataView.alert_count(alert_count=self.alert_count)
        context['n'] = self.alert_count

        return context
