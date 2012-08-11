#!/usr/bin/env python

import collections
import csv
import datetime
import json
import urllib

from data import DEFAULT_USER, USERNAMES, MILESTONES, STATES, LABELS

#######################################################################
# Configuration. Who doesn't like configuration.
#######################################################################
# Your repository name (the subdirectory we will write data to).
REPO = 'unknown-horizons/'
# Locations of particular files. It is recommended to keep issues
# and comments  in the same directory, which usually is issues/.
ISSUES_PATH = REPO + 'issues/%s.json'
COMMENTS_PATH = REPO + 'issues/%s.comments.json'
MILESTONES_PATH = REPO + 'milestones/%s.json'
# Path to csv-exported comments. We used the following sql (trac 0.12):
# SELECT `ticket`, `time`, `author`, `newvalue` FROM `ticket_change`
# WHERE `field`='comment' AND `newvalue` ORDER BY `time` ASC
CSVFILE = './comments.csv'
# This depends on your database csv export routine.
CSVDELIM = ','
CSVESCAPE ='\''
# Mainly important to get right is this ID. Make sure it has all data
# you need. Trac usually calls the report something along the lines of
# "all tickets by milestone (Including closed)".
REPORT_NO = 6
#
# Magic report id we used to attach special labels to certain tickets
# As all EASY_ stuff, commented out but we used it just like that.
#EASY_NO = 14
#
# A valid url that opens the trac main page.
TRAC_URL = 'http://trac.unknown-horizons.org/t/'
#
# If you use a custom server configuration or an older or more recent
# trac version, you may or may not have to adapt the following lines.
TRAC_TICKET_URL = TRAC_URL + 'ticket/%s'
TRAC_REPORT_URL = TRAC_URL + 'report/%s?asc=1&format=csv' % REPORT_NO
#
#EASY_REPORT_URL = TRAC_URL + 'report/%s?asc=1&format=csv' % EASY_NO
#######################################################################

#######################################################################
# Again, pretty sure this is not necessary for anybody but here we go
#######################################################################
#easy_data = urllib.urlopen(EASY_REPORT_URL)
#reader = csv.DictReader(easy_data)
#easy_tickets = set()
#for row in reader:
#    if row.get('ticket'):
#        easy_tickets.add(row['ticket'])
#######################################################################

def trac_to_gh(text):
    """Right, fun goes here. If you aspire to write magic syntax conversion
    from trac to github flavored markdown, this is your place to be. We just
    replaced basic markup because even getting the links right was a headache.
    """
    t = text.replace('}}}', '```')
    t = t.replace('{{{', '```')
    t = t.replace('[[BR]]', '\n')
    return t or 'Empty!' # No empty issue bodies are supported

def github_label(text):
    """If you do not like the idea of having all your labels converted to
    lower case, now would be a great opportunity to edit one line of code.
    """
    return unicode(text.lower())

def github_time(date):
    """Takes trac date, returns github-ready timestamp. Yes, trac
    for whatever reason may store dates in a highly weird format.
    Only necessary for comments, the tickets are extracted per web
    and thus do not rely on a date representation in trac's db.
    """
    date = int(date) // 1000000
    time = datetime.datetime.fromtimestamp(date)
    return time.strftime('%Y-%m-%dT%H:%M:%S+01:00')

def massage_comment(ticket, date, author, body):
    """Expands the ticket comment list for *ticket* with a json comment
    representation of *date*, *author* (mapped to github) and text *body*.
    """
    body = trac_to_gh(body.decode('utf-8'))

    # Not sure whether we have a related github account for that user.
    if USERNAMES.get(author):
        user = USERNAMES[author]
    else: # If we do not, at least mention the user in our comment body
        user = DEFAULT_USER
        body = 'This comment was posted by **{reporter}**\r\n\r\n'.format(
            reporter=author) + body
    return {
          'body': body,
          'user': user,
          'created_at': github_time(date),
          }

