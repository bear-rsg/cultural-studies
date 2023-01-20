"""
Settings that are specific to this particular instance of the project.
This can contain sensitive information (such as keys) and should not be shared with others.

REMEMBER: If modfiying the content of this file, reflect the changes in local_settings.example.py
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create a SECRET_KEY.
# Online tools can help generate this for you, e.g. https://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''

# Set to True if in development, or False is in production
DEBUG = True/False

# Set static file storage.
# In live, use ManifestStaticFilesStorage with DEBUG set to False
# In other environments, use StaticFilesStorage with DEBUG set to True
if DEBUG is True:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Set to ['*'] if in development, or specific IP addresses and domains if in production
ALLOWED_HOSTS = ['*']/['culturalstudies.bham.ac.uk']

# Use for Django Debug Toolbar. To hide DDT, simply comment this out.
# DDT breaks accessibility CI, so don't include in local_settings.test.py
INTERNAL_IPS = [
    "127.0.0.1"
]

# Provide the email address for the site admin (e.g. the researcher/research team)
ADMIN_EMAIL = '...@bham.ac.uk'

# Set the database name below
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'cultural-studies.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'cultural-studies_TEST.sqlite3'),
        },
    }
}
