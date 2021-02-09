from datetime import datetime
from uuid import uuid4
import tarfile
from os import remove

DATETIME = datetime.now().isoformat('T','milliseconds')
FILES = []


def id():
    id = uuid4().hex
    return id, f'{id}.md'

def xstr(s):
    return '' if s is None else str(s)

def cstr(text, condition=None, alternative=''):
    return text if condition else alternative

def line(key=None, value=None, jump=True):
    return "{}{}{}{}".format(xstr(key), cstr(': ', value is not None), xstr(value), cstr('\n', jump))


def entity(type, title=None, body=None, parent='', date=None, args={}):
    obid, filename = id()
    file = open(filename, 'w')

    if title is not None:
        file.write(line(title))
        file.write(line())

    if body is not None:
        file.write(line(body))
        file.write(line())
    
    file.write(line('id', obid))
    file.write(line('created_time', date))
    file.write(line('updated_time', date))

    if len(args):
        for k, v in args.items():
            file.write(line(k, v))
            
    if parent is not None:
        file.write(line('parent_id', parent))

    file.write(line('user_created_time', date))
    file.write(line('user_updated_time', date))
    file.write(line('encryption_cipher_text', ''))
    file.write(line('encryption_applied', 0))
    file.write(line('is_shared', 0))
    file.write(line('type_', type, False))

    file.close()
    FILES.append(filename)
    return obid


def notebook(title, parent='', date=DATETIME):
    return entity(2, title, parent=parent, date=date)

def tag(title, date=DATETIME):
    return entity(5, title, date=date)

def tag_note(tag, note, date=DATETIME):
    return entity(6, parent=None, date=date, args={'tag_id': tag, 'note_id': note})

def note(title, body, parent, date=DATETIME, latitude=0, longitude=0, altitude=0, author=''):
    return entity(1, title, body, parent=parent, date=date, args={
        'is_conflict': 0, 'latitude': latitude, 'longitude': longitude, 'altitude': altitude,
        'author': author, 'source_url': '', 'is_todo': 0, 'todo_due': 0, 'todo_completed': 0,
        'source': 'python', 'source_application': 'kindle', 'application_data': '', 'order': 0
    })


def tar():
    tar = tarfile.open('joplin.jex', "w:")
    tar.format = tarfile.USTAR_FORMAT
    for name in FILES:
        tar.add(name)
        remove(name)
    tar.close()
    return tar
    


def jex():
    nbid = notebook("Notebook 1")
    print(nbid)
    ntid = note("Note 1", "Note 1", nbid)
    print(ntid)
    tgid = tag("Tag 1")
    print(tgid)
    tnid = tag_note(tgid, ntid)
    print(tnid)
    tar()


if __name__ == '__main__':
    jex()
