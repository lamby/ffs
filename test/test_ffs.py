"""
Unittests for the adb.fs module
"""
import datetime
import errno
import os
import tempfile
import unittest

from mock import patch

import ffs

class MkdirPTestCase(unittest.TestCase):

    def test_mkdirs(self):
        "Simple case"
        with patch.object(ffs.os, 'makedirs') as pmkd:
            ffs.mkdir_p('/ihd/lost/pairing')
            pmkd.assert_called_once_with('/ihd/lost/pairing')

    def test_EEXIST(self):
        "Already exists"
        def raiser(*args, **kwargs):
            err = OSError()
            err.errno = errno.EEXIST
            raise err

        with patch.object(ffs.os, 'makedirs') as pmkd:
            pmkd.side_effect = raiser
            ffs.mkdir_p('/ihd/lost/pairing')
            pmkd.assert_called_once_with('/ihd/lost/pairing')

    def test_err(self):
        "Should pass up the err"
        def raiser(*args, **kwargs):
            raise ValueError()

        with patch.object(ffs.os, 'makedirs') as pmkd:
            pmkd.side_effect = raiser
            with self.assertRaises(ValueError):
                ffs.mkdir_p('/ihd/lost/pairing')
                pmkd.assert_called_once_with('/ihd/lost/pairing')


class BaseNTestCase(unittest.TestCase):

    def test_basen(self):
        "Can we split the last n segments of path?"
        cases = [
            ('/foo/bar/car/goo.txt', 2, 'car/goo.txt'),
            ('/foo/bar/car/goo.txt', 1, 'goo.txt'),
            ('/foo/bar/car/goo.txt', 3, 'bar/car/goo.txt'),
            ]
        for path, num, expected in cases:
            based = ffs.basen(path, num=num)
            self.assertEqual(expected, based)

class LsmtimeTestCase(unittest.TestCase):

    def test_lessthan(self):
        "Files modified less than... "
        mtimes = [456, 789, 123]
        def mtimer(path):
            return mtimes.pop()

        def walker(self):
            yield ['/foo/bar/', [], ['baz.txt', 'caz.txt', 'daz.txt']]

        with patch.object(ffs.os, 'walk') as pwalk:
            pwalk.side_effect = walker

            with patch.object(ffs.os.path, 'getmtime') as ptime:
                ptime.side_effect = mtimer

                lessthan = ffs.lsmtime('/foo/bar', datetime.datetime(1970, 1, 1, 0, 3))

                expected = ['/foo/bar/baz.txt']

                self.assertEqual(expected, lessthan)

class RmTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_(self):
        """ """
        pass

    def tearDown(self):
        pass

class SizeTestCase(unittest.TestCase):

    def test_hsize(self):
        """ Get the hex size of a file """
        with tempfile.NamedTemporaryFile(delete=False) as ebl:
            ebl.write("Hello Beautiful World!\n")
            ebl.close()
            self.assertEqual('0x17', ffs.hsize(ebl.name))

    def test_hsize_nofile(self):
        """ Don't Error if the file doesn't exist """
        filepath = 'shouldnt_exist.file'
        self.assertTrue(not os.path.exists(filepath))
        self.assertEqual(None, ffs.hsize(filepath))

class IsExeTestCase(unittest.TestCase):

    def test_is_exe(self):
        """ Is a known file executable? """
        if ffs.OS == "WINDOWS!":
            path = os.path.abspath('/Windows/system32/notepad.exe')
            self.assertEqual(True, ffs.is_exe(path))
        else:
            self.assertEqual(True, ffs.is_exe('/bin/bash'))



if __name__ == '__main__':
    unittest.main()
