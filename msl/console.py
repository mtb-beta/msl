import os
import sys
import uuid
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

def main():
    logging.debug('call main')
    args = sys.argv
    logging.debug('sys.args:%s'% args)

    if len(args) > 1 and sys.argv[1] == 'create':
        logging.debug('call create command')
        temporary_note = str(uuid.uuid1())
        note_path = Path('~/.msl/', temporary_note)
        (Path.home() / '.msl/').mkdir(exist_ok=True)
        logging.debug(note_path)
        os.system("vim {}".format(note_path))

if __name__=='__main__':
    main()
