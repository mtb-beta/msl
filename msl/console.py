import os
import sys
import uuid
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

DATA_DIR = Path.home() / '.msl/'

def main():
    logging.debug('call main')
    args = sys.argv
    logging.debug('sys.args:%s'% args)

    if len(args) > 1 and sys.argv[1] == 'create':
        logging.debug('call create command')

        temporary_note = str(uuid.uuid1())
        note_path = DATA_DIR / temporary_note
        DATA_DIR.mkdir(exist_ok=True)
        logging.debug(note_path)
        os.system("vim {}".format(note_path))

if __name__=='__main__':
    main()
