
library(dplyr)
library(stringr)
library(tidyr)
library(fuzzyjoin)


#Clean function to normalize strings
clean <- function(x) {
  x %>%
    tolower() %>%
    str_remove_all("\\[.*?\\]") %>%
    str_remove_all("\\(.*?\\)") %>%
    str_replace_all("[^a-z ]", " ") %>%
    str_squish()
}



#SONG PAIRS DATA WITH EXTRA COLUMNS AND NOT NOMRALIZED SONG NAMES
all = read.csv("all_mix_pairs.csv")

#Extracting postive pairs, normalizing song names, ignoring unused columns, and de-duplicating
positive_pairs = read.csv("all_mix_pairs.csv")|>
  mutate(s1 = clean(str_extract(song1_title,  "(?<=title=['\"]).*?(?=['\"])")))|>
  mutate(s2 = clean(str_extract(song2_title,  "(?<=title=['\"]).*?(?=['\"])")))|>
  mutate(
    s_min = pmin(s1, s2),
    s_max = pmax(s1, s2)
  ) |>
  distinct(s_min, s_max, .keep_all = TRUE)|>
  mutate(compatible=TRUE)|>
  select(-c(s_min, s_max, song1_index, song2_index, mix, song1_title, song2_title ))|>
  rename(
    mfcc_a_1 = mfcc_1_1,
    mfcc_b_1 = mfcc_2_1,
    mfcc_c_1 = mfcc_3_1,
    mfcc_d_1 = mfcc_4_1,
    mfcc_e_1 = mfcc_5_1,
    mfcc_f_1 = mfcc_6_1,
    mfcc_g_1 = mfcc_7_1,
    mfcc_h_1 = mfcc_8_1,
    mfcc_i_1 = mfcc_9_1,
    mfcc_j_1 = mfcc_10_1,
    mfcc_k_1 = mfcc_11_1,
    mfcc_l_1 = mfcc_12_1,
    mfcc_m_1 = mfcc_13_1,
    
    mfcc_a_2 = mfcc_1_2,
    mfcc_b_2 = mfcc_2_2,
    mfcc_c_2 = mfcc_3_2,
    mfcc_d_2 = mfcc_4_2,
    mfcc_e_2 = mfcc_5_2,
    mfcc_f_2 = mfcc_6_2,
    mfcc_g_2 = mfcc_7_2,
    mfcc_h_2 = mfcc_8_2,
    mfcc_i_2 = mfcc_9_2,
    mfcc_j_2 = mfcc_10_2,
    mfcc_k_2 = mfcc_11_2,
    mfcc_l_2 = mfcc_12_2,
    mfcc_m_2 = mfcc_13_2
  )


#Extracting individual sings and their features
song_features_1 <- positive_pairs |>
  select(s1, ends_with("_1")) |>
  rename_with(~ sub("_1$", "", .x), ends_with("_1")) |>
  rename(song = s1)

song_features_2 <- positive_pairs |>
  select(s2, ends_with("_2")) |>
  rename_with(~ sub("_2$", "", .x), ends_with("_2")) |>
  rename(song = s2)


song_features <- bind_rows(song_features_1, song_features_2) |>
  group_by(song) |>
  summarise(across(where(is.numeric), mean, na.rm = TRUE), .groups = "drop")|>
  mutate(song_id = row_number())


write.csv(song_features, "song_features.csv")


#Sampling negative songs 
unique <- unique(c(positive_pairs$s1, positive_pairs$s2))

set.seed(42)
negative_pairs <- tibble(
  s1 = sample(unique, 4000, replace = TRUE),
  s2 = sample(unique, 4000, replace = TRUE)
) |>
  filter(s1 != s2)|>
  distinct(s1, s2) |>
  anti_join(positive_pairs, by = c("s1", "s2"))|>
  head(nrow(positive_pairs))|>
  left_join(song_features, by = c("s1" = "song")) |>
  rename_with(~ paste0(.x, "_1"), -c(s1, s2)) |>
  
  left_join(song_features, by = c("s2" = "song")) |>
  rename_with(~ paste0(.x, "_2"), -c(s1, s2, ends_with("_1")))|>
  mutate(compatible = FALSE)|>
  mutate(
    s_min = pmin(s1, s2),
    s_max = pmax(s1, s2)
  ) |>
  distinct(s_min, s_max, .keep_all = TRUE)|>
  select(-c(s_min, s_max))

#Checking for no duplicates
setdiff(names(positive_pairs), names(negative_pairs))
setdiff(names(negative_pairs), names(positive_pairs))

#Binding to final dataset
negative_pairs <- negative_pairs %>%
  select(names(positive_pairs))
final_pairs <- bind_rows(positive_pairs, negative_pairs)

#Writing final data
write.csv(final_pairs, "final_pairs.csv")
  
write.csv(song_features, "song_featuress.csv")

  


final_pairs = read.csv("final_pairs.csv")
song_features = read.csv("song_featuress.csv")

colnames(final_pairs)



