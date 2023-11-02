'''
Packages the separate hash lists into a HMLanguages "Packaged Hashlist" (HMLA)
Find more information on the format here: https://tonytools.win/libraries/hmlanguages#hash-list-format
'''

from crc import Calculator, Crc32
from struct import pack
import json, sys

if len(sys.argv) != 2:
    print("Invalid arguments! Requires a version argument.")
    exit(1)

version = 0
try:
    version = int(sys.argv[1])
except ValueError:
    print("Could not parse version to int!")
    exit(1)

print("Packing hash lists...")

calculator = Calculator(Crc32.CRC32, True)

SOUNDTAGS = json.load(open("soundtags.json", "r"))
CASES = json.load(open("cases.json", "r"))
LINES = json.load(open("lines.json", "r"))

def write_section(dict):
    data = bytearray()
    data += pack('I', sum(x is not None for x in dict.values()))

    for hash, value in dict.items():
        if value is None:
            continue

        data += pack('I', int(hash, 16))
        data += value.encode()
        data += '\x00'.encode()

    return data

file = open("hash_list.hmla", "wb")

# Write magic and version
file.write("HMLA".encode())
file.write(pack('I', version))

# Construct the binary data
data = bytearray()

data += write_section(SOUNDTAGS)
data += write_section(CASES)
data += write_section(LINES)

# Add checksum and write
file.write(pack('I', calculator.checksum(data)))
file.write(data)

print("Done!")
