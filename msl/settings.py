from pathlib import Path
import configparser


config = configparser.ConfigParser()

config_path = Path.home()/'.mslconfig'


if config_path.exists():
    config.read(Path.home()/'.mslconfig')

if 'data' in config and 'path' in config['data']:
    BASE_DIR = Path(config['data']['path']) / '.msl'
else:
    BASE_DIR = Path.home() / '.msl'

if 'data' in config and 'hostname' in config['data']:
    HOSTNAME = config['data']['hostname']
else:
    HOSTNAME = 'default'


BASE_DIR.mkdir(exist_ok=True)

META_DIR = BASE_DIR / 'meta'
NOTE_DIR = BASE_DIR / 'notes'
GROUP_DIR = BASE_DIR / 'groups'
BUILD_DIR = BASE_DIR / 'build'
ARCHIVE_DIR = BASE_DIR / 'archive'


META_DIR.mkdir(exist_ok=True)
NOTE_DIR.mkdir(exist_ok=True)
GROUP_DIR.mkdir(exist_ok=True)
BUILD_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)

BUILD_TEMPLATE_PATH = Path('./msl/') / 'build_template.html'
if BUILD_TEMPLATE_PATH.exists():
    BUILD_TEMPLATE = BUILD_TEMPLATE_PATH.read_text()

