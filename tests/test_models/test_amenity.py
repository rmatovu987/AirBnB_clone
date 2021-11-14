#!/bin/usr/python3
"""Test Amenity"""

import unittest
from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Test Amenity"""

    def test_class(self):
        """Test class"""
        self.assertEqual(Amenity.name, "")
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_instance(self):
        """Test instance"""
        my_amenity = Amenity()
        self.assertEqual(my_amenity.name, "")
        self.assertTrue(isinstance(my_amenity, BaseModel))
