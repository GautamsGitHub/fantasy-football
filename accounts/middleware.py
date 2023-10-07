from django.shortcuts import redirect
from django.http import HttpRequest
from django.conf import settings
from . import views
from os import getenv

class MemberAuthMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.session.get("member_authorised", False):
            return self.get_response(request)
        elif request.path == "/accounts/member_auth":
            return views.memberPass(request)
        else:
            return redirect("Member Authentication")
        