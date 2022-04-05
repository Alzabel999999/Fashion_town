import contextlib

with contextlib.suppress(ImportError):
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())  # load environment variables from .env when using pycharm

from .base import *
from .path import *
from .apps import *
from .database import *
from .languages import *
from .notify import *
from .celery import *
from .ckeditor import *
from .page import *
from .menu import *
from .migrations import *
from .menu import *
from .drf import *
from .youtube import *
from .content import *
from .event import *
from .social import *
from .shop import *
# from .raven import *
from .cors import *
