from datetime import datetime
from uuid import uuid4
import tarfile
from os import remove

DATETIME = datetime.now().isoformat('T','milliseconds')
FILES = []


def __id():
    id = uuid4().hex
    return id, f'{id}.md'

def __xstr(s):
    return '' if s is None else str(s)

def __cstr(text, condition=None, alternative=''):
    return text if condition else alternative

def __line(key=None, value=None, jump=True):
    return "{}{}{}{}".format(__xstr(key), __cstr(': ', value is not None), __xstr(value), __cstr('\n', jump))


def __entity(type, title=None, body=None, parent='', date=None, args={}):
    obid, filename = __id()
    file = open(filename, 'w')

    if title is not None:
        file.write(__line(title))
        file.write(__line())

    if body is not None:
        file.write(__line(body))
        file.write(__line())
    
    data = {
        'id': obid, 'created_time': date, 'updated_time': date, **args,
        'user_created_time': date, 'user_updated_time': date, 'encryption_cipher_text': '',
        'encryption_applied': 0, 'is_shared': 0,
    }

    for k, v in data.items():
        file.write(__line(k, v))
            
    if parent is not None:
        file.write(__line('parent_id', parent))
    file.write(__line('type_', type, False))

    file.close()
    FILES.append(filename)
    return obid


def notebook(title, parent='', date=DATETIME):
    return __entity(2, title, parent=parent, date=date)

def tag(title, date=DATETIME):
    return __entity(5, title, date=date)

def tag_note(tag, note, date=DATETIME):
    return __entity(6, parent=None, date=date, args={'tag_id': tag, 'note_id': note})

def note(title, body, parent, date=DATETIME, latitude=0, longitude=0, altitude=0, author=''):
    return __entity(1, title, body, parent=parent, date=date, args={
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
