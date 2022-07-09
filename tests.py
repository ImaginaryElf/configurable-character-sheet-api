import pytest
import json

from game import Game

def test_valid_schema():
    with open("tests/fixtures/soulbound.schema.json") as f:
        game = Game({"schema": json.load(f)})
    assert game.validate_schema() == True

def test_invalid_schema():
    game = Game({"schema": ""})
    assert game.validate_schema() == False