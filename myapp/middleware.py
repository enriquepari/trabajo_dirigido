from django.shortcuts import reverse
from django.http import HttpResponseRedirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated and not request.path.startswith(reverse('login_view')):
            return HttpResponseRedirect(reverse('login_view'))
        return response
