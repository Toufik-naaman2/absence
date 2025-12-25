from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Special decorators for each role
admin_required = role_required(['admin'])
teacher_required = role_required(['teacher'])
student_required = role_required(['student'])