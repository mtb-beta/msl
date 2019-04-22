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

    if len(args) > 1 and (args[1] == 'group' or args[1] == 'gp'):
        group.group_console(args[1:])

    if len(args) == 1 or args[1] == 'create':
        note.create_command()

    elif len(args) > 1 and args[1] == 'list' or args[1] == 'l':
        option = {}
        if len(args) > 2 and "--strict" in args[2:]:
            option['strict'] = True

        if len(args) > 2 and "--all" in args[2:]:
            option['all'] = False
        else:
            option['all'] = True


        note.list_command(option)

    elif len(args) > 2 and args[1] == 'import':
        note.import_command(args[2])

    elif len(args) > 2 and args[1] == 'grep':
        note.grep_command(args[2])

    elif len(args) > 2 and args[1] == 'search' or args[1] == 's':
        note.search_command(args[2])

    elif len(args) > 2 and args[1] == 'delete':
        note.delete_command(args[2])

    elif len(args) > 2 and args[1] == 'build':
        note.build_command(args[2])

    elif len(args) > 2 and args[1] == 'merge':
        note.merge_command(args[2:])

    elif len(args) > 2 and args[1] == 'random' or args[1] == 'rand':
        note.random_command()

    elif len(args) > 2 and args[1] == 'cat':
        note.cat_command(args[2])

    elif len(args) == 2:
        note_name = args[1]
        note.edit_command(note_name)


if __name__=='__main__':
    import pdb;pdb.set_trace()
    main()
