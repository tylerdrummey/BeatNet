'''
Step 1 - Download Songs with DJMix API
'''

import os
import shutil
import djmix as dj

START_MIX = 47
END_MIX = 60

BASE_DIR = os.path.join(os.getcwd(), "djmix_dataset")
TRACKS_DIR = os.path.join(BASE_DIR, "tracks")

dj.set_root(BASE_DIR)

def latest_file(folder, before_set):
    after = set(os.listdir(folder))
    new_files = list(after - before_set)
    if not new_files:
        return None

    return max(
        new_files,
        key=lambda f: os.path.getctime(os.path.join(folder, f))
    )

for mix_idx in range(START_MIX, END_MIX + 1):

    mix = dj.mixes[mix_idx]
    mix_folder = os.path.join(BASE_DIR, f"mix_{mix_idx}")
    os.makedirs(mix_folder, exist_ok=True)

    print(f"\n=== mix_{mix_idx} ===")

    for i, track in enumerate(mix.tracklist):

        try:
            before = set(os.listdir(TRACKS_DIR)) if os.path.exists(TRACKS_DIR) else set()

            track.download()

            new_file = latest_file(TRACKS_DIR, before)

            if new_file is None:
                print(f"❌ No file for index {i}")
                continue

            src = os.path.join(TRACKS_DIR, new_file)

            # 🔥 THIS preserves correct order deterministically
            dst = os.path.join(mix_folder, f"{i}.mp3")

            shutil.move(src, dst)

            print(f"✔ Track {i}")

        except Exception as e:
            print(f"❌ Failed {i}: {e}")

print("\nDone.")