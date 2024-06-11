"""
validator.py

Author: Liam Nixon
Last modified: 13/05/2024

Validates user input against a list of accepted values
"""


def validate(input_string: str, valid_inputs: [str]) -> bool:
    return input_string in valid_inputs
