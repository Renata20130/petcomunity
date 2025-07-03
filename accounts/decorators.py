from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def tipo_requerido(tipo_usuario):
    def decorador(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if hasattr(request.user, 'profile') and request.user.profile.tipo == tipo_usuario:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorador
