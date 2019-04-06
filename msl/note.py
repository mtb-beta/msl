import os
import uuid
import logging
import json
from pathlib import Path
from datetime import datetime

from colorama import Fore, Style
from jinja2 import Template
import markdown

from msl import settings


BASE_DIR = settings.BASE_DIR
META_DIR = settings.META_DIR
NOTE_DIR = settings.NOTE_DIR
BUILD_DIR = settings.BUILD_DIR


class Note:
    def __init__(self):
        self.note_id = str(uuid.uuid1())

    @property
    def path(self):
        return NOTE_DIR / self.note_id

    @property
    def build_path(self):
        return BUILD_DIR / (self.note_id + ".html")

    @property
    def meta_path(self):
        return META_DIR / str(self.note_id + '.json')

    def open(self):
        logging.debug(f"open_note:{self.note_id}")
        os.system("vim {}".format(self.path))

    def save(self):
        save_meta_data(self.note_id)

    @classmethod
    def load(clz, note_path):
        note = Note()
        note.note_id = note_path.name
        return note

    @property
    def content(self):
        return self.path.read_text()

    @property
    def html(self):
        return markdown.markdown("#" + self.content)


    def build(self):
        template = Template(settings.BUILD_TEMPLATE)
        html_content = template.render(content=self.html)
        self.build_path.write_text(html_content)

    @property
    def title(self):
        if not self.meta_path.exists():
            save_meta_data(self.note_id)
        with self.meta_path.open() as f:
            meta = json.load(f)
        return meta['title']

    def cat(self):
        os.system("cat {}".format(self.path))

class NoteManager:
    def find(self, note_name):
        if len(note_name) == 36:
            notes_path = list(NOTE_DIR.glob(note_name))
        else:
            notes_path = list(NOTE_DIR.glob(note_name+"*"))

        notes = [Note.load(note_path) for note_path in notes_path]
        return notes

    def get(self, note_name):
        notes = self.find(note_name)

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

        return notes[0]

    def delete(self, note_name):
        notes = self.find(note_name)

        if len(notes) != 1:
            print(f'{note_name} can not find.')
            return

        os.remove(notes[0].path)
        settings.repo.index.remove(['*'])
        settings.repo.index.add(['*'])
        settings.repo.index.commit("delete:{}".format(note_name))

    def all(self):
        notes = list(NOTE_DIR.glob('*'))
        for note in notes:
            yield self.get(note.name)

    def build(self, note_name):
        note = self.get(note_name)
        note.build()
        return note

    @property
    def build_path(self):
        return BUILD_DIR / "index.html"

    @property
    def html(self):
        contents_list = []
        for note in self.all():
            contents_list.append(f'- [{note.title}]({note.build_path})')

        markdown_content = "\n".join(contents_list)
        return markdown.markdown(markdown_content)

    def build_index(self):
        template = Template(settings.BUILD_TEMPLATE)
        html_content = template.render(content=self.html)
        self.build_path.write_text(html_content)

    def search(self, keyword):
        result = []
        for note in self.all():
            if keyword in note.content:
                result.append(note)
        return result

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

    data['hostname'] = settings.HOSTNAME

    json_note_path = META_DIR / str(note_name + '.json')
    with json_note_path.open(mode='w') as json_file:
        json.dump(data, json_file)

    settings.repo.index.add(['*'])
    settings.repo.index.commit("save:{}".format(note_name))


def create_note_name():
    return str(uuid.uuid1())


def create_command():
    """
    This command craete note.
    """
    temporary_note = Note()
    temporary_note.open()
    temporary_note.save()


def list_command(option):
    """
    This command list notes.
    """
    for note in note_manager.all():
        if 'strict' in option and option['strict']:
            print(f'{note.note_id}{Fore.GREEN}:{Style.RESET_ALL}{note.title}')
        else:
            print(f'{note.note_id[:8]}{Fore.GREEN}:{Style.RESET_ALL}{note.title}')


def edit_command(note_name):
    """
    This will open editor at note_name.
    """
    note = note_manager.get(note_name)
    if not note:
        return

    note.open()
    note.save()


def import_command(path_str):
    logging.info(f'import file is {path_str}')

    target_path = Path(path_str)
    if target_path.is_dir():
        notes_path = list(target_path.glob('*'))
    else:
        notes_path = [target_path]

    for note_path in notes_path:
        # load content
        if note_path.name == ".DS_Store":
            continue
        content = note_path.read_text()

        # create new file
        new_note_name = create_note_name()
        new_note_path = NOTE_DIR / new_note_name
        # exclude extension from title
        title = note_path.name.split('.')[0]
        new_note_path.write_text(title + '\n' + content)
        save_meta_data(new_note_name)
        print(f'create note title {new_note_name}')


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
    note_manager.delete(note_name)
    print(f'{note_name} deleted.')


def build_command(note_name):
    """
    This command build note to html.
    """
    if note_name == "all":
        for note in note_manager.all():
            note_manager.build(note.note_id)
            print(f'{note.build_path} build.')
        note_manager.build_index()
        print(f'{note_manager.build_path} build.')
    else:
        note = note_manager.build(note_name)
        print(f'{note.build_path} build.')


def cat_command(note_name):
    """
    This command call cat command at note.
    """
    note = note_manager.get(note_name)
    if not note:
        return

    note.cat()


def search_command(keyword):
    for note in note_manager.search(keyword) :
        print(f'{note.note_id[:8]}{Fore.GREEN}:{Style.RESET_ALL}{note.title}')
