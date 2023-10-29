import os

HTTP_CLIENT_DIR = os.path.join("/Volumes/HDD", ".gists42.com", "http_response")
if os.path.exists("/.dockerenv"):
    HTTP_CLIENT_DIR = os.path.join("/http_response")  # use docker volumes
