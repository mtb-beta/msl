from pathlib import Path
import configparser

import git

config = configparser.ConfigParser()

config_path = Path.home()/'.mslconfig'


if config_path.exists():
    config.read(Path.home()/'.mslconfig')

if 'data' in config and 'path' in config['data']:
    BASE_DIR = Path(config['data']['path']) / '.msl'
else:
    BASE_DIR = Path.home() / '.msl'

BASE_DIR.mkdir(exist_ok=True)


repo = git.Repo.init(BASE_DIR)

META_DIR = BASE_DIR / 'meta'
NOTE_DIR = BASE_DIR / 'notes'
