from __future__ import print_function


class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition  # instance of Edition
        self.print_id = int(print_id)  # integer from Print Number:
        self.partiture = partiture  # boolean

    # reconstructs and prints the original stanza
    def format(self):
        printData('Print Number:', self.print_id)
        printComposers(self.composition().authors)
        printData('Title:', self.composition().name)
        printData('Genre:', self.composition().genre)
        printData('Key:', self.composition().key)
        printData('Composition Year:', self.composition().year)
        printData('Edition:', self.edition.name)
        printEditors(self.edition.authors)
        printVoice(self.composition().voices)
        printData('Partiture:', 'yes' if self.partiture else 'no')
        printData('Incipit:', self.composition().incipit)
        print('')

    def composition(self):
        return self.edition.composition


class Edition:
    def __init__(self, composition, authors, name,year):
        self.composition = composition  # instance of Composition
        self.authors = authors  # a list of Person instances
        self.name = name  # string from Edition: field, or None
        self.year = year


class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors


class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range


class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died


def printData(n, data):
    if data is not None:
        print(n, ("%s" % data).strip())


def printVoice(d):
    count = 1
    for i in d:
        delimeter = ''
        range = i.range if i.range is not None else ''
        name = i.name if i.name is not None else ''
        if range != '':
            if name != '':
                delimeter = ', '
        print('Voice %d: %s%s%s' % (count, range.strip(), delimeter, name))
        count = count + 1


def printComposers(d):
    if d == []:
        return

    print('Composer: ', end='')
    delimeter = ''
    counter = 0
    for i in d:
        born = '' if i.born is None else i.born
        died = '' if i.died is None else i.died
        date = ' (' + born + '--' + died + ')' if born != '' or died != '' else ''
        if counter != 0:
            delimeter = '; '
        print('%s%s%s' % (delimeter, i.name.strip(), date), end='')
        counter = counter + 1

    print('')


def printEditors(d):
    if d == []:
        return
    delimeter = ''
    counter = 0
    print('Editor: ', end='')
    for i in d:
        if counter != 0:
            delimeter = ', '
        print('%s%s' % (delimeter, i.name), end='')
        counter = counter + 1

    print('')
