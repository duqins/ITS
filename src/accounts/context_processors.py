def active_role(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {}
    return {
        "active_role": getattr(request, "active_role", None),
        "my_roles": list(user.active_user_roles()),
    }
