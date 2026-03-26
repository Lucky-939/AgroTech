"""
<<<<<<< HEAD
WSGI config for config_temp project.
=======
WSGI config for agrotech project.
>>>>>>> 05f56bc7 (Initial commit for AgroTech)

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
=======
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
>>>>>>> 05f56bc7 (Initial commit for AgroTech)
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrotech.settings')

application = get_wsgi_application()
