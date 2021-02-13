from csv import DictReader
from datetime import datetime
from joplin import notebook, note, tag, tag_note, jex

LOCATION = (0, 0, 0)
CREATOR = "SYSTEM"

AUTHORS = {}
BOOKS = {}
TAGS = {}


def __database_nb(key, obj, fn, args={}):
    if key in obj:
        return obj[key]
    else:
        ide = fn(**args)
        obj[key] = ide
        return ide


def __date(data, pattern):
    try:
        res = datetime.strptime(data, pattern)
    except ValueError:
        res = datetime.strptime(data, '%d/%m/%Y')
    return res.isoformat('T', 'milliseconds')


def __title(title, subtitle):
    ref = '[{}] '.format('{0:04d}'.format(subtitle) if type(subtitle) == 'Number' else subtitle) \
        if len(subtitle) and len(subtitle) < 7 else ''
    return '{}{}'.format(ref, title)


def __metadata(text, row):
    values = ['author', 'book', 'date', 'ref']
    return text + '\n\n\n\n' + "\n".join(['- {}'.format(row[value]) for value in values if row[value]])


def ini_process(nb="IMPORT"):
    return notebook(nb)


def end_process(outfile="joplin"):
    return jex(outfile)


def csv_process(infile, location=LOCATION, creator=CREATOR, parent=None, metadata=True, outfile=None,
                dateformat='%d/%m/%Y %H:%M:%S', encoding='utf-8-sig'):
    with open(infile, encoding=encoding) as csv_file:
        reader = DictReader(csv_file, delimiter=',')

        nb = ini_process() if parent is None else parent

        for row in reader:
            date = __date(row['date'], dateformat)
            title = __title(row['title'], row['ref'])
            body = __metadata(row['text'], row) if metadata else row['text']

            author = __database_nb(row['author'], AUTHORS, notebook,
                                   {'title': row['author'].upper(), 'parent': nb, 'date': date}
                                   )
            __database_nb(author, BOOKS, dict)
            book = __database_nb(row['book'], BOOKS[author], notebook,
                                 {'title': row['book'], 'parent': author, 'date': date}
                                 )

            quote = note(
                title, body, book, date, author=creator,
                latitude=location[0], longitude=location[1], altitude=location[2]
            )

            if len(row['tags']):
                for key in row['tags'].split(','):
                    keyword = __database_nb(key.strip(), TAGS, tag, {'title': key.strip(), 'date': date})
                    tag_note(keyword, quote)

    return jex(outfile) if outfile else None
