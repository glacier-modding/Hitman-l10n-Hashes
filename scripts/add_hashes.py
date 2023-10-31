'''
Adds hashes (put as new lines in a text file) to their lists.

Text file example:
--- Start of File
DIALOGUE_BADDSG_DELUXETANG
DIALOGUE_BADDSG_47STARTRACCOON
--- End of File

Usage:
py add_hashes.py <type> <path to file>

Valid types are: cases, lines, and soundtags
'''

from crc import Calculator, Crc32
import json, sys, os

calculator = Calculator(Crc32.CRC32)

# Adds values to the file specified, returns how many were added.
def addValuesToFile(path, values):
    j = json.load(open(path, "r"))

    count = 0
    for value in values:
        hash = f"{calculator.checksum(str.encode(value)):08X}"
        if hash in j and j[hash] == None:
            j[hash] = value
            count += 1

    json.dump(j, open(path, "w"), sort_keys=True, indent=4)

    return count

if len(sys.argv) != 3:
    print("Invalid arguments!")
    print("Usage: py add_hashes.py <type> <path to file>")
    print("Valid types: cases, lines, and soundtags")
    exit(1)

if not os.path.exists(sys.argv[2]):
    print("File path provided does not exist.")
    exit(1)

newValues = open(sys.argv[2], "r").read().strip().splitlines()

type = sys.argv[1].lower()
if type not in ["cases", "lines", "soundtags"]:
    print("Invalid type!")
    print("Valid types: cases, lines, and soundtags")
    exit(1)

found = addValuesToFile(f"../{type}.json", newValues)
print(f"{found} new hashes added!")
