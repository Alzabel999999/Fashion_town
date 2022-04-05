from corsheaders.defaults import default_headers


CORS_ALLOW_HEADERS = list(default_headers) + ['currency', 'origin']

# ========
import os
if bool(os.getenv('DEBUG')):
    CORS_ALLOW_ALL_ORIGINS = True
# ========/
