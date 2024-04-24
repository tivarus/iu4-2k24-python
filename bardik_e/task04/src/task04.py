import argparse
import os
import json

from task04.converter import read_items_from_file, filter_items


def main():
	parser = argparse.ArgumentParser(description="Item Game to JSON files converter.")
	parser.add_argument("path", type=str, nargs=1, help="Path to convertible file.")
	parser.add_argument("--output", type=str, default="", help="Path to output file.")
	parser.add_argument("--regex", type=str, default="", help="Regex that the items in output file must match.")
	args = parser.parse_args()

	source_path = args.path[0]
	output_path = args.output if args.output else "output.json"
	regex = args.regex

	if not os.path.isfile(source_path):
		parser.error("file with provided path does not exist.")

	try:
		with open(source_path, "rt") as input_file:
			try:
				with open(output_path, "wt") as output_file:
					attributes = filter_items(read_items_from_file(input_file), regex)
					json.dump(attributes, output_file, ensure_ascii=False, indent=4, sort_keys=True)

			except PermissionError:
				parser.error(f"cannot open file {output_path} for writing")

	except PermissionError:
		parser.error(f"cannot open file {source_path} for reading")


if __name__ == '__main__':
	main()
