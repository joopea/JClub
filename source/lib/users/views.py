from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, View
from .forms import BaseLoginForm, PasswordResetForm, SetPasswordForm
from lib.users.data_views import UserDataView


class LoginView(FormView):
    """
    Login method for the users
    """
    template_name = "users/login.html"
    form_class = BaseLoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        self.request.session.cycle_key()
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    """
    Uses POST method for security purposes
    """

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return self.logout(request)

    @classmethod
    def logout(cls, request):
        logout(request)
        logout_url = request.GET.get('next', '/')
        return HttpResponseRedirect(logout_url)


class PasswordResetView(FormView):
    """
    4 steps for password reset:
    - password_reset sends the mail
    - password_reset_done shows a success message for the above
    - password_reset_confirm checks the link the user clicked and
      prompts for a new password
    - password_reset_complete shows a success message for the above
    """
    template_name = 'users/password_reset.html'
    form_class = PasswordResetForm

    def form_valid(self, form):

        form.save(self.request)
        return super(PasswordResetView, self).form_valid(form)

    def get_success_url(self):
        return reverse("users:password-reset")


class PasswordResetConfirmView(FormView):
    """
    4 steps for password reset:
    - password_reset sends the mail
    - password_reset_done shows a success message for the above
    - password_reset_confirm checks the link the user clicked and
      prompts for a new password
    - password_reset_complete shows a success message for the above
    """
    template_name = 'users/password_reset_confirm.html'
    form_class = SetPasswordForm
    user = None

    def dispatch(self, request, *args, **kwargs):

        uid = kwargs.get('uidb64')
        token = kwargs.get('token')

        self.user = UserDataView.by_id(urlsafe_base64_decode(uid))
        if not default_token_generator.check_token(self.user, token):
            raise Http404("Invalid token")

        return super(PasswordResetConfirmView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(PasswordResetConfirmView, self).get_form_kwargs()
        kwargs.update({'user': self.user})
        return kwargs

    def form_valid(self, form):

        form.save()
        return super(PasswordResetConfirmView, self).form_valid(form)

    def get_success_url(self):
        return reverse("users:login")
