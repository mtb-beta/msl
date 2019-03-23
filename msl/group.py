import uuid
import json
from datetime import datetime

from colorama import Fore, Style

from msl import settings


class GroupManager:
    def __init__(self):
        self.dir = settings.GROUP_DIR

    def create(self, group_name):
        group_id = str(uuid.uuid4())
        data = {}
        data['created_at'] = datetime.now().isoformat(timespec='seconds')
        data['title'] = group_name
        data['note'] = {}

        group_path = self.dir / group_id
        with group_path.open(mode='w') as json_file:
            json.dump(data, json_file)

    def list(self):
        groups = list(self.dir.glob('*'))
        for group in groups:
            with group.open() as f:
                group_data = json.load(f)
            title = group_data['title']
            yield group.name, title


group_manager = GroupManager()



def create_command(group_name):
    """
    This command craete group.
    """
    group_manager.create(group_name)

def list_command():
    """
    This command list notes.
    """
    for note_name, title in group_manager.list():
        print(f'{note_name[:8]}{Fore.GREEN}:{Style.RESET_ALL}{title}')

def group_console(args):
    if len(args) > 2 and (args[1] == "create" or args[1] == 'c'):
        create_command(args[2])
    elif len(args) > 1 and (args[1] == "list" or args[1] == 'l'):
        list_command()
    else:
        print('command not found')

