from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import defaults
from django.views.decorators.http import require_POST

from audit.models import AuditLog

from .forms import SignInForm
from .middleware import SESSION_KEY
from .models import User, UserRole
from .permissions import log_refusal


def permission_denied(request, exception=None):
    """Every refused page goes to the audit log (FR-02.3), not only refusals of the role check."""
    if exception is not None and not getattr(exception, "logged", False):
        log_refusal(request, "open record")
    return defaults.permission_denied(request, exception)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    form = SignInForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.filter(username__iexact=form.cleaned_data["username"]).first()
        if user is not None and user.is_locked():
            form.add_error(None, "This account is locked for 15 minutes after 5 failed sign-ins. Try again later.")
        elif user is not None and user.sign_in(form.cleaned_data["password"]):
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            AuditLog.record(user, "signed in", user)
            target = request.GET.get("next", "")
            if url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
                return redirect(target)
            return redirect("core:home")
        else:
            if user is not None:
                AuditLog.record(user, "failed sign-in", user)
            if user is not None and user.is_locked():
                form.add_error(None, "Too many failed sign-ins. This account is locked for 15 minutes.")
            else:
                form.add_error(None, "The username or password is not correct.")
    return render(request, "accounts/sign_in.html", {"form": form})


@require_POST
def sign_out(request):
    if request.user.is_authenticated:
        AuditLog.record(request.user, "signed out", request.user)
    logout(request)
    return redirect("accounts:login")


@login_required
@require_POST
def switch_role(request):
    user_role = UserRole.objects.filter(
        pk=request.POST.get("user_role"), user=request.user, status=UserRole.Status.ACTIVE
    ).select_related("role", "department").first()
    if user_role is None:
        messages.error(request, "You do not hold that role.")
    else:
        request.session[SESSION_KEY] = user_role.pk
        request.user.active_role = user_role
        AuditLog.record(request.user, "switched role", request.user, after=str(user_role))
        messages.success(request, f"You are now working as {user_role}.")
        # From the refused page, go back to the page the user was trying to open.
        target = request.POST.get("next", "")
        if url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            return redirect(target)
    return redirect("core:home")
