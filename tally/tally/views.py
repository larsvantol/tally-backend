from django.http import HttpResponse
from django.shortcuts import redirect
import json


def json_response(something):
    return HttpResponse(
        json.dumps(something), content_type="application/javascript; charset=utf8"
    )


def is_authenticatedView(request):
    if request.user.is_authenticated:
        return json_response({"authenticated": True})
    else:
        return json_response({"authenticated": False})


def loginView(request):
    if not (request.user.is_authenticated):
        return redirect("oidc_authentication_init")
    else:
        return is_authenticatedView(request)


def logoutView(request):
    if request.user.is_authenticated:
        return redirect("oidc_logout")
    else:
        return is_authenticatedView(request)
