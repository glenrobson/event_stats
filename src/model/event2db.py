#!/usr/local/bin/python3

import sqlite3
from eventbrite import Eventbrite
import sys
import os
from dateutil import parser
import json
import arrow

def createDB(conn):
    conn.execute("drop table if exists users")
    conn.execute("create table if not exists users (id varchar(150) UNIQUE PRIMARY KEY, order_id varchar(150), name varchar(150), email varchar(150), ticket varchar(150), company varchar(256), last_mod DATE, created DATE)") # id should be date+amount
    conn.execute("drop table if exists question_link")
    conn.execute("create table if not exists question_link(user_id varchar(150),question_id varchar(150),answer varchar(254))") # fragment is the page of the pdf
    conn.execute("drop table if exists questions")
    conn.execute("create table if not exists questions(question_id varchar(150),type varchar(150), question varchar(254), parent_id  varchar(150))") # fragment is the page of the pdf
    conn.execute("create table if not exists updates(id varchar(150),timestamp date)") # fragment is the page of the pdf

def fixname(name):
    return name

def findQuestion(answers, question_id):
    for question in answers:
        if question["question_id"] == question_id:
            if "answer" in question:
                return question["answer"]
            else:
                return ""
def loadQuestions(eventbrite, eventId, conn):                
    questionsResponse = eventbrite.get('/events/%s/questions/' % eventId)

    questions = {}
    for question in questionsResponse['questions']:
        parentId = None
        if 'parent_id' in question:
            parentId = question['parent_id']
        returnValue = conn.execute('INSERT INTO questions VALUES (?, ?, ?, ?)', [ question['id'], question["type"], question["question"]['text'], parentId])
        questions[question['id']] = question["question"]['text']

    return questions

def loadDb(config):
    eventId = config['id']
    db_file = config['db']
    
    directory = os.path.dirname(db_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    conn = sqlite3.connect(db_file)
    createDB(conn)

    if 'eventbrite_key' not in os.environ:
        print('Required enviroment var "eventbrite_key" missing. Exiting...')
        return
    
    eventbrite = Eventbrite(os.environ['eventbrite_key'])

    questions = loadQuestions(eventbrite, eventId, conn)

    response = eventbrite.get('/events/%s/attendees/' % eventId)
    page = int(response["pagination"]["page_number"])
    pageCount = int(response["pagination"]["page_count"])
    while page <= pageCount:
        for attendee in response["attendees"]:
            if attendee["status"] == "Attending":
                user_id = attendee["id"]
                order_id = attendee['order_id']
                name = fixname(attendee["profile"]["name"])
                if "email" in attendee["profile"]:
                    email = attendee["profile"]["email"]
                else:
                    print ("MISSING email for %s" % attendee["profile"])
                
                ticket = attendee["ticket_class_name"]

                if 'company' in attendee["profile"]:
                    company = attendee["profile"]['company']
                else:
                    for questionId in config['company']:
                        # get from custom quetsions
                        company = findQuestion(attendee["answers"],questionId) # non consortium
                        if company:
                            break

                lastmod = parser.parse(attendee["changed"])
                created = parser.parse(attendee["created"])

                returnValue = conn.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [ user_id, order_id, name, email, ticket, company, lastmod, created])

                for question in attendee["answers"]:
                    question_id = question["question_id"]
                    if "answer" in question:
                        answer = question["answer"]
                        returnValue = conn.execute('INSERT INTO question_link VALUES (?, ?, ?)', [ user_id, question_id, answer])
                    else:
                        returnValue = conn.execute('INSERT INTO question_link (user_id, question_id) VALUES (?, ?)', [ user_id, question_id])

        page += 1
        if page <= pageCount:
            response = eventbrite.get('/events/%s/attendees/?page=%s' % (eventId, page))

    date = arrow.now()
    conn.execute('insert into updates VALUES(?,?)', [date.timestamp, date.datetime])
    conn.commit()
    conn.close()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:\n\tevent2db.py [conf_file]")
        print ("Arg no = %s" % len(sys.argv))
        sys.exit(0)

    with open(sys.argv[1], 'r') as f:
        config = json.load(f)
        loadDb(config)
    
    
