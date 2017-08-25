#!/usr/bin/env python3

import os, shutil, sys

HOMEPATH = os.path.expanduser('~')
STUDENT_REPO_PATH = os.path.join(HOMEPATH, 'projects/trilogy_TA_class/April-2017-Austin-Class-Repository')
LESSONS_REPO_PATH = os.path.join(HOMEPATH, 'projects/trilogy_TA_class/lesson-plans')
LESSONS_CLASS_CONTENT_PATH = os.path.join(LESSONS_REPO_PATH, '01-Class-Content')

ACTIVITIES = '01-Activities'
HOMEWORK = '02-Homework'

# input and raw_input are completely different in python2 vs 3, when you give input 'all' in python2, it returns the built in function all()
# error out if the script is ran with python2
if sys.version_info.major == 2:
    raise Exception("This script has to use python3...rerun with `python3 {name}`".format(name=__file__))

COLLECTED_ARGS = {}

def gather_arg(question, arg_key):
    question = question + '\n'
    result = input(question)
    COLLECTED_ARGS[arg_key] = result

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def make_directory_if_doesnt_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_subdirectories(path):
    """ gets the directories immediately below the path """
    return next(os.walk(path))[1]

def ensure_two_digit_number_string(week):
    week_int = int(week)
    if week_int < 10:
        return '0' + str(week_int)
    else:
        return str(week_int)

def find_matching_class_content_folder(week):
    subdirectories = get_subdirectories(LESSONS_CLASS_CONTENT_PATH)
    for d in subdirectories:
        if d.startswith(week):
            return d

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
        except:
            # print("This directory already exists: %s" % d)
            pass

def get_available_activities(week):
    this_week_class_content_folder = find_matching_class_content_folder(week)
    activities_folder = os.path.join(LESSONS_CLASS_CONTENT_PATH, this_week_class_content_folder, ACTIVITIES)
    activities_subdirectories = get_subdirectories(activities_folder)
    return activities_subdirectories

def copy_activity_folder(week, activity_name):
    this_week_class_content_folder = find_matching_class_content_folder(week)
    if not this_week_class_content_folder:
        raise Exception("Couldn't find that class_content_folder")
    activities_folder = os.path.join(LESSONS_CLASS_CONTENT_PATH, this_week_class_content_folder, ACTIVITIES)
    this_activity_folder = os.path.join(activities_folder, activity_name)
    class_repo_week_path = os.path.join(STUDENT_REPO_PATH, this_week_class_content_folder, ACTIVITIES, activity_name)
    make_directory_if_doesnt_exist(class_repo_week_path)
    copytree(this_activity_folder, class_repo_week_path)

def copy_activity_by_number(week, activity_number):
    activity_number_string = ensure_two_digit_number_string(activity_number)
    this_week_class_content_folder = find_matching_class_content_folder(week)
    if not this_week_class_content_folder:
        raise Exception("Couldn't find that class_content_folder")

    activities_folder = os.path.join(LESSONS_CLASS_CONTENT_PATH, this_week_class_content_folder, ACTIVITIES)
    activities_subdirectories = get_subdirectories(activities_folder)
    try:
        folder_name = [folder for folder in activities_subdirectories if folder.startswith(activity_number_string)][0]
        this_activity_folder = os.path.join(activities_folder, folder_name)
    except:
        raise Exception("Couldn't find that activity folder: %s" % (activities_folder + '/' + week + '-...'))

    class_repo_week_path = os.path.join(STUDENT_REPO_PATH, this_week_class_content_folder, ACTIVITIES, folder_name)
    make_directory_if_doesnt_exist(class_repo_week_path)
    copytree(this_activity_folder, class_repo_week_path)

def copy_all_assignments(week):
    activities_subdirectories = get_available_activities(week)
    for name in activities_subdirectories:
        copy_activity_folder(week, name)

def copy_homework(week):
    this_week_class_content_folder = find_matching_class_content_folder(week)
    this_week_homework_instructions_folder = os.path.join(LESSONS_CLASS_CONTENT_PATH, this_week_class_content_folder, HOMEWORK, 'Instructions')
    class_repo_homework_path = os.path.join(STUDENT_REPO_PATH, this_week_class_content_folder, HOMEWORK)
    make_directory_if_doesnt_exist(class_repo_homework_path)
    copytree(this_week_homework_instructions_folder, class_repo_homework_path)


gather_arg("What week are you uploading for?", "week")
if not COLLECTED_ARGS['week']:
    raise Exception("Please enter a week")
week = ensure_two_digit_number_string(COLLECTED_ARGS['week'])

activities_subdirectories = get_available_activities(week)
print("\nAvailable activities:")
for activity in activities_subdirectories:
    print("    %s" % activity)
print("\n")

gather_arg("Enter an activity number to upload from, 'all' for all activities this week, or leave blank to not upload activities", "assignment_start")

start = COLLECTED_ARGS['assignment_start']

if not start:
    pass
elif start == 'all':
    copy_all_assignments(week)
else:
    gather_arg("Enter the assignment number to end uploading at:", "assignment_end")
    end = int(COLLECTED_ARGS['assignment_end'])
    for i in range(start, end + 1):
        copy_activity_by_number(week, i)


gather_arg("Do you want to copy HW for this week? ('y' or 'yes' for yes; leave blank for 'no')", "hw_boolean")
if COLLECTED_ARGS['hw_boolean'].lower().startswith('y'):
    copy_homework(week)



#-------------------------------------------------------------------------------------------------------------------

# tests

result = ensure_two_digit_number_string(5)
assert result == '05'

result = ensure_two_digit_number_string(23)
assert result == '23'
