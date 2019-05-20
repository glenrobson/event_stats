#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import sqlite3
import os
import json
from bottle import Bottle
from bottle import route, run, template,debug, get, post, static_file, request, redirect, response
from datetime import date, timedelta
import arrow
from __init__ import isDBReady
from __init__ import dbUpdating

gottingen = Bottle()

def getDB():
    return sqlite3.connect('db/conference.db')

@gottingen.route('/gottingen/index.html')
def indexPage():
    if isDBReady():
        return dbUpdating()

    ticketData = json.loads(ticketCounts())
    timeDiff = getUpdateTimeDiff()

    response.content_type = 'text/html'
    return template('src/view/gottingen/index.tpl', ticket_counts=ticketData, updateDiff=timeDiff)

def getUpdateTimeDiff():
    conn = getDB()

    result = conn.execute('select * from updates order by id desc limit 1;').fetchone()

    updateDate = arrow.get(result[1], 'YYYY-MM-DD HH:mm:ss.SSSSSSZ')
    diff = arrow.now() - updateDate

    return "{}".format(diff.seconds / 60)
@gottingen.route('/gottingen/showcase-attendees.json')
def showcaseAttendees():
    conn = getDB()
    results = conn.execute("select date(created), count(*) from users where ticket = 'IIIF Showcase - Monday, June 24th' group by date(created) order by created;")
    data = {}
    data ['cols'] = [
        {'id': 'date', 'label': 'Date', 'type': 'date'},
        {'id': 'count', 'label': 'Ticket Count', 'type': 'number'}
    ]    

    data['rows'] = []
    count = 0
    data['rows'].append({
          'c': [
            { 'v':"Date(2019,3,4)"},
            { 'v':count}
          ]
        })

    for result in results:
        count += int(result[1])
        splitDate = result[0].split('-')
        data['rows'].append({
          'c': [
            { 'v':"Date({},{},{})".format(splitDate[0], int(splitDate[1]) - 1, splitDate[2])},
            { 'v':count}
          ]
        })

    response.content_type = 'application/json'
    return json.dumps(data, indent=4)

@gottingen.route('/gottingen/conference-attendees.json')
def conferenceAttendees():
    conn = getDB()
    results = conn.execute(u"select date(created),julianday('2019-06-25') - julianday(created), count(*) from users where ticket <> 'IIIF Showcase - Monday, June 24th' and ticket <> 'Workshop Only - Tuesday, June 25th' group by date(created) order by created;")

    firstDay = "{}".format((date(2019,6,24) - date(2019,4,3)).days)
    daysOutHash = {
        firstDay: {
            "date":"2019-04-03",
            "gottingen": {
                "count": 0
            }
        }
    }
    count = 0
    for result in results:
        created = result[0]
        daysOut = result[1]
        count += result[2]
        daysOutHash[int(daysOut)] = {
            "date":created,
            "daysOut": int(daysOut),
            "gottingen": {
                "count": count
            }
        }
    # now read in other conferences    
    with open('conf/past_events_stats.py') as json_file: 
        pastEvents = json.load(json_file)
        events = []
        count = 0
        for event in pastEvents.keys():
            events.append(event)
            for day in reversed(pastEvents[event]['conference']):
                daysOut = day.keys()[0] 
                count += int(day[daysOut])
                daysOut = int(daysOut.replace('.0',''))
                if daysOut not in daysOutHash:
                    created = u'{}'.format(str((date(2019,6,24) - timedelta(days=daysOut))))
                    daysOutHash[daysOut] = {
                        "date": created,
                        "daysOut": int(daysOut),
                        event: {
                            "count": count
                        }
                    }
                else: 
                    daysOutHash[daysOut][event] = {
                        "count":count
                    }


    data = {}
    data ['cols'] = [
        {'id': 'date', 'label': 'Date', 'type': 'date'},
        {'id': 'count', 'label': 'Gottingen', 'type': 'number'}
    ]    
    i = 1
    for event in events:
        data['cols'].append({'id': 'count_{}'.format(i), 'label': event, 'type': 'number'})
        i += 1

    sortedHash = sorted(daysOutHash.keys())
    i = 0
    for result in sortedHash:
        if 'rows' not in data:
            data['rows'] = []
        splitDate = daysOutHash[result]['date'].split('-')
        row = {
          'c': [
            { 'v':"Date({},{},{})".format(splitDate[0], int(splitDate[1]) - 1, splitDate[2])},
          ]
        }
        if 'gottingen' in daysOutHash[result]:
            row['c'].append({ 'v':daysOutHash[result]["gottingen"]['count']})
        else:
            if len(data['rows']) < 1:
                row['c'].append({ 'v': 0})
            else:    
                if 'gottingen' in daysOutHash[sortedHash[i - 1]]:
                    row['c'].append({ 'v': daysOutHash[sortedHash[i - 1]]['gottingen']['count']})
                else:    
                    row['c'].append({ 'v': 0})
            
        for event in events:
            if event in daysOutHash[result]:
                row['c'].append({ 'v':daysOutHash[result][event]['count']})
            else:
                if event in daysOutHash[sortedHash[i - 1]]:
                    row['c'].append({ 'v': daysOutHash[sortedHash[i - 1]][event]['count']})
                else:    
                    row['c'].append({ 'v': 0})
                    
                
        i += 1
        data['rows'].append(row)    

    response.content_type = 'application/json'
    return json.dumps(data, indent=4)
    #return json.dumps(daysOutHash, indent=4)

