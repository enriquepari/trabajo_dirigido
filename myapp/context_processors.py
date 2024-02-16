# En tu archivo context_processors.py

from django.contrib.auth.models import Group

def user_group(request):
    # Obtén el grupo del usuario si está autenticado
    user_group = None

    if request.user.is_authenticated:
        try:
            user_group = Group.objects.get(user=request.user).name
        except Group.DoesNotExist:
            # Manejar la excepción si el grupo no existe
            pass
        except Group.MultipleObjectsReturned:
            # Manejar la excepción si hay múltiples grupos asociados al usuario
            pass

    return {'user_group': user_group}
