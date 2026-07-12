from functools import wraps
import os


def obtener_usuarios_autorizados():

    return {
        int(x.strip())
        for x in os.getenv("AUTHORIZED_USERS", "").split(",")
        if x.strip()
    }


def requiere_autorizacion(func):

    @wraps(func)
    async def wrapper(update, context):

        user = update.effective_user

        if user is None:
            return

        autorizados = obtener_usuarios_autorizados()

        if user.id not in autorizados:
            return

        return await func(update, context)

    return wrapper