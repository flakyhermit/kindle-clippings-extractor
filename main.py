#!/usr/bin/env python3

import sys
import re
from db import Db

FILEDIR = sys.arg[0]
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
    for result in results:
        clip = {}
        # getting position data
        # TODO: A possible alternative to 'None'
        if result.group('postype') == 'location':
            loc = [result.group('posx'), result.group('posy')]
            page = [None, None]
        elif result.group('postype') == 'page':
            page = [result.group('posx'), result.group('posy')]
            loc = [result.group('locx'), result.group('locy')]
        # extracting timestamp
        timestring = '{weekday} {month} {day} {hour}:{minute}:{second} {year}'
        timestring = timestring.format(weekday=result.group('wday'), \
                                    month=result.group('month'), \
                                    day=result.group('day'), \
                                    hour=result.group('hr'), \
                                    minute=result.group('min'), \
                                    second=result.group('sec'), \
                                    year=result.group('year'))
        clip['author'] = result.group('author')
        clip['title'] = result.group('title')
        clip['type'] = result.group('ctype').lower()
        clip['timestamp'] = timestring
        clip['highlight'] = result.group('highlight')
        clip['page'] = page
        clip['location'] = loc
        clips.append(clip)
        return clips

def db_update(clips):
    db = Db(DBPATH)
    for clip in clips:
        if db.check_if_exists(clip) is False:
            db.insert_clip(clip)

# Main program
# 1. Read source file.
# 2. Check if string empty.
# 3. Check for valid formatting. (How?)
# 4. Parse text, return clips object.
# 5. Update database
#   1. Check if table exists, create table
#   2. Check if clip exists (How?)
