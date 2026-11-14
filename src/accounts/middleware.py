from .models import UserRole

SESSION_KEY = "active_user_role_id"


class ActiveRoleMiddleware:
    """Puts the signed-in user's active role on the request and on the user (request.active_role)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.active_role = None
        if request.user.is_authenticated:
            roles = UserRole.objects.filter(user=request.user, status=UserRole.Status.ACTIVE).select_related(
                "role", "department"
            )
            chosen = roles.filter(pk=request.session.get(SESSION_KEY)).first() or roles.first()
            if chosen is not None:
                request.session[SESSION_KEY] = chosen.pk
            request.active_role = chosen
            request.user.active_role = chosen
        return self.get_response(request)
