import os, subprocess, shutil

# Get runtime dirs from environment
H1_RUNTIME = os.environ.get("H1_RUNTIME")
H2_RUNTIME = os.environ.get("H2_RUNTIME")
H3_RUNTIME = os.environ.get("H3_RUNTIME")

VERSIONS = ["HM2016", "HM2", "HM3"]

extracted = False

def call_rpkg(type, runtime, output_path, version):
    subprocess.call(f"rpkg-cli -extract_{type}_to_json_from \"{runtime}\" -output_path \"{output_path}\" -version {version}")

def delete_dirs(dir, allowed):
    dirs = next(os.walk(dir))[1]
    delete = [dir for dir in dirs if dir not in allowed]
    
    for folder in delete:
        shutil.rmtree(f"{dir}/{folder}")

def extract_files(version, runtime):
    global extracted
    extracted = True

    output_path = f"../extracted/H{version}"

    print(f"Extracting LOCR for H{version}...")
    call_rpkg("locr", runtime, output_path, VERSIONS[version - 1])

    print(f"Extracting DLGE for H{version}...")
    call_rpkg("dlge", runtime, output_path, VERSIONS[version - 1])

    print(f"Cleaning up files from H{version}...")

    # This deletes any files extracted from modded RPKGs
    to_keep = []
    if version == 1:
        size = os.path.getsize(f"{runtime}/chunk0.rpkg") / 1024 / 1024 / 1024
        if size > 20:
            # This is Epic/GOG, only keep chunk0
            to_keep = ["chunk0.rpkg"]
        else:
            # This is Steam, keep base and patch1
            to_keep = ["chunk0.rpkg", "chunk0patch1.rpkg"]
            for c in range(7):
                to_keep.append(f"dlc{c}.rpkg")
                to_keep.append(f"dlc{c}patch1.rpkg")
    elif version == 2:
        # In H2, there are 21 chunks (chunk0 + dlc0-19)
        for C in range(21):
            prefix = "dlc" if C != 0 else "chunk"
            c = 0 if C == 0 else C - 1 # Handles chunk0
            patch_level = (0 if c == 7 else (4 if c < 14 else 2)) + 1 # chunk14+ only have 2 patches, dlc7 has none

            to_keep.append(f"{prefix}{c}.rpkg")
            for p in range(1, patch_level):
                to_keep.append(f"{prefix}{c}patch{p}.rpkg")
    elif version == 3:
        # In H3, there are 30 chunks (0-29)
        for c in range(30):
            # Chunk 28 and 29 only have 1 patch
            patch_level = (4 if c < 28 else 1) + 1
            to_keep.append(f"chunk{c}.rpkg")
            for p in range(1, patch_level):
                to_keep.append(f"chunk{c}patch{p}.rpkg")

    delete_dirs(f"{output_path}/LOCR", to_keep)
    delete_dirs(f"{output_path}/DLGE", to_keep)

    print(f"Done extracting files from H{version}!")

if H1_RUNTIME:
    extract_files(1, H1_RUNTIME)

if H2_RUNTIME:
    extract_files(2, H2_RUNTIME)

if H3_RUNTIME:
    extract_files(3, H3_RUNTIME)

if extracted:
    print("Finished extracting files!")
else:
    print("Did not extract any files. Ensure environment variables are set.")
