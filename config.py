import os
from starlette.config import Config
#from starlette.datastructures import CommaSeparatedStrings, Secret


dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path
config = Config(f'{root_dir}\.env')

BOT_TOKEN = config('BOT_TOKEN', default=None)
