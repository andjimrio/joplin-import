# ref: https://gitlab.com/seawind/kindle-highlights-in-joplin
import re
import dateparser


path_highlights = "files/txt/My Clippings.txt"
separator = "=========="

highl_kws = 'subrayado|Subrayado' 
note_kws = 'nota|Nota'
page_kws = 'página'
added = 'Añadid. el' 
locs = 'posición|Pos\.'


def read_clippings_file(path,separator=separator):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read().split(separator)
    except:
        print(f"{path} is not accessible. Verify that the path is correct.")
        quit()


def get_highlight_data(hl):
    md = {}
    cont = hl.splitlines()
    cont = [md for md in cont if md != '']
    ## Book
    book = re.match(r'(?P<title>.*)\((?P<author>.*)\)', cont[0])
    md['title'] = book.group('title').strip()
    md['author'] = book.group('author').strip()
    ### defines if it's a note or a highlight -- So far, it only retrieves those elemets
    if re.search(highl_kws,cont[1]):
        md['type'] = 'highlight'
    elif re.search(note_kws,cont[1]):
        md['type'] = 'note'
    else:
        return None
    ## Location or position in the ebook
    loc = re.match(r'.*('+ locs + r') (?P<location>[0-9,-]+).*', cont[1])
    md['location'] = loc.group('location')
    ## Page
    try:
        pag = re.match(r'.*('+page_kws+') (?P<page>[0-9,-]+) |$', cont[1])
        md['page'] = pag.group('page')
    except:
        md['page'] = ''
    ## Date
    dateS = re.match(r".*("+added +") (?P<timestamp>.*) (?P<hour>[0-9]+)(H|:)(?P<minutes>[0-9]+)(H|:)(?P<seconds>[0-9]+)('|.)(?P<id>.*)$", cont[1])
    date = f"{dateS.group('timestamp')} {dateS.group('hour')}:{dateS.group('minutes')}:{dateS.group('seconds')}"
    date = date + dateS.group('id') if dateS.group('id') in ['AM','PM'] else date
    md['date_time'] = dateparser.parse(date)
    ### Assigns the body of the highlight or note
    md['highlight'] = cont[-1]
    return md


def get_highlights(path):
    highlights_list = read_clippings_file(path)
    highlights = []
    print ('Retrieving highlights')
    for hl in highlights_list:
        if hl!='\n':
            md = get_highlight_data(hl)
            if md:
                highlights.append(md)
    print (f'{len(highlights)} highlights retrieved from the original file.')
    return highlights


def main():
    highlights = get_highlights(path_highlights)
    print(highlights[-1])


if __name__ == '__main__':
    main()
