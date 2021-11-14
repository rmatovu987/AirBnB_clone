#!/usr/bin/python3
"""Class Amenity that inherits BaseModel"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity Class"""

    name = ""

    def __init__(self, *args, **kwargs):
        """Commom definition for all models"""
        super().__init__(*args, **kwargs)
        