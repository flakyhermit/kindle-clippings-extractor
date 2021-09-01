#!/usr/bin/env python3

import sys
import re
import time
from db import Db

FILENAME = "My Clippings.txt"
EXPORTPATH = './out'
DBPATH = './clippings.db'

def read_source_file(filepath):
    """Read the clippings file and return as string."""
    try:
        file = open(filepath, 'r', encoding = 'utf-8')
    except FileNotFoundError:
        return None
    clips_str = file.read()
    return clips_str

def parse(text):
    """Use regex to extract info from clippings text."""
    p = re.compile(r"^(?P<title>[\S ]+) \((?P<author>[\S ]+)\)\n" \
                "- Your (?P<ctype>Highlight|Note|Bookmark) " \
                "(on|at) (?P<postype>location|page) " \
                "(?P<posx>\d+)(-?(?P<posy>\d+))?" \
                "( \| location (?P<locx>\d+)(-?(?P<locy>\d+))?)? \| " \
                # Getting the timestamp
                "Added on (?P<wday>[a-zA-Z]{3})[a-zA-Z]{,3}day, " \
                "(?P<day>\d{1,2}) (?P<month>[a-zA-Z]{3})[a-zA-Z]* " \
                "(?P<year>\d{4}) (?P<hr>\d\d):(?P<min>\d\d):(?P<sec>\d\d)\n\n" \
                "(?P<highlight>[\S ]+)\n==========", re.MULTILINE)
    results = p.finditer(text)
    clips = []
    for result in results:
        clip = {}
        # getting position data
        if result.group('postype') == 'page':
            loc = result.group('locx')
            page = result.group('posx')
        else:
            loc = result.group('posx')
            page = None
        # extracting timestamp
        def month_to_number (string):
            month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', \
                          'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            return month_list.index(string) + 1
        timestring = '{year}-{month}-{day} {hour}:{minute}:{second}'
        timestring = timestring.format(weekday=result.group('wday'), \
                                    month=month_to_number(result.group('month')), \
                                    day=result.group('day'), \
                                    hour=result.group('hr'), \
                                    minute=result.group('min'), \
                                    second=result.group('sec'), \
                                    year=result.group('year'))
        time_s = time.strptime(timestring, '%Y-%m-%d %H:%M:%S')
        timestamp = time.strftime('%s', time_s)
        # Convert timestring to unix millis
        clip['author'] = result.group('author')
        clip['title'] = result.group('title')
        clip['type'] = result.group('ctype').lower()
        clip['timestamp'] = timestamp
        clip['highlight'] = result.group('highlight')
        clip['page'] = page
        clip['location'] = loc
        clips.append(clip)
    return clips


def db_update(clips):
    db = Db(DBPATH)
    for clip in clips:
        book_id = db.get_book_id(clip['title'], clip['author'])
        if book_id is None:
            book_id = db.insert_book(clip['title'], clip['author'])
        clip_tuple = (
            clip['location'],
            clip['page'],
            clip['type'],
            clip['timestamp'],
            clip['highlight'],
            "",
            str(book_id)
        )
        db.insert_clip(clip_tuple)

# Main program
# 1. Read source file.
# 2. Check if string empty.
# 3. Check for valid formatting. (How?)
# 4. Parse text, return clips object.
# 5. Update database
#   1. Check if table exists, create table
#   2. Check if clip exists (How?)
#   3. If not, check if book exists, if not, add, get the book id
#   4. Add clip
#   5. Close db.

# Read the source file
with open(FILENAME, 'r', encoding='utf-8') as file:
    clips_str = file.read()

if clips_str:
    clips = parse(clips_str)
    db_update(clips)