@gottingen.route('/gottingen/conference-types.json')
def conferenceAttendeesTypes():
    conn = getDB()
    results = conn.execute("select ticket,count(*) from users where ticket <> 'IIIF Showcase - Monday, June 24th' and ticket <> 'Workshop Only - Tuesday, June 25th' group by ticket;")
    data = {}
    data ['cols'] = [
        {'id': 'ticket', 'label': 'Ticket Type', 'type': 'string'},
        {'id': 'count', 'label': 'Count', 'type': 'number'}
    ]    

    data['rows'] = []
    for result in results:
        data['rows'].append({
          'c': [
            { 'v':result[0]},
            { 'v':result[1]}
          ]
        })

    response.content_type = 'application/json'
    return json.dumps(data, indent=4)

@gottingen.route('/gottingen/attendees.json')
def ticketCounts():
    conn = getDB()
    results = conn.execute("select ticket,count(*) from users group by ticket;")
    data = {}
    for result in results:
        data[result[0]] = result[1]

    response.content_type = 'application/json'
    return json.dumps(data, indent=4)

@gottingen.route('/gottingen/workshop-attendees.json')
def workshopAttendees():
    conn = getDB()
    results = conn.execute('select answer, ticket from users inner join question_link on users.id = question_link.user_id where question_id = "22866012" and ticket <> "IIIF Showcase - Monday, June 24th";')

    tickets = ["Non-IIIF Consortium Member", "IIIF Consortium Member", 'Sponsor Ticket', "Workshop Only - Tuesday, June 25th", "IIIF Staff Ticket","Göttingen Host Ticket"]
    ticketsMapping = {
        "Non-IIIF Consortium Member": 'Non-IIIF Consortium',
        "IIIF Consortium Member": 'Consortium',
        'Sponsor Ticket': 'Sponsor',
        "Workshop Only - Tuesday, June 25th": 'Workshop Only',
        "IIIF Staff Ticket":'Staff Ticket',
        "Göttingen Host Ticket": 'Host Ticket'
    }
    workshopOrder = ["I will not attend any of the workshops", u'Morning - IIIF f\xfcr Einsteiger \u2013 eine deutschsprachige Einf\xfchrung (A German-language introduction to IIIF)', "Morning - Mirador 3 Hands On User Workshop", "Afternoon - Mirador 3 Hands On Technical Workshop", "Afternoon - UV Half Day Showcase and Workshops", u'Afternoon - \u201cFrom Zero to IIIF Hero in 20 min\u201d or \u201cIIIF Delivery and Consumption within the Goobi Community\u201d']
    workshopMapping= {
        "I will not attend any of the workshops": 'None',
        u'Morning - IIIF f\xfcr Einsteiger \u2013 eine deutschsprachige Einf\xfchrung (A German-language introduction to IIIF)': 'Morning - German Lang Introduction', 
        "Morning - Mirador 3 Hands On User Workshop": 'Morning - Mirador Hands on', 
        "Afternoon - Mirador 3 Hands On Technical Workshop": 'Afternoon - Mirador tech', 
        "Afternoon - UV Half Day Showcase and Workshops": 'Afternoon - UV',
        u'Afternoon - \u201cFrom Zero to IIIF Hero in 20 min\u201d or \u201cIIIF Delivery and Consumption within the Goobi Community\u201d': 'Afternoon - Goobi'
    }
    workshops = {}
    for result in results:
        answer = result[0]
        if not answer:
            answer = "None"
        #if 'Zero to IIIF' in answer and answer not in workshopOrder:
         #   workshopOrder.append(answer)
            
        ticket = result[1]

        key = ""
        if '|' in answer:
            for workshop in answer.split('|'):
                workshop = normalize(workshop)
                if workshop not in workshops:
                    workshops[workshop] = {}
                    
                if ticket not in workshops[workshop]:
                    workshops[workshop][ticket] = 0
                workshops[workshop][ticket] += 1    
        else:
            workshop = normalize(answer)
            if workshop not in workshops:
                workshops[workshop] = {}
                    
            if ticket not in workshops[workshop]:
                workshops[workshop][ticket] = 0
            workshops[workshop][ticket] += 1    


    data = {}
    data ['cols'] = [
        {'id': 'workshop', 'label': 'Workshop', 'type': 'string'}
    ]    

    for ticket in tickets:
        data['cols'].append({'id': 'count_{}'.format(tickets.index(ticket)), 'label': ticketsMapping[ticket], 'type': 'number'})

    data['rows'] = []
    for workshop in workshopOrder:
        row = {
            'c': [
                { 'v': workshopMapping[workshop]}
            ]
        }
        for ticket in tickets:
            if workshop not in workshops or ticket not in workshops[workshop]:
                if workshop in workshops:
                    workshops[workshop][ticket] = 0
                else:
                    workshops[workshop] = {}
                    workshops[workshop][ticket] = 0
            row['c'].append({ 'v': workshops[workshop][ticket]})

        data['rows'].append(row)


    return data
    #response.content_type = 'application/json'
    #return json.dumps(data, indent=4)

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


