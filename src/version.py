from os import environ

from .utils import formatted_current_time


VERSION =  f"{environ.get('VERSION', 'dev')}-{formatted_current_time('%Y.%m.%d')}"
