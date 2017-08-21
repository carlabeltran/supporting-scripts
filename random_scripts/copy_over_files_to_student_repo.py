#!/usr/bin/env python3

import os, shutil, sys

HOMEPATH = os.path.expanduser('~')
STUDENT_REPO_PATH = os.path.join(HOMEPATH, 'projects/trilogy_TA_class/April-2017-Austin-Class-Repository')
LESSONS_REPO_PATH = os.path.join(HOMEPATH, 'projects/trilogy_TA_class/lesson-plans')
LESSONS_CLASS_CONTENT_PATH = os.path.join(LESSONS_REPO_PATH, '01-Class-Content')

ACTIVITIES = '01-Activities'
# input and raw_input are completely different in python2 vs 3, when you give input 'all' in python2, it returns the built in function all()
# error out if the script is ran with python2
if sys.version_info.major == 2:
    raise Exception("This script has to use python3...rerun with `python3 {name}`".format(name=__file__))


"""
run script:
    if an assignment number range isn't given (1 8 for copying from 1 to 8, etc) or the word 'all' or 'none' isnt given:
        raise error message

if first arg isn't "none":
    given a week number, copy over all assignment folders up to a given number, or the word 'all':
        make 01-Assignments in the student folder for that week if needed
        copy each of those folders over to student folder as needed

prompt runner if they want to also upload HW now:
    if yes:
        upload HW instructions (and images if available)


"""

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
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def copy_activity_folder(week, activity_number):
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

    print('folder_name')
    print(folder_name)
    print('this_activity_folder')
    print(this_activity_folder)

    class_repo_week_path = os.path.join(STUDENT_REPO_PATH, this_week_class_content_folder, ACTIVITIES, folder_name)
    make_directory_if_doesnt_exist(class_repo_week_path)

    print('class_repo_week_path')
    print(class_repo_week_path)

    copytree(this_activity_folder, class_repo_week_path)




def copy_all_assignments(week_number):
    pass


# gather_arg("What week are you uploading for?", "week")
# COLLECTED_ARGS['week'] = ensure_two_digit_number_string(COLLECTED_ARGS['week'])
#
# gather_arg("If you want to upload assignments, either enter 'all', 'none', or the assignment number to start from", "assignment_start")
#
# start = COLLECTED_ARGS['assignment_start']
# print(start)

# TODO: revert
start = 'none'

if start == 'none':
    pass
elif start == 'all':
    copy_all_assignments(COLLECTED_ARGS['week'])
else:
    gather_arg("Enter the assignment number to end uploading at:", "assignment_end")
    week, start, end = COLLECTED_ARGS['week'], COLLECTED_ARGS['assignment_start'], COLLECTED_ARGS['assignment_end']
    print(week)
    print(find_matching_class_content_folder(week))
    # print(find_matching_class_content_folder(start))
    # print(find_matching_class_content_folder(end))

COLLECTED_ARGS['week'] = '18'

# print(find_matching_class_content_folder(week))

copy_activity_folder(COLLECTED_ARGS['week'], '04')

# generator = walklevel(LESSONS_CLASS_CONTENT_PATH)
#
# for root, dirs, files in generator:
#     print(root)
#     print(dirs)
#     print(files)


#-------------------------------------------------------------------------------------------------------------------

# tests

result = ensure_two_digit_number_string(5)
assert result == '05'

result = ensure_two_digit_number_string(23)
assert result == '23'
