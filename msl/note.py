import os
import uuid
import logging
import json
from pathlib import Path
from datetime import datetime

from colorama import Fore, Style

from msl import settings


BASE_DIR = settings.BASE_DIR
META_DIR = settings.META_DIR
NOTE_DIR = settings.NOTE_DIR


class Note:
    def __init__(self):
        self.note_id = str(uuid.uuid1())

    def open(self):
        note_name = self.note_id
        logging.debug(f"open_note:{note_name}")
        note_path = NOTE_DIR / note_name
        os.system("vim {}".format(note_path))

    def save(self):
        save_meta_data(self.note_id)

    @classmethod
    def load(clz, note_path):
        note = Note()
        note.note_id = note_path.name
        return note

class NoteManager:
    def get(self, note_name):
        if len(note_name) == 36:
            notes = list(NOTE_DIR.glob(note_name))
        else:
            notes = list(NOTE_DIR.glob(note_name+"*"))

        logging.debug(f'notes:{notes}')
        if not notes:
            print(f'{Fore.RED}{note_name} is not found.{Style.RESET_ALL}')
            return

        if len(notes) != 1:
            print(f'{Fore.RED}There are many [{note_name}] note.{Style.RESET_ALL}')
            for note in notes:
                print(f'  - {note.name}')
            return

        logging.debug(f'note_name:{note_name}')

        return Note.load(notes[0])

note_manager = NoteManager()


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

    json_note_path = META_DIR / str(note_name + '.json')
    with json_note_path.open(mode='w') as json_file:
        json.dump(data, json_file)

    settings.repo.index.add(['*'])
    settings.repo.index.commit("save:{}".format(note_name))

def list_note():
    notes = list(NOTE_DIR.glob('*'))
    for note in notes:
        name = note.name
        meta_path = META_DIR / str(name + '.json')
        if not meta_path.exists():
            save_meta_data(note.name)
        with meta_path.open() as f:
            meta = json.load(f)
        title = meta['title']
        yield note.name, title


def create_note_name():
    return str(uuid.uuid1())


def create_command():
    """
    This command craete note.
    """
    temporary_note = Note()
    temporary_note.open()
    temporary_note.save()


def list_command():
    """
    This command list notes.
    """
    for note_name, title in list_note():
        print(f'{note_name[:8]}{Fore.GREEN}:{Style.RESET_ALL}{title}')


def edit_command(note_name):
    """
    This will open editor at note_name.
    """
    note = note_manager.get(note_name)
    if not note:
        return

    note.open()
    note.save()


def import_command(path):
    logging.info(f'import file is {path}')

    target_path = Path(path)
    if target_path.is_dir():
        notes = list(target_path.glob('*'))
    else:
        notes = [target_path]

    for note in notes:
    # load content
        content = note.read_text()

        # create new file
        new_note_name = create_note_name()
        new_note_path = NOTE_DIR / new_note_name
        new_note_path.write_text(note.name + '\n' + content)
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
                    print(f'{note.name[:8]}{Fore.GREEN}:{Style.RESET_ALL}{print_line}')

def delete_command(note_name):
    if len(note_name) == 36:
        notes = list(NOTE_DIR.glob(note_name))
    else:
        notes = list(NOTE_DIR.glob(note_name+"*"))

    if len(notes) != 1:
        print(f'{note_name} can not find.')
        return

    os.remove(notes[0])
    print(f'{note_name} deleted.')
