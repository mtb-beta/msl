import uuid
import json
from datetime import datetime

from msl import settings

def create_command(group_name):
    """
    This command craete group.
    """
    group_id = str(uuid.uuid4())
    data = {}
    data['created_at'] = datetime.now().isoformat(timespec='seconds')
    data['title'] = group_name
    data['note'] = {}

    group_path = settings.GROUP_DIR / group_id
    with group_path.open(mode='w') as json_file:
        json.dump(data, json_file)


def group_console(args):
    if len(args) > 1 and args[1] == "create":
        create_command(args[2])
    else:
        print('command not found')

