import json

from django.http import HttpResponse
from django.shortcuts import redirect


def json_response(something):
    return HttpResponse(json.dumps(something), content_type="application/javascript; charset=utf8")


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


def login_failureView(request):
    """View to handle login failure. It shows the user the reason why the login failed."""
    if "authentication_errors" in request.session:
        return json_response({"authenticated": request.session["authentication_errors"]})
    return json_response(
        {"authenticated": "Login failed due to unknown reasons. Please try again."}
    )
