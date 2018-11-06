import sqlite3
import os, re, sys, json
from collections import OrderedDict

DATABASE_FILE = 'scorelib.dat'

def parsePeople(data):
    people = []
    for person in data:
        author = OrderedDict()
        author['name'] = person[2]
        author['born'] = person[0]
        author['died'] = person[1]
        people.append(author)
    return people

def parseVoices(voice_data):
    voices = OrderedDict()
    for voice in voice_data:
        v = OrderedDict()
        v['name'] = voice[2]
        v['range'] = voice[1]
        voices.update({str(voice[0]): v})

    return voices

def main():

    #author =  '%' + 'Carl Maria' + '%'
    author =  '%' + sys.argv[1] + '%'
    conn = sqlite3.connect(DATABASE_FILE)
    conn.text_factory = str
    cur = conn.cursor()
    RESULT_FOR_PRINT = []

    cur.execute('SELECT * FROM person WHERE person.name LIKE ?',(author,))
    authors = cur.fetchall()

    for author in authors:
        composer_id = author[0]
        composer_name = author[3]
        print_instance = OrderedDict()
        PRINTS = []
        RESULT = OrderedDict({composer_name: PRINTS})

        cur.execute('SELECT * FROM score JOIN (SELECT * FROM score_author JOIN person ON score_author.composer = person.id WHERE person.id = ?) ON score.id = score', (composer_id,))
        scores_data = cur.fetchall()

        for score in scores_data:
            print_instance = OrderedDict()
            score_id = score[0]
            title = score[1]
            genre = score[2]
            key = score[3]
            incipit = score[4]
            composition_year = score[5]

            cur.execute('SELECT born,died,name FROM score_author JOIN person ON score_author.composer = person.id WHERE score = ?', (score_id,))
            composers_arr = parsePeople(cur.fetchall())
            cur.execute('SELECT * FROM edition WHERE score = ?', (score_id,))
            editions_data = cur.fetchall()

            for edition in editions_data:

                edition_id = edition[0]
                edition_name = edition[2]
                cur.execute('SELECT born,died,name FROM edition_author JOIN person ON edition_author.editor = person.id WHERE edition = ?', (edition_id,))
                editors_array = parsePeople(cur.fetchall())
                cur.execute('SELECT * FROM print WHERE edition = ?', (edition_id,))
                print_data = cur.fetchone()
                cur.execute('SELECT number, range, name FROM voice WHERE score = ?', (score_id,))
                voice_data = cur.fetchall()


                print_instance['Print Number'] = print_data[0]
                print_instance['Composer'] = composers_arr
                print_instance['Title'] = title
                print_instance['Genre'] = genre
                print_instance['Key'] = key
                print_instance['Composition Year'] = composition_year
                print_instance['Edition'] = edition_name
                print_instance['Editor'] = editors_array
                print_instance['Voices'] = parseVoices(voice_data)
                print_instance['Partiture'] = True if print_data[1] == 'Y' else False
                print_instance['Incipit'] = incipit
                PRINTS.append(print_instance)

        if len(print_instance) != 0:
            RESULT_FOR_PRINT.append(RESULT)
            #print(json.dumps(RESULT, indent=2, ensure_ascii=False))

    if len(RESULT_FOR_PRINT) != 0:
        print(json.dumps(RESULT_FOR_PRINT, indent=2, ensure_ascii=False))


    conn.close()

main()
