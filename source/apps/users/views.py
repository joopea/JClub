from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, View
from formtools.wizard.views import SessionWizardView

from apps.core.views import AjaxFormResponseMixin
from apps.users.queries import UserDataView, UsernameVariationDataView, UserDataView
from apps.users.forms import LoginForm, UserRegistrationForm, UserChangeForm, PWResetFormQuestion, PWResetUsernameForm, \
    SetPasswordForm, PasswordConfirmationForm
from lib.users.mixins import LanguageRedirectMixin
from lib.users.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from apps.block.views import BlockedUsers
from apps.follow.views import FollowingUserUsers, FollowedUserUsers
from apps.menu.views import WithUserMenu


class LoginView(LanguageRedirectMixin, BaseLoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    form_action = reverse_lazy("users:login")
    prefix = 'user'

    def form_valid(self, form):
        self.language = form.get_user().language

        result = super(LoginView, self).form_valid(form)
        return result

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update(
            {
                'form_action': str(self.form_action),
                'login_form': context.pop('form', None)
            }
        )
        return context


class LogoutView(BaseLogoutView):
    pass


class RegisterView(AjaxFormResponseMixin, FormView):
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    form_css_class = 'register-form'
    submit_name = 'Register'
    form_action = reverse_lazy("users:register_ajax")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_next_url())
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(RegisterView, self).get_initial()
        # initial['username'] = self.request.GET.get('username', '')
        return initial

    def form_valid(self, form):

        form.save()
        form.authenticate_and_login(self.request)
        # messages.success(self.request, _('Thank you! Your registration was successfull. You are now logged in.'))

        context = {}
        return JsonResponse(
            {
                'success': True,
                'data': self.get_context_data(**context)
            }
        )

    def get_success_url(self):
        return self.get_next_url()

    def get_next_url(self):
        return self.request.GET.get('next', '/')

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)

        context.update({
            "form_css_class": self.form_css_class,
            "submit_name": self.submit_name,
            "form_action": str(self.form_action)
        })

        return context


class UserDetailsView(WithUserMenu, FollowedUserUsers, FollowingUserUsers, BlockedUsers, LanguageRedirectMixin, FormView):
    template_name = 'users/user_details.html'
    form_css_class = 'user-detail-form'
    form_class = UserChangeForm
    submit_name = _('Save')
    object = None
    default_redirect_param = reverse_lazy("users:user-details")
    allow_logged_in = True

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(UserDetailsView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        self.object = self.get_object()

        return super(UserDetailsView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        self.object = UserDataView.by_id(self.request.user.id)
        return self.object

    def form_valid(self, form):

        form.save()
        self.language = form.get_language()
        messages.success(self.request, _('Your profile is updated.'))

        return super(UserDetailsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserDetailsView, self).get_context_data(**kwargs)

        context.update({
            "form_css_class": self.form_css_class,
            "submit_name": self.submit_name,
        })

        return context


class UsernameVariationView(View):

    def get(self, request, *args, **kwargs):
        variations = UsernameVariationDataView.by_username(request.GET.get('username_id'))
        data = serializers.serialize('json', variations, fields=('id', 'username_variation_no'))
        return HttpResponse(data, content_type='application/json')


PW_FORMS = [("username", PWResetUsernameForm),
         ("sec-question1", PWResetFormQuestion),
         ("sec-question2", PWResetFormQuestion),
         ("confirmation", SetPasswordForm)]


class PasswordResetView(SessionWizardView):
    template_name = 'users/pw_reset.html'
    form_list = PW_FORMS
    user = None

    def done(self, form_list, **kwargs):
        for form in form_list:
            if hasattr(form, 'save'):
                form.save()

        return HttpResponseRedirect('/')

    def get_form(self, step=None, data=None, files=None):
        form = super(PasswordResetView, self).get_form(step, data, files)

        if not step:
            step = self.steps.current

        if step == 'sec-question1':
            form.user = self.get_user()
            form.answer = form.user.security_answer_1
            form.question = form.user.security_question_1

        if step == 'sec-question2':
            form.user = self.get_user()
            form.answer = form.user.security_answer_1
            form.question = form.user.security_question_2

        if step == 'confirmation':
            form.user = self.get_user()
            form.question = _("Please specify your new password. You will be directed to the homepage after successfully setting the new password.")

        return form

    def get_user(self):
        username = self.get_cleaned_data_for_step('username').get('username')
        return UserDataView.by_username(username)


class ProfileDeleteView(WithUserMenu, FormView):
    template_name = 'users/delete.html'
    form_class = PasswordConfirmationForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileDeleteView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'user': self.request.user
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        form.save(self.request)
        return HttpResponseRedirect('/')
