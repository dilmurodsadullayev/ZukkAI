from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """
    Login qilmagan user saytga kira olmaydi.
    Faqat login, register, static, media va admin yo'llari ochiq qoladi.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        login_url = reverse("login")
        register_url = reverse("register")

        allowed_paths = [
            login_url,
            register_url,
            "/admin/",
            settings.STATIC_URL,
            settings.MEDIA_URL,
        ]

        is_allowed = any(path.startswith(allowed_path) for allowed_path in allowed_paths)

        if not request.user.is_authenticated and not is_allowed:
            query = urlencode({"next": path})
            return redirect(f"{login_url}?{query}")

        return self.get_response(request)