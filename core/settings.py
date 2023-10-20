from .helpers import load_dotenv_file, Console
import os

ENV = os.environ.get('ENV', 'DEVELOPMENT').upper()

Console.log("=====> ENV : %s <=====" % ENV, Console.HEADER)

if ENV == "DEVELOPMENT":
    load_dotenv_file('.env.development')
    from core.conf.settings_dev import *

if ENV == "PRODUCTION":
    load_dotenv_file('.env.production')
    from core.conf.settings_prod import *
else:
    load_dotenv_file('.env.local')
    from core.conf.settings_local import *

Console.log("==========================================", Console.WARNING)
