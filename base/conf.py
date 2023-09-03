import os

ROOT_DIRNAME = os.path.join('/Volumes/HDD','.gists42.com','files')
if os.path.exists('/.dockerenv'):
    ROOT_DIRNAME = os.path.join('/files') # use docker volumes
RESPONSE_DIRNAME = os.path.join(ROOT_DIRNAME,'response')
