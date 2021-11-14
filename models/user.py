#!/usr/bin/python3
"""Class User that inherits from BaseModel"""
from models.base_model import BaseModel


class User(BaseModel):
    """User Class on creation"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
