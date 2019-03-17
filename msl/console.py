import argparse
import os
import sys
import uuid
import logging
import json
import subprocess
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

def create_note_name():
    return str(uuid.uuid1())

def create_command():
    """
    This command craete note.
    """
    temporary_note_name = create_note_name()
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
    if len(note_name) == 36:
        notes = list(NOTE_DIR.glob(note_name))
    else:
        notes = list(NOTE_DIR.glob(note_name+"*"))

    logging.debug(f'notes:{notes}')
    if not notes:
        print(f'{Fore.RED}{note_name} is not found.{Style.RESET_ALL}')
        return

    logging.debug(f'note_name:{note_name}')

    note_name = notes[0].name
    # open note
    open_note(note_name)

    # save meta data
    save_meta_data(note_name)


def import_command(path):
    logging.info(f'import file is {path}')

    # load content
    content = Path(path).read_text()

    # create new file
    new_note_name = create_note_name()
    new_note_path = NOTE_DIR / new_note_name
    new_note_path.write_text(content)
    save_meta_data(new_note_name)

def grep_command(keyword):
    all_notes = NOTE_DIR.glob('*')

    # check all note loop
    for note in all_notes:
        with note.open() as f:
            # check all line loop
            for line in f:
                if keyword in line:
                    print_line = line.replace('\n', '')
                    print(f'{note.name}{Fore.GREEN}:{Style.RESET_ALL}{print_line}')


def main():
    print(f'{Style.RESET_ALL}', end="")
    logging.debug('call main')

    #parser = argparse.ArgumentParser()
    #parser.add_argument('first')
    #args = parser.parse_args()

    args = sys.argv
    logging.debug('sys.args:%s'% args)

    if len(args) == 1 or args[1] == 'create':
        logging.debug('call create command')
        create_command()

    elif len(args) > 1 and args[1] == 'list':
        logging.debug('call list command')
        list_command()

    elif len(args) > 2 and args[1] == 'import':
        logging.debug('call import command')
        import_command(args[2])

    elif len(args) > 2 and args[1] == 'grep':
        logging.debug('call grep command')
        grep_command(args[2])

    elif len(args) == 2:
        logging.debug('call edit command')
        note_name = args[1]
        edit_command(note_name)


if __name__=='__main__':
    import pdb;pdb.set_trace()
    main()
