import os

ENVIRONMENT = os.environ.get('DJANGO_ENV', 'DEVELOPMENT')
if ENVIRONMENT == 'DEVELOPMENT':
  from environment.development import *
else:
  from environment.production import *
