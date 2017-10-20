#!/usr/bin/env python
import os
import random
from faker import Faker

FAKER = Faker()
"""

"""

HOMEPATH = os.path.expanduser('~')

COURSE_PATH = os.path.join(HOMEPATH, 'projects/trilogy/fakeCourseFiles')

WEEK_1 = os.path.join(COURSE_PATH, '01-excel')
WEEK_2 = os.path.join(COURSE_PATH, '02-vba')
WEEK_3 = os.path.join(COURSE_PATH, '03-python')

weeks = [WEEK_1, WEEK_2, WEEK_3]

for week in weeks:
    if not os.path.exists(week):
        os.makedirs(week)

    for i in range(1, 4):
        filepath = os.path.join(week, str(i))
        if not os.path.exists(filepath):
            os.makedirs(filepath)


for root, dirs, files in os.walk(COURSE_PATH):
    for directory in dirs:
        choices = ['1', '2', '3']
        if directory in choices:
            activities_path = os.path.join(root, directory, 'Activities')
            if not os.path.exists(activities_path):
                os.makedirs(activities_path)

            random_activities_count = random.randint(6, 12)
            for i in range(random_activities_count):

                fake_name = FAKER.catch_phrase().replace(' ', '-')

                if i < 10:
                    number = '0' + str(i + 1)
                else:
                    number = str(i + 1)

                filestring = number + '-' + fake_name

                new_activity_path = os.path.join(activities_path, filestring)
                if not os.path.exists(new_activity_path):
                    os.makedirs(new_activity_path)

                random_files_count = random.randint(1, 4)
                for i in range(random_files_count):
                    fake_name = FAKER.catch_phrase().replace(' ', '-').replace('/', '-')
                    new_file_path = os.path.join(new_activity_path, fake_name + '.py')
                    if not os.path.exists(new_file_path):
                        open(new_file_path, 'w').close()
