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

def test_valid_layout():
    with open("tests/fixtures/soulbound.layout.json") as f:
        game = Game({"layout": json.load(f)})
    assert game.validate_layout() == True

def test_invalid_schema():
    game = Game({"layout": {}})
    assert game.validate_layout() == False

def test_valid_character():
    with open("tests/fixtures/soulbound.schema.json") as f:
        game = Game({"schema": json.load(f)})
    with open("tests/fixtures/soulbound.example_character.json") as f:
        character = json.load(f)
    assert game.validate_character(character) == True

def test_invalid_character():
    with open("tests/fixtures/soulbound.schema.json") as f:
        game = Game({"schema": json.load(f)})
    character = {}
    assert game.validate_character(character) == False