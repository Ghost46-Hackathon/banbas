from typing import Optional

ROLE_EXPIRY_SECONDS = {
    'admin': 15 * 60,   # 15 minutes
    'agent': 60 * 60,   # 1 hour
    'viewer': 4 * 60 * 60,  # 4 hours
}


class RoleBasedSessionExpiryMiddleware:
    """
    Middleware to set per-role session expiry. Applies a sliding expiration
    based on the authenticated user's role.

    - Admin: 15 minutes
    - Agent: 1 hour
    - Viewer: 4 hours
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._apply_role_based_expiry(request)
        response = self.get_response(request)
        return response

    def _apply_role_based_expiry(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return

        # Determine role safely
        role: Optional[str] = None
        try:
            role = user.userprofile.role
        except Exception:
            role = None

        if not role:
            return

        current_role_marker = request.session.get('rbse_role')
        already_applied = request.session.get('rbse_applied')

        # Only (re)apply if never applied or role changed
        if not already_applied or current_role_marker != role:
            expiry_seconds = ROLE_EXPIRY_SECONDS.get(role)
            if expiry_seconds:
                request.session.set_expiry(expiry_seconds)
                request.session['rbse_applied'] = True
                request.session['rbse_role'] = role
