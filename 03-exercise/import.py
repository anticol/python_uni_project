from test import *
import sqlite3
import os, re

if os.path.isfile(sys.argv[2]):
    os.remove(sys.argv[2])
    #os.remove("scorelib.dat")

TABLES = ["""CREATE TABLE person (
                id integer primary key not null,
                born integer,
                died integer,
                name varchar not null
                )""",
          """CREATE TABLE score (
                id integer primary key not null,
                name varchar,
                genre varchar,
                key varchar,
                incipit varchar,
                year integer
                )""",
          """CREATE TABLE voice (
                id integer primary key not null,
                number integer not null, -- which voice this is
                score integer references score( id ) not null,
                range varchar,
                name varchar
                )""",
          """CREATE TABLE edition (
                id integer primary key not null,
                score integer references score( id ) not null,
                name varchar,
                year integer
                )""",
          """CREATE TABLE score_author (
                id integer primary key not null,
                score integer references score( id ) not null,
                composer integer references person( id ) not null 
                )""",
          """CREATE TABLE edition_author (
                id integer primary key not null,
                edition integer references edition( id ) not null,
                editor integer references person( id ) not null 
                )""",
          """CREATE TABLE print (
                id integer primary key not null,
                partiture char(1) default 'N' not null, -- N = No, Y = Yes, P = Partial
                edition integer references edition( id )
                )""",
          ]


def insertPeople(cur, people):
    for person in people:
        cur.execute("select * from person where name=?", (person.name,))
        personData = cur.fetchone()
        if personData is not None:
            if(person.born) is not None and personData[1] is None:
                cur.execute("UPDATE person SET born = ? WHERE id= ?", (person.born, personData[0],))
            if(person.died) is not None and personData[2] is None:
                cur.execute("UPDATE person SET died = ? WHERE id= ?", (person.died, personData[0],))
            continue
        cur.execute("INSERT INTO person ('born','died','name') VALUES(?,?,?)",
                    (person.born, person.died, person.name))


def insertComposition(cur, comp):
    #cur.execute("select id from score where name = ? and genre = ? and key = ? and incipit = ? and year = ?", (comp.name,comp.genre,comp.key,comp.incipit,comp.year,))
    cur.execute("select id from score where name = ? and genre = ? and key = ?", (comp.name,comp.genre, comp.key,))
    lastId = cur.fetchone()
    if lastId is None:
        cur.execute("INSERT INTO score ('name','genre','key','incipit','year') VALUES(?,?,?,?,?)",
                (comp.name, comp.genre, comp.key, comp.incipit, comp.year,))
        return cur.lastrowid
    else:
        return lastId[0]



def insertVoice(cur, editionID, voice, number):
    cur.execute("select id from voice where name = ? and number = ? and score = ? and range = ?", (voice.name, number, editionID, voice.range))
    voicedata = cur.fetchone()
    if voicedata is not None:
        return
    cur.execute("INSERT INTO voice ('number', 'score','range','name') VALUES(?,?,?,?)",
                (number, editionID, voice.range, voice.name,))


def insertCompositionComposer(cur, composers, compositionId):
    for person in composers:
        cur.execute("SELECT id FROM person WHERE name=?", (person.name,))
        personId = cur.fetchone()[0]
        cur.execute("INSERT INTO score_author ('score','composer') VALUES(?,?)",
                    (compositionId, personId))


def insertVoices(cur, compId, voices):
    number = 1
    for v in voices:
        insertVoice(cur, compId, v, number)
        number = number + 1

#DONE
def insertEdition(cur, compId, edition):
        cur.execute("INSERT INTO edition ('score','name','year') VALUES(?,?,?)",
                (compId, edition.name, edition.year,))
        return cur.lastrowid

def insertEditionAuthor(cur,editionId,edition):
    for author in edition.authors:
        cur.execute("SELECT id FROM person WHERE name=?", (author.name,))
        editorId = cur.fetchone()[0]
        cur.execute("INSERT INTO edition_author ('edition','editor') VALUES(?,?)",
                (editionId,editorId))

def insertPrint(cur,print_obj,editionId):
    partiture = 'Y' if print_obj.partiture is True else 'N'
    cur.execute("INSERT INTO print ('id','partiture','edition') VALUES(?,?,?)",
                (print_obj.print_id,partiture,editionId))
def main():
    conn = sqlite3.connect(sys.argv[2])
    conn.text_factory = str
    cur = conn.cursor()

    for i in TABLES:
        cur.execute(i)

    for i in load(sys.argv[1]):
        insertPeople(cur, i.edition.authors + i.edition.composition.authors)
        compId = insertComposition(cur, i.edition.composition)
        insertVoices(cur, compId, i.edition.composition.voices)
        insertCompositionComposer(cur, i.edition.composition.authors, compId)
        editionId = insertEdition(cur, compId, i.edition)
        insertEditionAuthor(cur,editionId,i.edition)
        insertPrint(cur,i,editionId)
    conn.commit()
    conn.close()

main()
