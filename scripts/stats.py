#!/usr/local/bin/python3

import sqlite3
import sys

def printSummary(conn, questionId):
    results = conn.execute('select answer, count(answer) as count from users inner join question_link on users.id = question_link.user_id where question_id = ? group by answer order by count desc;', [questionId])
    total=0
    for result in results:
        result = printAndaddStatic(questionId, result)
        total+=result[1]
    print ("Total: %s" % total)

def printAndaddStatic(question,result):
    answer = result[0]
    count = result[1]
    if question == '18401662':
        if answer != 'I do not want a t-shirt':
            print (" * %s - %s/%s max - spare: %s" % (answer,count, ordered, (ordered - count)))
        else:
            print (" * %s - %s" % (answer,count))
    elif question == '18549982' and answer == 'Yes':
        print (" * %s - %s/%s max " % (answer,count,215))
    elif question == '18401802' and answer == 'Yes':
        print (" * %s - %s/%s max " % (answer,count,210))
    else:
        print (" * %s - %s " % (answer,count))

    return (answer,count)

def plusTotal(dictonary, key):
    if key:
        if key not in dictonary:
            dictonary[key] = 1
        else:
            dictonary[key] += 1

def normalize(string):
    if string:
        if " " in string:
            return " ".join(string.split())
        else:
            return string
    else:
        return ""

def processWorkshops(conn):
    results = conn.execute('select user_id, answer from users inner join question_link on users.id = question_link.user_id where question_id = "22866012" and ticket in ("Non-IIIF Consortium Member","IIIF Consortium Member","IIIF Staff Ticket","Göttingen Host Ticket", "Workshop Only - Tuesday, June 25th");')

    morning = 0
    afternoon = 0
    workshops = {}
    for result in results:
        answer = result[1]
        #print (result)
        if not answer:
            plusTotal(workshops, "None")
        else:
            if 'Morning' in answer:
                morning += 1
            if 'Afternoon' in answer:
                afternoon += 1
            key = ""
            if '|' in answer:
                for workshop in answer.split('|'):
                    workshop = normalize(workshop)
                    plusTotal(workshops,workshop)
            else:
                plusTotal(workshops,normalize(answer))

    return {
        "morning": morning,
        "afternoon": afternoon,
        "workshops": workshops
    }

def processRole(conn, questionId):
    results = conn.execute('select user_id, answer from users inner join question_link on users.id = question_link.user_id where question_id = ?;', [questionId])

    roles = {}
    for result in results:
        answer = result[1]
        if '|' in answer:
            for role in answer.split('|'):
                role = normalize(role)
                plusTotal(roles,role)
        else:
            plusTotal(roles,normalize(answer))

    return roles

if __name__ == "__main__":
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    else:
        mode = 'default'

    conn = sqlite3.connect('db/conference.db')
    print("Showcase Attendees:")
    results = conn.execute('select ticket, count(ticket) as count from users where ticket in ("IIIF Showcase - Monday, June 24th") group by ticket;')
    total = 0
    for result in results:
        print (" * %s - %s" % (result[0], result[1]))
        total += result[1]

    print ('Total: %s\n' % total)

    print("Conference Attendees:")
    total=0
    results = conn.execute('select ticket, count(ticket) as count from users where ticket in ("Non-IIIF Consortium Member","IIIF Consortium Member","IIIF Staff Ticket","Göttingen Host Ticket") group by ticket ;')
    for result in results:
        print (" * %s - %s" % (result[0], result[1]))
        total += result[1]
    print ("Total: %s" % total)
    results = conn.execute('select ticket, count(ticket) as count from users where ticket in ("Workshop Only - Tuesday, June 25th") group by ticket;')
    total = 0
    for result in results:
        print (" * %s - %s" % (result[0], result[1]))
        total += result[1]


   
    print ("\nWorkshops:")
    workshops = processWorkshops(conn)
    for workshop in workshops["workshops"]:
        print (" * %s - %s" % (workshop, workshops["workshops"][workshop]))
    print ("Workshops: morning - %s/125, afternoon - %s/125" % (workshops["morning"], workshops["afternoon"]))

    print ("\nT-Shirt sizes:")
    printSummary(conn, '22866123')

    if mode == 'full':
        print ("\nNew to IIIF?")
        printSummary(conn, '22866215')

        print ("\nRole type:")
        roles = processRole(conn, '22866225')
        for role in roles:
            print (" * %s - %s" % (role, roles[role]))

        print ("\nInstitutions:")
        results = conn.execute("select company, count(*) as count from users group by company order by count desc;")
        for row in results:
            print (" * %s - %s" % (row[0],row[1]))

    if mode == 'food':
        print("\nFood preferences:")
        printSummary(conn, '22866048')
        print('\nComments:')
        results = conn.execute('select ticket, answer from question_link inner join users on question_link.user_id = users.id where question_id = "22866049" and answer is not null')
        for row in results:
            print ('({}): {}'.format(row[0], row[1]))
    
        print("\nNumber attending Consortium Reception:")
        printSummary(conn, '22866288')

        print("\nNumber attending Conference Reception:")
        printSummary(conn, '22866275')

