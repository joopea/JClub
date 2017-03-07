# Create your views here.
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from apps.shorturl.models import ShortURL
from django.http.response import Http404


# Cache is handled by Varnish
def redir(request, shorturl=None):
    try:
        if request.method not in ('GET', 'HEAD'):
            return HttpResponseForbidden('Wrong method, only reads allowed')
        return redirect(get_object_or_404(ShortURL.objects.active(), short=shorturl).long)
    except ValueError:
        raise Http404()