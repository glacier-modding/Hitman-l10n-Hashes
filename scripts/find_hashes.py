'''
Finds hashes from DLGE and LOCR files located in "extracted"
It will automatically add them to the pre-existing JSON files found
at the root of the repo.
'''

import glob, json

SOUNDTAGS = json.load(open("soundtags.json", "r"))
CASES = json.load(open("cases.json", "r"))
LINES = json.load(open("lines.json", "r"))

# DLGE
NEW_SOUNDTAGS = []
NEW_CASES = []

def processCases(cases):
    for case in cases:
        if case not in CASES and case not in NEW_CASES:
            NEW_CASES.append(case)

def processContainer(container):
    type = container["type"]
    if type == "WavFile":
        soundtag = container["soundtag"]
        if soundtag not in SOUNDTAGS and soundtag not in NEW_SOUNDTAGS:
            NEW_SOUNDTAGS.append(soundtag)

        if "cases" in container:
            processCases(container["cases"])
    elif type == "Random":
        for cont in container["containers"]:
            processContainer(cont)

        if "cases" in container:
            processCases(container["cases"])
    elif type == "Switch":
        # Quick little hack
        processCases([container["switchKey"], container["default"]])

        for cont in container["containers"]:
            processContainer(cont)
    elif type == "Sequence":
        for cont in container["containers"]:
            processContainer(cont)


print("Processing DLGE...")
for path in glob.glob("extracted/**/*.DLGE.JSON", recursive=True):
    j = json.load(open(path, "r", encoding="utf-8"))
    processContainer(j["rootContainer"])

print(f"Found {len(NEW_SOUNDTAGS)} new soundtag hashes.")
for soundtag in NEW_SOUNDTAGS:
    SOUNDTAGS[soundtag] = None

print(f"Found {len(NEW_CASES)} new switch hashes.")
for case in NEW_CASES:
    CASES[case] = None

# LOCR
NEW_LINES = []

print("Processing LOCR...")
for path in glob.glob("extracted/**/*.LOCR.JSON", recursive=True):
    j = json.load(open(path, "r", encoding="utf-8"))
    for lang, entries in j["languages"].items():
        for hash in entries.keys():
            if hash not in LINES and hash not in NEW_LINES:
                NEW_LINES.append(hash)

print(f"Found {len(NEW_LINES):,} new line hashes.")
for line in NEW_LINES:
    LINES[line] = None

json.dump(SOUNDTAGS, open("soundtags.json", "w"), sort_keys=True, indent=4)
json.dump(CASES, open("cases.json", "w"), sort_keys=True, indent=4)
json.dump(LINES, open("lines.json", "w"), sort_keys=True, indent=4)
