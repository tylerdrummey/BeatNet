'''
Extract Features from Single mp3 file
'''
import librosa
import numpy as np

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

print("Extracting features from single mp3 file...")
features = extract_features("UsedMP3s/mix_40/0.mp3")
print(features)
