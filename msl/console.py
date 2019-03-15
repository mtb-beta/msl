import os
import sys
import uuid
import logging
import json
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

DATA_DIR = Path.home() / '.msl/'

def main():
    logging.debug('call main')
    args = sys.argv
    logging.debug('sys.args:%s'% args)

    if len(args) > 1 and sys.argv[1] == 'create':
        logging.debug('call create command')

        temporary_note = str(uuid.uuid1())
        temporary_note_path = DATA_DIR / temporary_note
        DATA_DIR.mkdir(exist_ok=True)
        logging.debug(temporary_note_path)
        # open note
        os.system("vim {}".format(temporary_note_path))

        # save note
        if temporary_note_path.exists():
            logging.debug('save note')
            data = {}
            with temporary_note_path.open() as note_file:
                data['content'] = note_file.readline()

            data['created_at'] = datetime.now().isoformat(timespec='seconds')
            json_note_path = DATA_DIR / str(temporary_note + '.json')
            with json_note_path.open(mode='w') as json_file:
                json.dump(data, json_file)

            os.remove(temporary_note_path)

if __name__=='__main__':
    main()
