import os
import unittest


class Tests(unittest.TestCase):
    def test_path_separator(self):
        """
        Test valid for windows, mac or linux, gets the default separator for the current OS ('/' or '\')
        """
        print("\n1) os.sep: " + os.sep)  # Outputs the path separator character
        print(os.sep + 'test1')
        print(str("test2").join(os.sep))  # do not join the string, ignores test2
        print(os.sep.join('test3'))

        print("\n2) os.path.sep: " + os.path.sep)  # Outputs the same path separator character
        print(os.path.sep + 'test4')
        print(os.path.sep.join('test5'))

        print("\n3) os.path.join: ")  # Outputs the same path separator character
        print(os.path.join('test6', 'test7', 'test8'))

        # Check if they are the same
        print("\n4) os.sep == os.path.sep:")
        print(os.sep == os.path.sep)  # Outputs True

        self.assertEqual(os.sep, os.path.sep)
