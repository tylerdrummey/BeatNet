
library(dplyr)
library(stringr)
library(tidyr)
library(fuzzyjoin)

# df = read.csv("data.csv")
# 
# 
# df <- df %>%
#   mutate(track_name  = song1 <- str_remove_all(title, "\\[.*?\\]"))
# 
# 
# pairs <- df %>%
#   group_by(id) %>%
#   mutate(
#     song1 = track_name,
#     song2 = lead(track_name)
#   ) %>%
#   filter(!is.na(song2)) %>%
#   ungroup()|>
#   mutate(compatibility = TRUE)|>
#   select(song1, song2, compatibility)
# 
# 
# pairs <- pairs %>%
#   separate(song1, into = c("artist_name1", "track_name1"), sep = " - ", extra = "merge") %>%
#   separate(song2, into = c("artist_name2", "track_name2"), sep = " - ", extra = "merge")

# pairs <- pairs %>%
#   mutate(
#     artist_track_1 = clean(paste(artist_name1, track_name1)),
#     artist_track_2 = clean(paste(artist_name2, track_name2))
#   )


# n = 5000
# a1 = audio_data[1:n, ]
# #a2 = audio_data[(n+1):nrow(audio_data), ]
# 
# pairs_1 <- stringdist_left_join(
#   unmatched,
#   a1,
#   by = c("song" = "audio_key"),
#   method = "jw",        # Jaro-Winkler
#   max_dist = 0.10,      
#   distance_col = "dist1"
# )|>
#   filter(!is.na(key))

clean <- function(x) {
  x %>%
    tolower() %>%
    str_remove_all("\\[.*?\\]") %>%
    str_remove_all("\\(.*?\\)") %>%
    str_replace_all("[^a-z0-9 ]", " ") %>%
    str_squish()
}

pairs = read.csv("pairs.csv")

audio_data = read.csv("SpotifyAudioFeaturesApril2019.csv")|>
  select(-track_id)|>
  mutate(
    audio_key = clean(paste(artist_name, track_name))
  )


pairs_features <- pairs %>%
  left_join(audio_data, by = c("song_key1" = "audio_key")) %>%
  left_join(audio_data, by = c("song_key2" = "audio_key"), suffix = c("_1", "_2"))
  

write.csv(pairs_features, "pairs_features.csv")

unique_songs <- data.frame(
  song = unique(c(pairs$song_key1, pairs$song_key2)),
  stringsAsFactors = FALSE
)

match_table <- data.frame(
  song = character(),
  audio_key = character(),
  stringsAsFactors = FALSE
)

exact <- exact <- unique_songs %>%
  left_join(audio_data, by = c("song" = "audio_key")) %>%
  filter(!is.na(key))|>
  mutate(audio_key = song) %>%   # enforce identity mapping
  select(song, audio_key)|>
  distinct(song, audio_key)
  

match_table <- bind_rows(match_table, exact)%>%
  distinct(song, .keep_all = TRUE)
  


songs_remaining <- unique_songs

songs_remaining = songs_remaining %>%
  anti_join(match_table, by = "song")
# -----------------------------
# 1. LOOP: match songs
# -----------------------------
step = 500
current = 12001 


repeat {
  cat("Remaining songs:", nrow(songs_remaining), "\n")
  
  if (nrow(songs_remaining) == 0) break
    
  # -------------------------
  # B. FUZZY MATCH (ONLY UNMATCHED)
  # -------------------------
  fuzzy <- stringdist_left_join(
    songs_remaining,
    audio_data[current-step:current,],
    by = c("song" = "audio_key"),
    method = "jw",
    max_dist = 0.10
  ) %>%
    filter(!is.na(audio_key)) %>%
    select(song, audio_key)
  current = current + step
  
  if (current >= nrow(audio_data)) break
  
  cat("matched", nrow(fuzzy),"Current:", current, "\n")
  
  # add fuzzy matches
  match_table <- bind_rows(match_table, fuzzy) %>%
    distinct(song, .keep_all = TRUE)
  
  # update remaining again
  songs_remaining <- songs_remaining %>%
    anti_join(match_table, by = "song")
}

# -----------------------------
# 2. FINAL CLEANUP
# -----------------------------

match_table <- match_table %>%
  distinct(song, .keep_all = TRUE)

write.csv(match_table, "match_table.csv")

  





