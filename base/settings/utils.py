import os
import setuptools

"""
from base_apps.settings import get_context_processors, get_installed_apps, get_middleware
"""

APPS_FILES = [
    'admin.py',
    'apps.py',
    'models.py',
]
APPS_DIRS = [
    'admin',
    'apps',
    'models',
    'templatetags'
]


def isapp(path):
    if os.path.exists(os.path.join(path, 'management', 'commands')):
        return os.path.join(path)
    if not os.path.exists(os.path.join(path, '__init__.py')):
        return False
    for app_file in APPS_FILES:
        fullpath = os.path.join(path, app_file)
        if os.path.exists(fullpath) and os.path.isfile(fullpath):
            return True
    for app_dir in APPS_DIRS:
        fullpath = os.path.join(path, app_dir, '__init__.py')
        if os.path.exists(fullpath) and os.path.isfile(fullpath):
            return True


def find_apps(path):
    """return a list of apps"""
    apps = []
    for package in setuptools.find_packages(os.path.abspath(path)):
        if 'views' not in package.split('.') and 'urls' not in package.split('.'):
            if isapp(os.path.join(path, package.replace('.', os.sep))):
                apps.append(package)
    return apps

def get_lines(path):
    return list(filter(
        lambda s:s and '#' not in s,
        open(path).read().splitlines()
    ))

def get_context_processors():
    path = os.path.join('settings','context_processors.txt')
    if os.path.exists(path):
        return get_lines(path)
    return []

def get_installed_apps():
    path = os.path.join('settings','apps.txt')
    return get_lines(path)+find_apps(os.getcwd())

def get_middleware():
    path = os.path.join('settings','middleware.txt')
    if os.path.exists(path):
        return get_lines(path)
    return []
