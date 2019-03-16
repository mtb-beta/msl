import os
import sys
import uuid
import logging
import json
from pathlib import Path
from datetime import datetime

from colorama import Fore, Style

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

BASE_DIR = Path.home() / '.msl/'
META_DIR = BASE_DIR / 'meta'
NOTE_DIR = BASE_DIR / 'notes'

def main():
    print(f'{Style.RESET_ALL}', end="")
    logging.debug('call main')
    args = sys.argv
    logging.debug('sys.args:%s'% args)

    if len(args) > 1 and sys.argv[1] == 'create':
        logging.debug('call create command')

        temporary_note = str(uuid.uuid1())
        temporary_note_path = BASE_DIR / temporary_note
        BASE_DIR.mkdir(exist_ok=True)
        logging.debug(temporary_note_path)
        # open note
        os.system("vim {}".format(temporary_note_path))

        # save note
        if temporary_note_path.exists():
            logging.debug('save note')
            # save meta data
            data = {}
            data['created_at'] = datetime.now().isoformat(timespec='seconds')
            with temporary_note_path.open() as f:
                data['title'] = f.readline().replace('\n', '')

            META_DIR.mkdir(exist_ok=True)
            json_note_path = META_DIR / str(temporary_note + '.json')
            with json_note_path.open(mode='w') as json_file:
                json.dump(data, json_file)

            # move temporary_note
            NOTE_DIR.mkdir(exist_ok=True)
            temporary_note_path.rename(NOTE_DIR/temporary_note_path.name)

    if len(args) > 1 and sys.argv[1] == 'list':
        logging.debug('call list command')
        notes = list(NOTE_DIR.glob('*'))
        for note in notes:
            name = note.name
            meta_path = META_DIR / str(name + '.json')
            with meta_path.open() as f:
                meta = json.load(f)
            title = meta['title']
            print(f'{note.name}{Fore.GREEN}:{Style.RESET_ALL}{title}')

if __name__=='__main__':
    main()
