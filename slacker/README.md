# Purpose

A command line tool to swiftly slack instructions for in-class work to students directly to a slack channel

## Install

ensure your Slacker token is set in your ~/.bash_profile exactly like so:

```
export SLACK_TOKEN="xoxo-your-token-abcdefg"
```

To be able to run Slacker from anywhere on your machine, I recommend configuring it also in ~/.bash_profile:

```
export slacker="/Users/username/projects/trilogy_TA_class/lesson-plans/slacker/slacker.py"
```

Now you can call it from anywhere on your machine like:

```
slacker -m "Please compute this homework by Saturday" -f "Homework/lesson-1"
```

## Usage

`slacker` represents the full path to slacker.py

You can also run it like

```
python /path/to/slacker.py filepath -m "Hello"
```

or if you're in the same directory as slacker.py, just

```
./slacker.py filepath -m "Hello"
```

## Selecting a channel

Slacker defaults to the `main_student_channel` set in `def __init__(self, main_student_channel="default-channel"):`

You can select a specific channel per each usage by giving the `-c` flag as follows:

```
slacker "Hey guys, use this new channel to discuss JBJ" -c jon-bon-jovi
```

#### Send file(s)

The `slacker.py` program takes full or relative paths to send files to slack.

It also takes multiple filenames

```
slacker /some/absolute/filepath.txt
```

or

```
slacker relative/filepath.txt /another/absolute/filepath.txt [more files...]
```

#### Send a directory (Slacker will zip it up)

```
slacker /some/absolute/directory
```

or

```
slacker relative/directory-path /another/file/here.txt
```

#### Send a message

```
slacker "your message"
```

Ex:

```
slacker "Hey guys, check out https://www.youtube.com/watch?v=s8MDNFaGfT4 if you like sandwiches"
```

#### Send a file(s) (or directory(s)) and a message

You can send files with and messages as position args, where each file or message is sent to slack in the order it was given:

```
slacker directory_path "your message" another_file "another message"
```

Remember that Slacker takes absolute or relative filepaths.

Exs:

```
slacker some/relative/lesson/file.pdf "Read this to learn CSS"
```

```
slacker Activities/1.2/Solutions/Activity-1/ "here are the solution files for activity 1" /home/username/lesson-plans/Activities/1.2/Solutions/README.md
```

You can also use the normal flags, -m for message and -f for file, in additional to the -c flag for channel

Exs:

```
slacker /some/absolute/homework/directory -m "Hey guys, do your homework"
```

```
slacker -f lesson.txt -m "See this awesome lesson"
```

```
slacker -m "Use these images im your project" -f Activities/lesson-2/Images -c project-ideas
```


## Automated Slacker Overview

Reads slackerfile.yml in each class content folder like:

```
/02-lesson-plans/01-html-css-three-days/1-Class-Content/1.2/slackerfile.yml
```

Set the `self.current_lesson_number` each day before use

With that set and a valid slackerfile in the right place, now you can query using -o for 'options':

```
slacker -o

5- send github account instructions
9- send repo creation PDF
```

Learn yaml:

<http://docs.ansible.com/ansible/YAMLSyntax.html>
<http://symfony.com/doc/current/components/yaml/yaml_format.html>

## Adding new commands to a slackerfile.yml

Commands are added in json format

Command number should correspond to the class section number. For example, if the instruction in the lesson plan are like "9. Instructor Do: Slack GitHub Guide (2 mins)", the first slacker command would be "9" to correspond with this step in the lesson plan.


## Plumbing

Uses <https://github.com/candrholdings/slack-cli> to send messages

Sending files is broken through slack-cli
The maintainers are not serious about the repo

Sending files:

<https://api.slack.com/methods/files.upload>
