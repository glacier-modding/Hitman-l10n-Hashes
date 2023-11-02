'''
Generates statistics for the various hash lists and places them into the README.
'''

import json

SOUNDTAGS = json.load(open("soundtags.json", "r"))
CASES = json.load(open("cases.json", "r"))
LINES = json.load(open("lines.json", "r"))

# From glacier-modding/Hitman-Hashes
def generate_badge_url(label, value, colour):
    label = label.replace(" ", "%20")
    return f"https://img.shields.io/badge/{label}-{value}-{colour}.svg"

# From glacier-modding/Hitman-Hashes
def total_completion_colour(percentage):
    if percentage >= 90:
        return "green"
    elif 70 <= percentage < 90:
        return "yellow"
    else:
        return "red"

# From glacier-modding/Hitman-Hashes
def add_to_readme(start_marker, end_marker, addition_str):
    with open("README.md", "r") as f:
        content = f.read()

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index != -1 and end_index != -1:
        before_section = content[:start_index + len(start_marker)]
        after_section = content[end_index:]
        content = before_section + "\n" + addition_str + after_section

    with open("README.md", "w", newline="\n") as f:
        f.write(content)

def generate_badge(obj, name):
    completed = 0
    for value in obj.values():
        if value != None:
            completed += 1

    completion = (completed / len(obj)) * 100

    return f"![{name} Completion - {completion:.2f}%]({generate_badge_url(name, f'{completion:.2f}%25', total_completion_colour(completion))})"

badges = [
    generate_badge(SOUNDTAGS, "Soundtag"),
    generate_badge(CASES, "Case"),
    generate_badge(LINES, "LINE")
]

add_to_readme("<!-- BADGES_START -->", "<!-- BADGES_END -->", "\n".join(badges) + "\n")
