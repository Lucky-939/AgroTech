"""
<<<<<<< HEAD
ASGI config for config_temp project.
=======
ASGI config for agrotech project.
>>>>>>> 05f56bc7 (Initial commit for AgroTech)

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
=======
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
>>>>>>> 05f56bc7 (Initial commit for AgroTech)
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config_temp.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrotech.settings')
>>>>>>> 05f56bc7 (Initial commit for AgroTech)

application = get_asgi_application()
