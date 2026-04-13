# BeatNet
Machine Learning Final Project - AI DJ Classifier/Mixer

# Abstract
This project aims to build a classifier that predicts whether two songs are compatible for a smooth DJ transition. If time permits, we will extend this into a full DJ auto-mixing and recommendation system, potentially incorporating web scraping to gather more recent transition and song data.

To build our dataset we will use the DJ Mix Dataset, which provides labeled sequences of tracks used in real DJ sets, to extract the positive examples (compatible song pairs). Then, the negative examples will be generated from pairs of songs that do not appear together in the DJ Mix dataset, and randomly sampled pairs of tracks not in the data set. Finally, we will extract audio features from the Spotify API for each song pair to form our final data set, which we’ll use to train a model to predict transition compatibility.

We will evaluate our model using a balanced dataset of compatible and non-compatible pairs, measuring performance on a train-test split. Success will be defined as achieving accuracy significantly above a 50% baseline.

# Motivation and Questions

This project will explore machine learning’s capability to understand music and classify musical relationships between songs. The Spotify API provides the necessary features for describing songs. The DJ Mix Dataset provides access to training data regarding relationships between songs, (further data about which could be collected using webscrapers on soundcloud or 1001tracklists.com). Together these datasets will serve as training data in an algorithm that identifies compatible songs based on their features.

Inspiration for BeatNet came from listening to DJ mixes. This experience lends well to testing our model: we have both a subjective intuition regarding song compatibility, as well as an array of DJ mixes not in the training set that can be used to evaluate the model’s performance.

The ultimate motivation behind BeatNet is to further develop AI integration in music generation and recommendation, specifically in the space of AI DJ transition models. AI DJs have the ability to improve listening retention, introduce new music to users, and revolutionize the way we listen to music. Hopefully our model will inform AI DJs and DJs alike in choosing which songs to mix together.

# Planned Deliverables Sebastian
Our primary deliverable will be a Python package that trains a machine learning model for predicting DJ transition compatibility between two songs. The package will include all code for data processing, feature extraction (via the Spotify API), model training, and evaluation, along with clear documentation. Additionally, we will provide at least one Jupyter Notebook demonstrating how to use the package, including exploratory analysis and evaluation of model performance.

# Resources Required
Our target data comes from the DJ Mix Dataset, https://github.com/mir-aidj/djmix-dataset, which provides tracklists of existing DJ mixes. Once we have cleaned the dataset, this source will provide the pairings of songs that have been directly mixed together (pairs of songs where there is a transition from Song 1 -> Song 2). 

Our feature data will come from the Spotify API, which contains songs and their musical features. The final format of our dataset will be rows containing the features of pairings of two songs, along with a single binary label according to whether or not this pairing was found in the DJ Mix Dataset. Negative labels will be generated from random pairs of songs: either songs that were not paired in the DJ Mix Dataset, or randomly generated pairings from the Spotify API.

Concatenating these two datasets will present a couple challenges. First, in order to match Spotify API features with the DJ Mix pairings, we need to have an efficient method of matching song titles. Second, we will have to explore the different two methods of choosing negatively labelled song pairings.

## Partial Success:
At minimum, we will produce a working classifier that takes two songs as input and outputs a binary prediction indicating whether they are compatible for a DJ transition. This will be accompanied by a Jupyter Notebook showcasing the full pipeline, including training, evaluation on a train-test split, and analysis of model accuracy. We will also include qualitative evaluation, such as testing the model on DJ mixes not present in the dataset and incorporating subjective assessments of transition quality. 

## Full Success:
If successful, we will expand the dataset by incorporating additional DJ mix data through web scraping from platforms such as SoundCloud, and 1001Tracklists. We may also explore more advanced approaches, such as using embeddings to model, or even create,  transitions. In this scenario, the system could evolve beyond binary classification to include a recommendation component that suggests compatible songs given a single input track, moving closer to a fully automated DJ mixing assistant. We are also considering including some sort of compatibility scoring, to rank the quality of the compatibility between two songs, which would help with the recommendation system. This might potentially turn the problem into a linear regression model to predict those scores. 

