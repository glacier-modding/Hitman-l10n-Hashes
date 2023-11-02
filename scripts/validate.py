'''
Validates various things that need to be validated, these include:
- LINE collisions [1]
- Strings matching hashes [2]
'''

from crc import Calculator, Crc32
import glob, json, sys

calculator = Calculator(Crc32.CRC32)

# Returns number of LINE collisions
def checkCollisions():
    hashes = {}
    for path in glob.glob("extracted/H1/**/*.LOCR.JSON", recursive=True):
        j = json.load(open(path, "r", encoding="utf-8"))
        for hash, value in j["languages"]["en"].items():
            if hash in hashes and hashes[hash] != value:
                print(f"Collision found! \"{path}\" - {hash} - {value} | {hashes[hash]}")
            else:
                hashes[hash] = value


def checkHashes():
    SOUNDTAGS = json.load(open("soundtags.json", "r"))
    CASES = json.load(open("cases.json", "r"))
    LINES = json.load(open("lines.json", "r"))

    for hash, value in SOUNDTAGS.items():
        if value == None:
            continue

        if hash != f"{calculator.checksum(str.encode(value)):08X}":
            print(f"Soundtag mismatch: \"{hash}\" - \"{value}\"")

    for hash, value in CASES.items():
        if value == None:
            continue

        if hash != f"{calculator.checksum(str.encode(value)):08X}":
            print(f"Case mismatch: \"{hash}\" - \"{value}\"")

    for hash, value in LINES.items():
        if value == None:
            continue

        if hash != f"{calculator.checksum(str.encode(value)):08X}":
            print(f"LINE mismatch: \"{hash}\" - \"{value}\"")

if len(sys.argv) != 2:
    print("Invalid arguments!")
    print("Usage: py validate.py <mode>")
    print("Valid modes: 1 and 2")
    exit(1)

if sys.argv[1] == "1":
    print("Checking for collisions...")
    checkCollisions()
    print("Done!")
elif sys.argv[1] == "2":
    print("Validating hashes...")
    checkHashes()
    print("Done!")
else:
    print("Invalid mode!")
    print("Valid modes: 1 and 2")
