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

from msl import settings
from msl import group, note

#logging.basicConfig(level=logging.DEBUG)

def main():
    print(f'{Style.RESET_ALL}', end="")
    logging.debug('call main')

    #parser = argparse.ArgumentParser()
    #parser.add_argument('first')
    #args = parser.parse_args()

    args = sys.argv
    logging.debug('sys.args:%s'% args)

    if len(args) > 1 and args[1] == 'group':
        logging.debug('call group command')
        group.group_command(args[1:])

    if len(args) == 1 or args[1] == 'create':
        logging.debug('call create command')
        note.create_command()

    elif len(args) > 1 and args[1] == 'list':
        logging.debug('call list command')
        note.list_command()

    elif len(args) > 2 and args[1] == 'import':
        logging.debug('call import command')
        note.import_command(args[2])

    elif len(args) > 2 and args[1] == 'grep':
        logging.debug('call grep command')
        note.grep_command(args[2])

    elif len(args) > 2 and args[1] == 'delete':
        logging.debug('call delete command')
        note.delete_command(args[2])

    elif len(args) == 2:
        logging.debug('call edit command')
        note_name = args[1]
        note.edit_command(note_name)


if __name__=='__main__':
    import pdb;pdb.set_trace()
    main()
