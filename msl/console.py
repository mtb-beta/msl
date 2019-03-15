import os
import sys
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    logging.debug('call main')
    args = sys.argv
    logging.debug('sys.args:%s'% args)

    if len(args) > 1 and sys.argv[1] == 'create':
        logging.debug('call create command')
        temporary_note = str(uuid.uuid1())
        os.system("vim {}".format(temporary_note))

if __name__=='__main__':
    main()
