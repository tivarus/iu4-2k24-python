from collections.abc import Iterator
import shlex
import re


def read_items_from_file(source: Iterator) -> dict:
	"""
	Read items attributes from iterable object.
	:param source: iterator to source collection or file.
	:return: dictionary, that describes items attributes. Keys are item names and values are dictionaries containing
	items attributes.
	"""

	result = dict()
	is_attributes_section = False
	braces_count = 0  # difference between opening and closing curly braces
	stack = list()  # stack, that contains item names
	attributes_section_tokens = list()  # tokens of current attribute section

	try:
		strip_line = next(source).strip()
		lexer = shlex.split(strip_line)

		while True:
			if lexer[0] == "attributes":
				is_attributes_section = True
				braces_count = 0
				attributes_section_tokens.clear()

			elif lexer[0] == "prefab":
				if lexer[1] in result.keys():  # if the item has parent with attributes, merge the attributes
					if stack[-1] in result.keys():
						# if prefab described after attributes section, need to merge attributes correctly
						result[stack[-1]] = merge_attributes(result[lexer[1]], result[stack[-1]])
					else:
						result[stack[-1]] = result[lexer[1]]

			else:
				if is_attributes_section:
					if braces_count != 0:  # if there are tokens from attribute section
						attributes_section_tokens.extend(lexer)  # insert them into list for further parsing

					if lexer[0] == "{":
						braces_count += 1

					elif lexer[0] == "}":
						braces_count -= 1

						if braces_count == 0:
							# when read equal count of opening and closing braces
							# insert the attributes into result dict
							if stack[-1] in result.keys():
								# if the item has parent with attributes, merge the attributes
								result[stack[-1]] = merge_attributes(result[stack[-1]],
									read_attributes_section(attributes_section_tokens))
							else:
								# otherwise, just consider only item's attributes
								result[stack[-1]] = read_attributes_section(attributes_section_tokens)

							is_attributes_section = False

				else:
					next_line = next(source).strip()
					lexer = shlex.split(next_line)

					if lexer[0] == "{":
						# if the line not in attributes section, check is next line containing opening curly brace
						# if true, this line contains name of item
						# push it to stack
						stack.append(strip_line[1:-1])
					elif lexer[0] == "}":
						# if next line is closing the section, pop the last name from stack
						stack.pop()

					strip_line = next_line
					continue

			strip_line = next(source).strip()
			lexer = shlex.split(strip_line)

	except StopIteration:
		pass

	return result.copy()


def read_attributes_section(section_text_tokens: list[str]) -> dict:
	"""
	Read attributes from list with attributes section tokens.
	:param section_text_tokens: list with attributes section tokens.
	:return: dict with keys are attributes names and values are attributes values.
	"""
	result = dict()

	subsection_start_idx = 0
	braces_count = 0

	for idx in range(len(section_text_tokens)):
		if section_text_tokens[idx] == "{":
			if not braces_count:  # if this is the start of nested attribute section
				subsection_start_idx = idx + 1

			braces_count += 1

		elif section_text_tokens[idx] == "}":
			braces_count -= 1

			if not braces_count:  # if this is the end of nested attribute section
				# recursively read the attributes from nested section
				result[section_text_tokens[subsection_start_idx - 2]] = (
					read_attributes_section(section_text_tokens[subsection_start_idx:idx]))
				subsection_start_idx = 0

		else:
			# tokens on even position are attribute names
			# tokens on odd position are attribute values
			if not braces_count and (idx % 2 != 0):
				result[section_text_tokens[idx - 1]] = section_text_tokens[idx]

	return result.copy()


def merge_attributes(parent_attributes: dict, child_attributes: dict) -> dict:
	result = dict()
	keys = parent_attributes.keys() | child_attributes.keys()

	for key in keys:
		if key in child_attributes:
			if key in parent_attributes:
				if isinstance(parent_attributes[key], str):
					result[key] = child_attributes[key]
				elif isinstance(parent_attributes[key], dict):
					result[key] = merge_attributes(parent_attributes[key], child_attributes[key])
			else:
				result[key] = child_attributes[key]
		else:
			result[key] = parent_attributes[key]

	return result.copy()


def filter_items(items_attributes: dict, regex: str) -> dict:
	"""
	Filter items from dictionary with provided regex.
	:param items_attributes: dictionary with items and their attributes.
	:param regex: regular expression to match dictionary keys.
	:return: filtered dictionary.
	"""
	result = dict()
	pattern = re.compile(regex)

	for key in items_attributes:
		if pattern.match(key):
			result[key] = items_attributes[key].copy()

	return result.copy()
