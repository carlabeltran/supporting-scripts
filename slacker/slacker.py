#!/usr/bin/env python

import argparse
from copy import copy
import os
import re
import sys
import yaml
import zipfile

from subprocess import Popen, PIPE

HOME = os.path.expanduser('~')
CWD = os.getcwd() # the path from which this script was invoked

LESSON_PLANS_PROJECT_REPO="{home}/projects/trilogy_TA_class/lesson-plans".format(home=HOME)
# DEFAULT_CHANNEL = "general"
DEFAULT_CHANNEL = "t-th-instructions"
# DEFAULT_CHANNEL = "m-w-instructions"
# DEFAULT_CHANNEL = "api-testing"


def determine_if_is_filepath(possible_filepath):
    if os.path.exists(possible_filepath):
        return True
    fullpath = os.path.join(CWD, possible_filepath)
    if os.path.exists(fullpath):
        return True
    return False

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


class Slacker(object):
    def __init__(self, main_student_channel=DEFAULT_CHANNEL):
        self.token = os.environ.get("SLACK_TOKEN")
        self.main_student_channel = main_student_channel
        self.current_lesson_number = "1.2"

    def run_command(self, command_number, lesson_number=None):
        """ given the data for a command, run it """
        data = self.load_slackerfile()
        containing_path = self.find_slackerfile_path(lesson_number)
        try:
            command_data = data[str(command_number)]
        except:
            try: command_data = data[float(command_number)]
            except: raise Exception("Could not find command {}".format(command_number))

        if 'filepath' in command_data.keys():
            command_data['filepath'] = os.path.join(containing_path, command_data['filepath'])
            self.send_file(**command_data)
        else:
            self.send_message(**command_data)

    def get_full_current_commands_info(self, lesson_number=None):
        """ returns all info about commands, such as files and messages """
        # TODO
        # slackerfile = self.get_exact_slackerfile_path(lesson_number)
        pass

    def get_current_commands_info(self, lesson_number=None):
        commands_info = ["Current commands info:"]
        data = self.load_slackerfile(lesson_number)
        commands = data.keys()
        sorted_commands = self.natural_sort(commands)
        try:
            for command in sorted_commands:
                dataset = data[command]
                commands_info.append(command + ": " + dataset['description'])
            return "\n\n".join(commands_info)
        except:
            return None

    def load_slackerfile(self, lesson_number=None):
        slackerfile_path = self.get_exact_slackerfile_path(lesson_number)
        data = self.load_from_yaml(slackerfile_path)
        # rewrites slackerfile to ensure that each key is a string.
        # We can also try lookups by float/int if str fails.
        # I felt this is easier. one problem is it rewrites the slackerfiles, which may confuse people

        """rewriting the yaml causes strange problems..."""
        # try:
        #     for key, value in data.items():
        #         data[str(key)] = value
        #     self.dump_to_yaml(slackerfile_path, data)
        #     return data
        # except:
        #     return None
        return data

    def get_exact_slackerfile_path(self, lesson_number=None):
        containing_path = self.find_slackerfile_path(lesson_number)
        return os.path.join(containing_path, 'slackerfile.yaml')

    def find_slackerfile_path(self, lesson_number=None):
        """ takes a number like 1.2, and searches through your
        lesson-plans repo to find that lesson's slackerfile """
        if not lesson_number:
            lesson_number = self.current_lesson_number
        lesson_plan_path = os.path.join(LESSON_PLANS_PROJECT_REPO, '02-lesson-plans')
        module_number = self.get_module_number_from_current_lesson_number(lesson_number)
        for root, dirs, files in os.walk(lesson_plan_path, topdown=True):
            for directory in dirs:
                this_module_number = self.get_module_number_from_lesson_path(directory)
                if this_module_number == module_number:
                    possible_root = os.path.join(root, directory, '1-Class-Content', lesson_number)
                    slackerfile_path_should_be = os.path.join(possible_root, 'slackerfile.yaml')
                    if os.path.exists(slackerfile_path_should_be):
                        return possible_root
                    else:
                        return None

    def natural_sort(self, the_list):
        """ takes
            [4, '11a', '23', '5', 'hw', 'assignment'] --> [4, '5', '11a', '23', 'assignment', 'hw']
        """
        final_list = []
        last_spot = len(the_list) - 1
        for i, item in enumerate(the_list):
            if i == last_spot:
                return the_list
            next_item = the_list[i + 1]
            comparison = self.natural_compare(item, next_item)
            if comparison == item:
                final_list.append(item)
            else:
                final_list.append(next_item)
                final_list.append(item)
                final_list.extend(the_list[i+2:])
                return self.natural_sort(final_list)

    def natural_compare(self, a, b):
        """ returns which item is first """
        a_as_string = str(a).lower()
        b_as_string = str(b).lower()
        starting_number_rgx = r"^[0-9.]+"
        number_match_a = re.search(starting_number_rgx, a_as_string)
        number_match_b = re.search(starting_number_rgx, b_as_string)
        if number_match_a and not number_match_b:
            return a
        elif number_match_b and not number_match_a:
            return b
        elif not number_match_a and not number_match_b:
            return a if a_as_string < b_as_string else b
        else:
            # handle number matches like 4 vs '22.3a'
            number_a = float(number_match_a.group())
            number_b = float(number_match_b.group())
            if number_a < number_b:
                return a
            elif number_b < number_a:
                return b
            else:
                remainder_a = copy(a_as_string).lstrip(number_a)
                remainder_b = copy(b_as_string).lstrip(number_b)
                if remainder_a < remainder_b:
                    return a
                elif remainder_b < remainder_a:
                    return b
                else:
                    return a # if both items are completely equal, just returns one of em

    def get_module_number_from_lesson_path(self, relative_path):
        """ give me '07-firebase' and get back '7' """
        rgx = "^\d{2}"
        try: return re.search(rgx, relative_path).group().lstrip('0')
        except: raise Exception("Could not find a lesson number from path '{0}'".format(relative_path))

    def get_module_number_from_current_lesson_number(self, current_lesson_number=None):
        """ give me '07-firebase' and get back '7' """
        if not current_lesson_number:
            current_lesson_number = self.current_lesson_number
        rgx = "^\d{1,2}"
        try: return re.search(rgx, current_lesson_number).group()
        except: raise Exception("Could not find a module number from current_lesson '{0}'".format(current_lesson))

    def send_file(self, filepath, message="", channel=None, **kwargs):
        print(filepath)
        if not channel:
            channel = self.main_student_channel
        if os.path.isdir(filepath):
            filepath = self.zip_up_directory(filepath)

        print('filepath:')
        print(filepath)

        command = """
            curl -F file=@{filepath} -F channels={channel} -F token={token} \
             -F initial_comment="{message}" \
             https://slack.com/api/files.upload
        """.format(filepath=filepath, channel=channel, token=self.token, message=message)
        call_sp(command)
        print(command)

    def send_message(self, message="", channel=None, **kwargs):
        if not channel:
            channel = self.main_student_channel

        if not message:
            raise Exception("Enter a message to send")

        command = """slackcli -h {channel} -m "{message}" """.format(channel=channel, message=message)
        call_sp(command)

    def zip_up_directory(self, filepath):
        """ if the file to send is actually several files, zip them up to /tmp before sending """
        # TODO: use below article to add compression
        # http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory/
        # https://pymotw.com/2/zipfile/
        filepath = filepath.rstrip('/')
        root, basename = os.path.split(filepath)
        if 'solved' in basename.lower() or 'unsolved' in basename.lower():
            renamed_filepath = root + '--' + basename
        zip_path = os.path.join('/tmp', renamed_filepath + '.zip')

        def zipdir(path, ziphandler):
            """ path is what you want to zip up, ziph is how to zip it up """
            for root, dirs, files in os.walk(path):
                for f in files:
                    thispath = os.path.join(root, f)
                    ziphandler.write(thispath)

        zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        zipdir(filepath, zipf)
        zipf.close()
        return zip_path

    def get_filepath(self, string):
        # firstly, should return a relative path if possible to make it easier to zip files
        # if not, the zipfile the students get will have a pointlessly long page like:
        #   /Users/cchilders/projects/trilogy_TA_class/lesson-plans/1.2/Activities/Images/
        # instead of just
        #  Images/
        if os.path.exists(string):
            return string

        fullpath = os.path.join(CWD, string)
        if os.path.exists(fullpath):
            return fullpath

        return None

    def load_from_yaml(self, filepath):
        if not filepath:
            return None
        with open(filepath, 'r') as stream:
            data = yaml.load(stream)
            return data

    def dump_to_yaml(self, filepath, data):
        with open(filepath, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)


