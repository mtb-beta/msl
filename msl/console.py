import argparse
import os
import sys
import uuid
import logging
import json
from pathlib import Path
from datetime import datetime

from colorama import Fore, Style

#logging.basicConfig(level=logging.DEBUG)

BASE_DIR = Path.home() / '.msl/'
META_DIR = BASE_DIR / 'meta'
NOTE_DIR = BASE_DIR / 'notes'

def open_note(note_name):
    """
    This will open editor by note_name.
    """
    NOTE_DIR.mkdir(exist_ok=True)
    note_path = NOTE_DIR / note_name
    os.system("vim {}".format(note_path))

def save_meta_data(note_name):
    """
    This will update meta data on note_name.
    """
    data = {}
    data['created_at'] = datetime.now().isoformat(timespec='seconds')
    note_path = NOTE_DIR / note_name

    if not note_path.exists():
        logging.warning('There is not note_path.')
        return

    with note_path.open() as f:
        data['title'] = f.readline().replace('\n', '')

    META_DIR.mkdir(exist_ok=True)
    json_note_path = META_DIR / str(note_name + '.json')
    with json_note_path.open(mode='w') as json_file:
        json.dump(data, json_file)


def create_command():
    """
    This command craete note.
    """
    temporary_note_name = str(uuid.uuid1())
    BASE_DIR.mkdir(exist_ok=True)
    # open note
    open_note(temporary_note_name)

    # save meta data
    save_meta_data(temporary_note_name)

def list_command():
    """
    This command list notes.
    """
    notes = list(NOTE_DIR.glob('*'))
    for note in notes:
        name = note.name
        meta_path = META_DIR / str(name + '.json')
        if not meta_path.exists():
            save_meta_data(note.name)
        with meta_path.open() as f:
            meta = json.load(f)
        title = meta['title']
        print(f'{note.name}{Fore.GREEN}:{Style.RESET_ALL}{title}')

def edit_command(note_name):
    """
    This will open editor at note_name.
    """
    notes = list(NOTE_DIR.glob(note_name))
    logging.debug(f'notes:{notes}')
    if not notes:
        print(f'{Fore.RED}{args[1]} is not found.{Style.RESET_ALL}')

    note_name = notes[0].name
    logging.debug(f'note_name:{note_name}')

    # open note
    open_note(temporary_note_name)

    # save meta data
    save_meta_data(temporary_note_name)


def main():
    print(f'{Style.RESET_ALL}', end="")
    logging.debug('call main')

    parser = argparse.ArgumentParser()
    parser.add_argument('first')
    args = parser.parse_args()

    args = sys.argv
    logging.debug('sys.args:%s'% args)

    if len(args) > 1 and sys.argv[1] == 'create':
        logging.debug('call create command')
        create_command()

    elif len(args) > 1 and sys.argv[1] == 'list':
        logging.debug('call list command')
        list_command()

    elif len(args) == 2:
        logging.debug('call edit command')
        note_name = args[1]
        edit_command(note_name)


if __name__=='__main__':
    import pdb;pdb.set_trace()
    main()
