import subprocess
import unittest


class SkeletorTestCase(unittest.TestCase):

    def test_skeletor_help(self):
        first_line = subprocess.check_output(["python", "skeletor.py", "--help"]).splitlines()[0].decode('utf-8')
        assert 'usage: skeletor' in first_line, "skeletor --help output's first line contains 'usage: skeletor'"
