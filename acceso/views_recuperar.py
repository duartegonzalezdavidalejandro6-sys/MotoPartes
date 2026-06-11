# acceso/views_recuperar.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password

from .models import PasswordResetToken as RecuperacionPassword, Usuarios


def recuperar_solicitud(request):
    if request.method == "POST":
        correo = request.POST.get("correo", "").strip()

        if not correo:
            messages.error(request, "Ingresa un correo válido.")
            return render(request, "acceso/registro/recuperar/recuperar_solicitud.html")

        try:
            user = Usuarios.objects.get(correoUsuario=correo)
        except Usuarios.DoesNotExist:
            messages.success(
                request,
                "✅ Si el correo existe en nuestro sistema, recibirás un enlace de recuperación."
            )
            return redirect("recuperar_solicitud")

        RecuperacionPassword.objects.filter(usuario=user, usado=False).delete()
        recuperacion = RecuperacionPassword.objects.create(usuario=user)
        reset_link = request.build_absolute_uri(f"/recuperar/nueva-clave/{recuperacion.token}/")
        nombre = user.nombreUsuario

        try:
            html_email = render_to_string(
                "acceso/emails/recuperar_password.html",
                {
                    "nombre": nombre,
                    "link": reset_link,
                }
            )

            import requests as http_requests
            from django.conf import settings

            response = http_requests.post(
                "https://api.mailersend.com/v1/email",
                headers={
                    "Authorization": f"Bearer {settings.MAILERSEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": {
                        "email": settings.MAILERSEND_FROM_EMAIL,
                        "name": settings.MAILERSEND_FROM_NAME,
                    },
                    "to": [{"email": correo, "name": nombre}],
                    "subject": "🔒 Recupera tu contraseña — MotoPartes",
                    "text": f"Hola {nombre}, ingresa a este enlace para recuperar tu contraseña: {reset_link}",
                    "html": html_email,
                },
                timeout=10,
            )

            if response.status_code not in (200, 202):
                raise Exception(f"MailerSend error: {response.text}")

            messages.success(request, "✅ Hemos enviado un enlace de recuperación a tu correo. Expira en 1 hora.")
            return redirect("login")

        except Exception as e:
            print(f"❌ Error enviando email: {type(e).__name__}: {str(e)}")
            recuperacion.delete()
            messages.error(request, "Error al enviar el correo. Intenta más tarde.")
            return render(request, "acceso/registro/recuperar/recuperar_solicitud.html")

    # GET — mostrar el formulario
    return render(request, "acceso/registro/recuperar/recuperar_solicitud.html")


def recuperar_nueva_clave(request, token):
    try:
        recuperacion = RecuperacionPassword.objects.get(token=token)
    except RecuperacionPassword.DoesNotExist:
        messages.error(request, "❌ El enlace no es válido o ha expirado.")
        return redirect("recuperar_solicitud")

    if not recuperacion.es_valido():
        messages.error(request, "❌ El enlace ha expirado. Solicita uno nuevo.")
        return redirect("recuperar_solicitud")

    if request.method == "POST":
        clave1 = request.POST.get("clave1", "").strip()
        clave2 = request.POST.get("clave2", "").strip()

        if not clave1 or not clave2:
            messages.error(request, "Las contraseñas no pueden estar vacías.")
            return render(request, "acceso/registro/recuperar/recuperar_nueva_clave.html", {"token": token})

        if clave1 != clave2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "acceso/registro/recuperar/recuperar_nueva_clave.html", {"token": token})

        if len(clave1) < 6:
            messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
            return render(request, "acceso/registro/recuperar/recuperar_nueva_clave.html", {"token": token})

        try:
            user = recuperacion.usuario
            user.claveUsuario = make_password(clave1)
            user.save()

            from django.contrib.auth.models import User as DjangoUser

            django_user = None
            try:
                django_user = DjangoUser.objects.get(email=user.correoUsuario)
            except DjangoUser.DoesNotExist:
                try:
                    django_user = DjangoUser.objects.get(username=user.correoUsuario)
                except DjangoUser.DoesNotExist:
                    print(f"❌ No se encontró User de Django para: {user.correoUsuario}")

            if django_user:
                django_user.set_password(clave1)
                django_user.save()

            recuperacion.usado = True
            recuperacion.save()

            messages.success(request, "✅ Contraseña cambiada correctamente. Ya puedes iniciar sesión.")
            return redirect("login")

        except Exception as e:
            print(f"❌ Error cambiando contraseña: {str(e)}")
            messages.error(request, "Error al cambiar la contraseña. Intenta de nuevo.")
            return render(request, "acceso/registro/recuperar/recuperar_nueva_clave.html", {"token": token})

    return render(request, "acceso/registro/recuperar/recuperar_nueva_clave.html", {"token": token})
