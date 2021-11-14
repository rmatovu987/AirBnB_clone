#!/usr/bin/python3
"""City Class that inherits from BaseModel"""
from models.base_model import BaseModel


class City(BaseModel):
    """City Class"""

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Commom definition for all models"""
        super().__init__(*args, **kwargs)
        