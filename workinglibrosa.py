import os
import re
import djmix as dj
import librosa
import numpy as np
import pandas as pd

DATASET_DIR = os.path.join(os.getcwd(), "djmix_dataset")

# ----------------------------
# FEATURE FUNCTION
# ----------------------------
def extract_features(path):
    y, sr = librosa.load(path)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)

    return {
        "tempo": float(tempo),
        "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
        "spectral_bandwidth": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
        "zero_crossing_rate": np.mean(librosa.feature.zero_crossing_rate(y)),
        **{f"mfcc_{i+1}": mfcc_mean[i] for i in range(len(mfcc_mean))}
    }

# ----------------------------
# PARSE MIX + INDEX FROM FILENAME
# ----------------------------
def parse_filename(filename):
    # expects "0.mp3", "12.mp3", etc.
    match = re.match(r"(\d+)\.mp3", filename)
    return int(match.group(1)) if match else None

# ----------------------------
# GET TITLE FROM DJMIX
# ----------------------------
def get_track_title(mix_idx, track_idx):
    try:
        mix = dj.mixes[mix_idx]
        track = mix.tracklist[track_idx]
        return str(track)
    except:
        return f"unknown_{mix_idx}_{track_idx}"

# ----------------------------
# MAIN LOOP
# ----------------------------
for mix_folder in sorted(os.listdir(DATASET_DIR)):

    mix_path = os.path.join(DATASET_DIR, mix_folder)

    if not os.path.isdir(mix_path):
        continue

    # extract mix index from folder name "mix_0"
    mix_idx = int(mix_folder.split("_")[1])

    print(f"\n=== Processing {mix_folder} ===")

    rows = []

    for file in sorted(os.listdir(mix_path)):

        if not file.endswith(".mp3"):
            continue

        track_idx = parse_filename(file)
        if track_idx is None:
            continue

        file_path = os.path.join(mix_path, file)

        try:
            feats = extract_features(file_path)

            # 🔥 KEY ADDITION: recover real title via DJMix
            title = get_track_title(mix_idx, track_idx)

            feats["title"] = title
            feats["mix"] = mix_idx
            feats["track_index"] = track_idx

            rows.append(feats)

            print(f"✔ {title}")

        except Exception as e:
            print(f"❌ Failed {file}: {e}")

    if len(rows) == 0:
        print(f"⚠️ No features for {mix_folder}")
        continue

    df = pd.DataFrame(rows)

    output_path = os.path.join(DATASET_DIR, f"{mix_folder}_features.csv")
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")