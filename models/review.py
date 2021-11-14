#!/usr/bin/python3
"""Review Class that inherits BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review Class"""

    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        """Commom definition for all models"""
        super().__init__(*args, **kwargs)
        