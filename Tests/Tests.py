import os
import unittest


class Tests(unittest.TestCase):
    def test_path_separator(self):
        """
        Test valid for windows, mac or linux, gets the default separator for the current OS ('/' or '\')
        """
        print(os.sep)  # Outputs the path separator character
        print(os.path.sep)  # Outputs the same path separator character

        # Check if they are the same
        print(os.sep == os.path.sep)  # Outputs True

        self.assertEqual(os.sep, os.path.sep)
