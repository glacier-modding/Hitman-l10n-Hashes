'''
Adds lines from the REPO.

Usage:
py add_lines_from_repo.py <path to repo file>
'''

from crc import Calculator, Crc32
import json, sys, os

calculator = Calculator(Crc32.CRC32)

if len(sys.argv) != 2:
    print("Invalid arguments!")
    print("Usage: py add_lines_from_repo.py <path to repo file>")
    exit(1)

if not os.path.exists(sys.argv[1]):
    print("File path provided does not exist.")
    exit(1)

lines = set()
props = ["Name", "Name_LOC", "Description", "Description_LOC"]
for entry in json.load(open(sys.argv[1], "r", encoding="utf-8")):
    for prop in props:
        if prop in entry:
            lines.add(entry[prop].upper())

j = json.load(open("./lines.json", "r"))

count = 0
for line in lines:
    hash = f"{calculator.checksum(str.encode(line)):08X}"
    if hash in j and j[hash] == None:
        j[hash] = line
        count += 1

json.dump(j, open("./lines.json", "w"), sort_keys=True, indent=4)

print(f"{count} new hashes added!")
