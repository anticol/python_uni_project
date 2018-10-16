from __future__ import print_function
import sys, os, re, codecs
from scorelib import Print, Edition, Composition, Voice, Person


def parsePerson(line):
    people = line.split(';')
    peopleInstances = []
    for item in people:
        if '(' not in item:
            parsedItem = Person(item.strip(), None, None)
            peopleInstances.append(parsedItem)
        else:
            r = re.search('[(](.*)[)]', item)
            isName = re.search('([^\d+*/-]+)', r.group(1))
            name = item.split('(')[0].strip() if isName is None else item.strip()
            born = re.search('^[*]?([0-9]{4})[-+]*[\s*-]', r.group(1))
            died = re.search('[-+]+([0-9]{4})$', r.group(1))
            born = born.group(1) if born is not None else None
            died = died.group(1) if died is not None else None
            parsedItem = Person(name, born, died)
            peopleInstances.append(parsedItem)
    return peopleInstances


def parseVoice(line):
    name = None
    range = None
    isRange = re.search('(\S+--\S+[^;,])[;,\s]+(.*)', line)

    if isRange is not None:
        range = isRange.group(1).strip()
        name = isRange.group(2).strip() if isRange.group(2) is not None else None
    else:
        name = line.strip()
    return Voice(name, range)


def parseComposition(line, voices_arr, people_arr):
    name = re.search("Title: (.*[\S].*)", line)
    genre = re.search("Genre: (.*[\S].*)", line)
    incipit = re.search("Incipit: (.*[\S].*)", line)
    year = re.search("Composition Year: *?.*([\d]{4})", line)
    key = re.search("Key: (.*[\S].*)", line)

    name_atr = name.group(1).strip() if name is not None else None
    genre_atr = genre.group(1).strip() if genre is not None else None
    incipit_atr = incipit.group(1).strip() if incipit is not None else None
    year_atr = int(year.group(1).strip()) if year is not None else None
    key_atr = key.group(1).strip() if key is not None else None

    return Composition(name_atr, incipit_atr, key_atr, genre_atr, year_atr, voices_arr, people_arr)


def parseEdition(line, editors_arr, composition,year):
    edition_name = re.search("Edition: (.*[\S].*)", line)
    edition_name = edition_name.group(1).strip() if edition_name is not None else None
    return Edition(composition, editors_arr, edition_name,year)


def parsePrint(line, edition):
    print_id = re.search("Print Number: (.*)", line)
    partiture_atr = False

    partiture = re.search("Partiture: (.*)", line)
    if partiture is not None:
        partiture_atr = False if 'yes' not in partiture.group(1) else True

    print_id_atr = print_id.group(1).strip()
    return Print(edition, print_id_atr, partiture_atr)


def parseEditors(line):
    editors_arr = []
    r = re.compile('(?:(?:[^\,]+\.?)(?:\,?\s+))?(?:[^\,]+\.?)')

    if line is not None:
        m = r.findall(line.group(1))
        for editor in m:
            person = Person(editor.strip(), None, None)
            editors_arr.append(person)

    return editors_arr


def load(filename):
    f = codecs.open(filename, 'r', errors='ignore')
    #f = open('scorelib.txt', 'r', encoding="utf-8")
    block = f.read().split('\n\n')
    print_arr = []

    for line in block:
        isEmpty = re.search("(\s)", line)
        if isEmpty is None:
            continue

        people_arr = []
        voices_arr = []

        composer = re.search("Composer: (.*[\S].*)", line)
        if composer is not None:
            people_arr = (parsePerson(composer.group(1)))

        range = re.findall("Voice [0-9]+:(.*[\S].*)", line)
        if range is not None:
            for i in range:
                voices_arr.append(parseVoice(i))

        editors = re.search("Editor: (.*[\S].*)", line)
        editors_arr = parseEditors(editors)

        composition = parseComposition(line, voices_arr, people_arr)
        publicationYear = re.search("Publication Year: *?.*([\d]{4})", line)
        year = int(publicationYear.group(1).strip()) if publicationYear is not None else None
        edition = parseEdition(line, editors_arr, composition,year)
        _print_ = parsePrint(line, edition)
        print_arr.append(_print_)

    return print_arr