# Resources Required

# What You Will Learn
I, Sebastian, aim to strengthen my skills in data wrangling, feature extraction, and implementation, tuning, and evaluation of machine learning models for specific applications. I am also excited to work with the Spotify API and further develop my ability to analyze and manipulate music data in a programming context.

I, Tyler, intend to improve my partner-coding skills in GitHub (which I have very little experience using), and build my understanding of binary classifier models. This project will also allow me to learn more about how to work with APIs like Spotify, and how to generate useful datasets for machine learning models.

# Risk Statement
One potential challenge is the inherently subjective nature of DJ transitions. Skilled DJs can often make seemingly incompatible songs work well together, which may mean that clear, consistent patterns in the data are weaker than expected or non-existent. Additionally, a binary classifier alone may not be very useful in practice, as users would still need to search through many song pairs manually; this creates a risk that the final system lacks practical usability without an automatic recommendation or mixing component. 

A second major risk is the construction of negative examples. While positive examples come from real DJ mixes, negative examples must be generated artificially, such as by randomly pairing songs or adding pairs not seen in the data. However, these pairs are not guaranteed to be truly incompatible, which may introduce noise into the training data. This could lead the model to learn whether two songs have historically been mixed together rather than whether they are inherently compatible based on their features. 

Additional risks include limitations in the dataset itself. The data is several years old and may not reflect more recent music trends, which could impact the model’s relevance. There is also a possibility of popularity bias, where songs that are more popular appear more frequently in DJ mixes, and are therefore more likely to be labeled as compatible, skewing the model toward well-known tracks

# Ethics Statement
Our binary classifier could help DJs, artists, and music listeners to identify songs for their mixes or listening sessions. Automated DJ systems help to more efficiently produce longer, more engaging song mixups. This alternative to listening to individual songs could improve listening retention and positively change the way we listen to music. DJ mixes can also make new music more accessible to people with a fixed music taste.
The aforementioned benefits DJ mixes could help spread the popularity of less well-known artists if their songs are mixable with more popular playlists.
Our classifier also has the potential to make music production easier for DJs and Artists. If we extend the project to recommend music, a casual listener could use the program for finding songs that work well together in a playlist. DJ mixes present a new way to listen to music, which has the potential to benefit anyone who enjoys listening to music.
Niche genres of music may be labeled as not compatible with other songs in DJ mixes. This bias is a result of there being less existing DJ mixes containing these types of songs. This could negatively impact lesser-known artists or those who listen to nontraditional genres of music.
The opposite issue may also occur: our model may be biased towards identifying popular songs that appear in many DJ mixes as always compatible for DJ mixes.
We hope that our model will make the world a better place by developing the space of DJ music recommendations. However, our model makes several key assumptions. First, we assume that song compatibility is predictable based on features of the individual songs. We assume two songs having been mixed is a close approximation to the true target of two songs being mixable. Finally, we assume that a model identifying mixable songs will assist DJs, artists, and listeners in creating mixes, and that the world is a better place when those mixes are generated more efficiently.
As mentioned before, song popularity in the DJ Mix Dataset may impact how the model assesses its compatibility with new songs.
The dataset contains a limited number of DJ mixes, meaning that culture and genre representation will be biased, and the model is likely to promote the tastes of select DJs.



# Tentative Timeline
We plan to structure our work to ensure a functional prototype early, followed by refinement and expansion.


## First Two Weeks:
We will develop the data acquisition pipeline, including integrating the DJ mix dataset with Spotify API features. By the end of this phase, we aim to have a clean, usable dataset and complete initial exploratory data analysis. 

## Final Two Weeks:
We will implement the binary classification model to predict song compatibility, along with thorough performance evaluation using a train-test split. If time permits, we will explore the extensions we have discussed, such as developing a recommendation component, an AI mixing functionality, or a way to quantify compatibility beyond binary classification. 


