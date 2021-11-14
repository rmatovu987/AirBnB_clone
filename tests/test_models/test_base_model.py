#!/usr/bin/python3
"""Unittest for BaseModel"""

import unittest
from datetime import datetime
from uuid import uuid4

from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test subclass creation"""

    def test_attributes(self):
        """Attributes testing in different cases"""
        inst_1 = BaseModel()
        inst_2 = BaseModel()
        # test if id is string
        self.assertIsInstance(inst_1.id, str)
        # test not equal id
        self.assertNotEqual(inst_1.id, inst_2.id)
        # test if created_at is datetime
        self.assertIsInstance(inst_1.created_at, datetime)
        # test if update_at is datetime
        self.assertIsInstance(inst_1.updated_at, datetime)

    def test_save0(self):
        """Save method testing"""
        inst_1 = BaseModel()
        # test updated_at before and after save()
        first_updated_at = inst_1.updated_at
        inst_1.save()
        second_updated_at = inst_1.updated_at
        self.assertNotEqual(first_updated_at, second_updated_at)
        # test the type of updated_at after save()
        self.assertIsInstance(inst_1.updated_at, datetime)

    def test_save1(self):
        """save method testing"""
        my_base23 = BaseModel()
        my_base23.save()
        my_base23id = "BaseModel." + my_base23.id
        with open("file.json", "r") as f:
            self.assertIn(my_base23id, f.read())

    def test_to_dict(self):
        """to_dict method testing"""
        inst_1 = BaseModel()
        dict_1 = inst_1.to_dict()
        # Test dict type
        self.assertIsInstance(dict_1, dict)
        # test if dictionary updates automatically
        inst_1.save()
        dict_2 = inst_1.to_dict()
        self.assertNotEqual(dict_1["updated_at"], dict_2["updated_at"])

    def test_str(self):
        """__str__ method testing"""
        s = "[BaseModel] ({}) {}"
        my_base25 = BaseModel()
        my_base25printed = my_base25.__str__()
        self.assertEqual(my_base25printed,
                         s.format(my_base25.id, my_base25.__dict__))


if __name__ == '__main__':
    unittest.main()
