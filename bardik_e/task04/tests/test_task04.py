import os
import pytest
import json
from io import StringIO

from src.task04.converter import read_items_from_file, filter_items


def test_read_items_attributes():
	output = StringIO()

	with open(os.path.join(os.getcwd(), "references", "items_game.txt"), "rt", encoding="utf-8") as input_file:
		attributes = filter_items(read_items_from_file(input_file), "")
		json.dump(attributes, output, ensure_ascii=False, indent=4, sort_keys=True)

	with open(os.path.join(os.getcwd(), "references", "test_no_filter.json"), "rt", encoding="utf-8") as input_file:
		assert output.getvalue() == input_file.read()


def test_read_items_attributes_filter_weapons():
	output = StringIO()

	with open(os.path.join(os.getcwd(), "references", "items_game.txt"), "rt", encoding="utf-8") as input_file:
		attributes = filter_items(read_items_from_file(input_file), "weapon+_[A-Za-z0-9]+_prefab+")
		json.dump(attributes, output, ensure_ascii=False, indent=4, sort_keys=True)

	with open(os.path.join(os.getcwd(), "references", "test_filter_weapon_prefab.json"), "rt",
			encoding="utf-8") as input_file:
		assert output.getvalue() == input_file.read()
