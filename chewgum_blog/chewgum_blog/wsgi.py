"""
WSGI config for chewgum_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chewgum_blog.settings')
#
# application = get_wsgi_application()

import os

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chewgum_blog.settings')
profile = os.environ.get('PROJECT_PROFILE','develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chewgum_blog.settings.%s' % profile)
application = get_wsgi_application()