if __name__ == '__main__':
    slacker = Slacker()

    # test natural_compare
    one = slacker.natural_compare(4, '11.2a')
    assert one == 4
    two = slacker.natural_compare('23', '11.2a')
    assert two == '11.2a'
    three = slacker.natural_compare('a', 'b')
    assert three == 'a'
    four = slacker.natural_compare('d', 'b')
    assert four == 'b'
    five = slacker.natural_compare(4, 'a')
    assert five == 4
    six = slacker.natural_compare('a', 6.4)
    assert six == 6.4

    # test natural_sort
    sorted_list = slacker.natural_sort([4, '11a', '23', '5', 'hw', 'assignment'])
    assert sorted_list == [4, '5', '11a', '23', 'assignment', 'hw']

    # commands_info = slacker.get_current_commands_info()
    # assert commands_info == '9: Send the Github help PDF\n\n11: explain instructions for blah blah\n\nhw: Their HW for this week'

    parser = argparse.ArgumentParser()
    parser.add_argument('positional', nargs='*', default='', help='filepath OR message OR filepath message')
    parser.add_argument('-m', required=False, help='The message to send', default='')
    parser.add_argument('-f', required=False, help='The file(s) to send', default='')
    parser.add_argument('-c', required=False, help='The channel to send it to', default='')
    parser.add_argument('-o', required=False, action='store_true', help='The current options of commands to use')
    parser.add_argument('-a', required=False, action='store_true', help='The full description of current commands to use [as in (a)ll info]')
    args = parser.parse_args()

    message = args.m
    filepath = args.f
    channel = args.c
    options_flag = args.o
    full_description_options_flag = args.a

    if options_flag and full_description_options_flag:
        raise Exception("\nIf you want to know the current options, please pick one of -o (brief description) and -a (all info)")

    def check_for_args(args):
        chars = ""
        try: chars = "".join(args.positional)
        except: chars = ""
        for attr in ['m', 'f', 'c']:
            chars += getattr(args, attr)
        return bool(chars)

    there_is_args = check_for_args(args)

    if full_description_options_flag:
        print(slacker.get_full_current_commands_info())
        sys.exit()

    if not there_is_args or options_flag:
        print(slacker.get_current_commands_info())
        sys.exit()

    if args.positional:
        length = len(args.positional)
        if length == 1:
            the_arg = args.positional[0]
            current_commands = slacker.get_current_commands_info()
            if current_commands:
                commands_as_strings = [str(c) for c in current_commands]
                if str(the_arg) in commands_as_strings:
                    slacker.run_command(the_arg)
                    sys.exit()

        for arg in args.positional:
            if determine_if_is_filepath(arg):
                slacker.send_file(filepath=arg, channel=channel)
            else:
                slacker.send_message(message=arg, channel=channel)

    if message and filepath:
        slacker.send_file(filepath=filepath, message=message, channel=channel)
    elif message:
        slacker.send_message(message=message, channel=channel)
    elif filepath:
        slacker.send_file(filepath=filepath, channel=channel)
