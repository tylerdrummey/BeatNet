import pandas as pd

df = pd.read_json("data.json")

tracks = df[["id", "tracklist"]].explode("tracklist").reset_index(drop=True)

tracks_norm = pd.json_normalize(tracks["tracklist"])

tracks = pd.concat(
    [tracks.drop(columns=["tracklist"]), tracks_norm],
    axis=1
)

tracks.to_csv("data.csv", index=False)