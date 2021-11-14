#!/usr/bin/python3
"""Unittest for FileStorage"""

import models
from models.engine.file_storage import FileStorage
import os
import unittest


class TestFile_Storage(unittest.TestCase):
    """class TestFile_Storage """

    def test_docstring(self):
        """ function test_docstring """
        msj = "Module doesnt have docstring"
        obj = models.engine.file_storage.__doc__
        self.assertIsNotNone(obj, msj)
        msj = "Classes doesnt have docstring"
        self.assertIsNotNone(obj, msj)

    def test_executable_file(self):
        """ function test_executable_file """
        is_read_true = os.access("models/engine/file_storage.py", os.R_OK)
        self.assertTrue(is_read_true)
        is_write_true = os.access("models/engine/file_storage.py", os.W_OK)
        self.assertTrue(is_write_true)
        is_exec_true = os.access("models/engine/file_storage.py", os.X_OK)
        self.assertTrue(is_exec_true)

    def test_is_an_instance(self):
        """ function test_is_an_instance """
        my_model = FileStorage()
        self.assertIsInstance(my_model, FileStorage)

if __name__ == '__main__':
    unittest.main()
