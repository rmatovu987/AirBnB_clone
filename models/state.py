#!/usr/bin/python3
"""State Class that inherits BaseModel"""
from models.base_model import BaseModel


class State(BaseModel):
    """State Class"""
    name = ""

    def __init__(self, *args, **kwargs):
        """Commom definition for all models"""
        super().__init__(*args, **kwargs)
        