"""
BACKUP_DIR/USER_ID/timestamp.tar.gz
RAW_DIR/USER_ID/GIST_ID/filename
TRASH_DIR/USER_ID/GIST_ID/filename
"""

import os

DEV_DIR = os.path.join("/Volumes/HDD", ".gists42.com")
BACKUP_DIR = os.path.join(DEV_DIR, "backup")
RAW_DIR = os.path.join(DEV_DIR, "raw")
TRASH_DIR = os.path.join(DEV_DIR, "trash")
HTTP_CLIENT_DIR = os.path.join(DEV_DIR, "http_response")
if os.path.exists("/.dockerenv"):
    BACKUP_DIR = "/backup"
    RAW_DIR = "/raw"
    TRASH_DIR = "/trash"
    HTTP_CLIENT_DIR = "/http_response"


