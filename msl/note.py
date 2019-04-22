import os
import uuid
import logging
import json
import random
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
        """
        This will update meta data on note_name.
        """

        if not self.path.exists():
            logging.warning('There is not note_path.')
            return

        data = {}
        data['hostname'] = settings.HOSTNAME
        data['created_at'] = self.created_at.isoformat(timespec='seconds')
        data['updated_at'] =  datetime.now().isoformat(timespec='seconds')

        with self.meta_path.open(mode='w') as json_file:
            json.dump(data, json_file)

        settings.repo.index.add(['*'])
        settings.repo.index.commit("save:{}".format(self.note_id))

    @classmethod
    def load(clz, note_path):
        note = Note()
        note.note_id = note_path.name
        return note

    @property
    def meta(self):
        if not self.meta_path.exists():
            return {}

        with self.meta_path.open() as f:
            meta = json.load(f)
        return meta

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
        with self.path.open() as f:
            return f.readline().replace('\n', '')

    @property
    def created_at(self):
        if not self.meta_path.exists():
            return datetime.now()
        return datetime.strptime(self.meta['created_at'], "%Y-%m-%dT%H:%M:%S")

    @property
    def updated_at(self):
        if 'updated_at' in self.meta:
            return datetime.strptime(self.meta['updated_at'], "%Y-%m-%dT%H:%M:%S")
        return self.created_at

    def cat(self):
        os.system("cat {}".format(self.path))
        print('')

    def write(self, content):
        self.path.write_text(content)


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

    def all(self, sort='updated_at'):
        note_paths = list(NOTE_DIR.glob('*'))
        for note_path in sorted(
                note_paths,
                key=lambda note_path: getattr(self.get(note_path.name), sort),
                reverse=True
            ):
            yield self.get(note_path.name)

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
    for count, note in enumerate(note_manager.all()):
        if count > 10 and 'all' in option and option['all']:
            continue

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
        print('please set import path')
        return

    imported_dir = target_path / 'imported'
    imported_dir.mkdir(exist_ok=True)

    for note_path in notes_path:
        # load content
        if note_path.name == ".DS_Store":
            continue
        if note_path.is_dir():
            continue
        content = note_path.read_text()

        # create new file
        new_note = Note()
        # exclude extension from title
        title = note_path.name.split('.')[0]
        new_note.write(title + '\n' + content)
        new_note.save()
        print(f'create note title {new_note.title}')
        note_path.replace(imported_dir / note_path.name )


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


def merge_command(merge_note_ids):
    """
    This command merge the multi note.
    """
    merge_notes = []
    for note_id in merge_note_ids:
        note = note_manager.get(note_id)
        if note:
            merge_notes.append(note)

    new_content = "\n\n#".join(
        [ note.content for note in merge_notes]
    )
    temporary_note = Note()
    temporary_note.write(new_content)
    temporary_note.open()
    temporary_note.save()
    print('merged!')

def search_command(keyword):
    for note in note_manager.search(keyword) :
        print(f'{note.note_id[:8]}{Fore.GREEN}:{Style.RESET_ALL}{note.title}')

def random_command():
    notes = note_manager.all()
    note = random.choice(list(notes))
    print(f'{note.note_id[:8]}{Fore.GREEN}:{Style.RESET_ALL}{note.title}')
    note.cat()
