from appmedica.api.mail import mail_router
from appmedica.api.health import health_router

routers = [mail_router, health_router]

__all__ = ["routers"]