def write_issue(row, outfile):
    """Dumps a csv line *row* from the issue query to *outfile*.
    """
    for key, value in row.items():
        row[key] = row[key].decode('utf-8')
    # Issue text body
    body = row.get('_description', u'')
    body = trac_to_gh(body) + '\r\n\r\n' \
        '[> Link to originally reported Trac ticket <] ({url})'.format(
        url=TRAC_TICKET_URL % row['ticket'])

    # Default state: open (no known resolution)
    state = STATES.get(row.get('status'), 'open')

    # Trac will have stored some kind of username.
    reporter = row['_reporter']

    # Not sure whether we have a related github account for that user.
    if USERNAMES.get(reporter):
        userdata = USERNAMES[reporter]
    else: # If we do not, at least mention the user in our issue body
        userdata = DEFAULT_USER
        body = ('This issue was reported by **%s**\r\n\r\n' % reporter) + body

    # Whether this is stored in 'milestone' or '__group__' depends on the
    # query type. Try to find the data or assign the default milestone 0.
    milestone_info = row.get(('milestone'), row.get('__group__'))
    milestone = MILESTONES.get(milestone_info, 0)

    labels = [] # Collect random tags that might serve as labels
    for tag in ('type', 'component', 'priority'):
        if row.get(tag) and LABELS.get(row[tag]):
            label = LABELS[row[tag]]
            labels.append({'name': github_label(label)})

    # Also attach a special label to our starter tasks.
    # Again, please ignore this.
    #if row['ticket'] in easy_tickets:
    #    labels.append({'name': unicode(LABELS.get('start').lower())})

    # Dates
    updated_at = row.get('modified') or row.get('_changetime')
    created_at = row.get('created') or updated_at

    # Now prepare writing all data into the json files
    dct = {
          'title': row['summary'],
          'body': body,
          'state': state,
          'user': userdata,
          'milestone': {'number': milestone},
          'labels': labels,
          'updated_at': updated_at,
          'created_at': created_at,
       }

    # Assigned user in trac and github account of that assignee
    assigned_trac = row.get('owner')
    assigned = USERNAMES.get(assigned_trac)
    # Assigning really does not make sense without github account
    if state == 'open' and assigned:
        dct['assignee'] = assigned

    # Everything collected, write the json file
    json.dump(dct, outfile, indent=5)

def main():
    #######################################################################
    # Gather information about our tickets (mainly assembles comment list)
    #######################################################################
    # Stores a list of comments for each ticket by ID
    comments = collections.defaultdict(list)
    comment_rows = csv.reader(open(CSVFILE, 'rb'),
                              delimiter=CSVDELIM, quotechar=CSVESCAPE)
    for row in comment_rows:
        try:
            ticket, date, author, body = row
        except: # malformed ticket query, fix in trac or the csv file!
            print '/!\\ Please at check this csv row: /!\\\n', row
            continue
        if not ticket: # nothing we can do if there is no ticket to assign
            continue
        dct = massage_comment(ticket, date, author, body)
        comments[ticket].append(dct) # defaultdict, append always works

    #######################################################################
    # Write the ticket comments to json files indicating their parent issue
    #######################################################################
    for ticket, data in comments.iteritems():
        with open(ISSUES_PATH % ticket, 'w') as f:
            json.dump(data, f, indent=5)

    #######################################################################
    # Write the actual ticket data to separate json files (GitHub API v3)
    #######################################################################
    csv_data = urllib.urlopen(TRAC_REPORT_URL)
    ticket_data = csv.DictReader(csv_data)
    for row in ticket_data:
        if not (row.get('summary') and row.get('ticket')):
            continue
        with open(ISSUES_PATH % row['ticket'], 'w') as f:
            write_issue(row, f)

    #######################################################################
    # Finally, dump all milestones and the related data. This script is not
    # attempting to extract due dates or other data. We just manually mined
    # the milestone names once and stored that in MILESTONES for reference.
    #######################################################################
    for name, id in MILESTONES.iteritems():
        with open(MILESTONES_PATH % id, 'w') as f:
            dct = {
                'number': id,
                'creator': DEFAULT_USER,
                'title': name,
            }
            json.dump(dct, f, indent=5)

    #######################################################################
    # Since trac supports ticket deletion, the following was a quick hack
    # to obtain the IDs of all tickets that no longer exist. We used that
    # list to rename existing GH issues to numbers from this pool.
    # All pull requests have an issue ID attached, so you may have issues
    # in your otherwise empty repository without realizing this!
    # Best check with your awesome github go-to if you are not sure.
    #######################################################################
    #ticketnumbers = csv.reader(open('ticket-ids.csv', 'rb'),
    #                           delimiter=CSVDELIM, quotechar=CSVESCAPE)
    #t_ids = set([int(t[0]) for t in ticketnumbers])
    #available_ids = [i for i in range(1, max(t_ids)) if i not in t_ids]
    #print len(available_ids), max(t_ids) + 1,  sorted(available_ids)
    #######################################################################

if __name__ == '__main__':
    main()
