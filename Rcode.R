
library(dplyr)
library(stringr)
library(tidyr)
library(fuzzyjoin)

df = read.csv("data.csv")


df <- df %>%
  mutate(track_name  = song1 <- str_remove_all(title, "\\[.*?\\]"))


pairs <- df %>%
  group_by(id) %>%
  mutate(
    song1 = track_name,
    song2 = lead(track_name)
  ) %>%
  filter(!is.na(song2)) %>%
  ungroup()|>
  mutate(compatibility = TRUE)|>
  select(song1, song2, compatibility)


pairs <- pairs %>%
  separate(song1, into = c("artist_name1", "track_name1"), sep = " - ", extra = "merge") %>%
  separate(song2, into = c("artist_name2", "track_name2"), sep = " - ", extra = "merge")
  

audio_data = read.csv("SpotifyAudioFeaturesApril2019.csv")|>
  select(-track_id)

audio_data = audio_data[1:10000,]

clean <- function(x) {
  x %>%
    tolower() %>%
    str_remove_all("\\[.*?\\]") %>%
    str_remove_all("\\(.*?\\)") %>%
    str_replace_all("[^a-z0-9 ]", " ") %>%
    str_squish()
}

pairs <- pairs %>%
  mutate(
    artist_track_1 = clean(paste(artist_name1, track_name1)),
    artist_track_2 = clean(paste(artist_name2, track_name2))
  )

audio_data <- audio_data %>%
  mutate(
    audio_key = clean(paste(artist_name, track_name))
  )

pairs_full <- stringdist_left_join(
  pairs,
  audio_data,
  by = c("artist_track_1" = "audio_key"),
  method = "jw",        # Jaro-Winkler (good for names)
  max_dist = 0.15,      
  distance_col = "dist1"
)|>
  filter(!is.na(key)) #only leave rows that matched
  
  
  


write.csv(pairs, "pairs.csv", row.names = FALSE)

