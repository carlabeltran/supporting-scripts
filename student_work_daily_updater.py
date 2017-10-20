#!/usr/bin/env python
import os
from subprocess import Popen, PIPE

"""
set settings for course files path, and mywork path

cd into course files folder:
    git pull
    [check if git pull worked, if not, offer a solution]

for each week:
    for each day:
        for everything in 'Activities':
            copy them to my work
"""

HOMEPATH = os.path.expanduser('~')

COURSE_PATH = os.path.join(HOMEPATH, 'projects/trilogy/fakeCourseFiles')
MYWORK_PATH = os.path.join(HOMEPATH, 'projects/trilogy/mywork')

if not os.path.exists(MYWORK_PATH):
    os.makedirs(MYWORK_PATH)

def call_sp(command, *args, **kwargs):
    if args:
        command = command.format(*args)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    output, err = p.communicate()
    print('\nOutput:\n')
    print(output.decode('utf-8'))
    print('\n\nErr:\n')
    print(err.decode('utf-8'))
    return output, err


call_sp('git pull', **{'cwd': COURSE_PATH})

"""
for each week available:
    for each day available:
        make the same folder in mywork, with an Activities folder inside

for each activity in that:
    copy it to mywork
