#!/usr/bin/env python

import unittest
import os

from lesson_plans.slacker import Slacker

CWD = os.getcwd()

"""
Tests are not running:

Traceback (most recent call last):
  File "test_slacker.py", line 6, in <module>
    from .slacker import Slacker
ValueError: Attempted relative import in non-package
"""

class SlackerTests(unittest.TestCase):

    def setUp(self):
        self.slacker = Slacker()
        self.fullpath = "/Users/cchilders/projects/trilogy_TA_class/lesson-plans/slacker"

    def test_get_filepath(self):
        filename = "slacker.py"
        # TODO: this should return the full path
        # self.assertEqual(self.slacker.check_if_is_valid_file(filename))
        # TODO: this should return the full path
        # self.assertEqual(self.slacker.check_if_is_valid_file(os.path.join(self.fullpath, filename)))
        self.assertIsNone(self.slacker.check_if_is_valid_file('bad filepath'))



if __name__ == '__main__':
    unittest.main()
