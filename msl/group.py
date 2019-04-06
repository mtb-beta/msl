import uuid
import json
import logging
from datetime import datetime

from colorama import Fore, Style

from msl import settings
from msl.note import note_manager


class Group:
    def __init__(self, group_name):
        self.group_id = str(uuid.uuid4())
        self.data = {}
        self.data['created_at'] = datetime.now().isoformat(timespec='seconds')
        self.data['title'] = group_name
        self.data['notes'] = []

    def save(self):
        group_path = settings.GROUP_DIR / self.group_id
        with group_path.open(mode='w') as json_file:
            json.dump(self.data, json_file)

    @classmethod
    def load(clz, group_path):
        group = Group("")
        group.group_id = group_path.name
        with group_path.open() as f:
            group.data = json.load(f)
        return group

    def add(self, note_id):
        note = note_manager.get(note_id)
        if note:
            self.data['notes'].append(note.note_id)

    @property
    def notes(self):
        return self.data['notes']


class GroupManager:
    def create(self, group_name):
        group = Group(group_name)
        group.save()

    def list(self):
        groups = list(settings.GROUP_DIR.glob('*'))
        for group in groups:
            with group.open() as f:
                group_data = json.load(f)
            title = group_data['title']
            yield group.name, title

    def get(self, group_name):
        if len(group_name) == 36:
            groups = list(settings.GROUP_DIR.glob(group_name))
        else:
            groups = list(settings.GROUP_DIR.glob(group_name+"*"))

        logging.debug(f'groups:{groups}')
        if not groups:
            print(f'{Fore.RED}{group_name} is not found.{Style.RESET_ALL}')
            return

        if len(groups) != 1:
            print(f'{Fore.RED}There are many [{group_name}] group.{Style.RESET_ALL}')
            for group in groups:
                print(f'  - {group.name}')
            return

        logging.debug(f'group_name:{group_name}')

        return Group.load(groups[0])

    def add(self, group, note):
        group = self.get(group)
        group.add(note)
        group.save()

group_manager = GroupManager()


def create_command(group_name):
    """
    This command craete group.
    """
    group_manager.create(group_name)


def list_command():
    """
    This command list group.
    """
    for group_name, title in group_manager.list():
        print(f'{group_name[:8]}{Fore.GREEN}:{Style.RESET_ALL}{title}')


def member_command(group_id):
    """
    This command list group member note.
    """
    group = group_manager.get(group_id)
    for note_id in group.notes:
        note = note_manager.get(note_id)
        if note:
            print(f'{note.note_id[:8]}{Fore.GREEN}:{Style.RESET_ALL}{note.title}')


def add_command(group_id, note_id):
    """
    This command add the note at the group.
    """
    group_manager.add(group_id, note_id)


def group_console(args):
    if len(args) > 2 and (args[1] == "create" or args[1] == 'c'):
        create_command(args[2])
    elif len(args) > 1 and (args[1] == "list" or args[1] == 'l'):
        list_command()
    elif len(args) > 2 and (args[1] == "member" or args[1] == 'l'):
        member_command(group_id=args[2])
    elif len(args) > 2:
        add_command(group_id=args[1], note_id=args[2])
    else:
        print('command not found')

