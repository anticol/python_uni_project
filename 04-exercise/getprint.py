import sqlite3
import os, re, sys, json
from collections import OrderedDict

DATABASE_FILE = 'scorelib.dat'

def main():
    print_id = sys.argv[1]

    conn = sqlite3.connect(DATABASE_FILE)
    conn.text_factory = str
    cur = conn.cursor()

    cur.execute(
        'SELECT person.name, person.born, person.died  FROM person JOIN score_author ON person.id = score_author.composer WHERE score = (SELECT edition.score FROM print JOIN edition ON print.edition = edition.id WHERE print.id = ?)',
        (print_id,))
    result = cur.fetchall()
    authors = []
    for i in result:
        author = OrderedDict()
        author['name'] = i[0]
        author['born'] = i[1]
        author['died'] = i[2]
        authors.append(author)

    if(len(authors) != 0):
        print(json.dumps(authors, indent=4, ensure_ascii=False))

    conn.close()

main()
