# BeatNet
Machine Learning Final Project - AI DJ Classifier/Mixer

Test

Test # 2

Test # 3

# Abstract
This project aims to build a classifier that predicts whether two songs are compatible for a smooth DJ transition. If time permits, we will extend this into a full DJ auto-mixing and recommendation system, potentially incorporating web scraping to gather more recent transition and song data.

To build our dataset we will use the DJ Mix Dataset, which provides labeled sequences of tracks used in real DJ sets, to extract the positive examples (compatible song pairs). Then, the negative examples will be generated from pairs of songs that do not appear together in the DJ Mix dataset, and randomly sampled pairs of tracks not in the data set. Finally, we will extract audio features from the Spotify API for each song pair to form our final data set, which we’ll use to train a model to predict transition compatibility.

We will evaluate our model using a balanced dataset of compatible and non-compatible pairs, measuring performance on a train-test split. Success will be defined as achieving accuracy significantly above a 50% baseline.

# Motivation and Questions





# Planned Deliverables Sebastian
Our primary deliverable will be a Python package that trains a machine learning model for predicting DJ transition compatibility between two songs. The package will include all code for data processing, feature extraction (via the Spotify API), model training, and evaluation, along with clear documentation. Additionally, we will provide at least one Jupyter Notebook demonstrating how to use the package, including exploratory analysis and evaluation of model performance.

## Partial Success:
    At minimum, we will produce a working classifier that takes two songs as input and outputs a binary prediction indicating whether they are compatible for a DJ transition. This will be accompanied by a Jupyter Notebook showcasing the full pipeline, including training, evaluation on a train-test split, and analysis of model accuracy. We will also include qualitative evaluation, such as testing the model on DJ mixes not present in the dataset and incorporating subjective assessments of transition quality. 

## Full Success:
    If successful, we will expand the dataset by incorporating additional DJ mix data through web scraping from platforms such as SoundCloud, and 1001Tracklists. We may also explore more advanced approaches, such as using embeddings to model, or even create,  transitions. In this scenario, the system could evolve beyond binary classification to include a recommendation component that suggests compatible songs given a single input track, moving closer to a fully automated DJ mixing assistant. We are also considering including some sort of compatibility scoring, to rank the quality of the compatibility between two songs, which would help with the recommendation system. This might potentially turn the problem into a linear regression model to predict those scores. 

# Resources Required

# What You Will Learn
I, Sebastian, aim to strengthen my skills in data wrangling, feature extraction, and implementation, tuning, and evaluation of machine learning models for specific applications. I am also excited to work with the Spotify API and further develop my ability to analyze and manipulate music data in a programming context.

# Risk Statement
One potential challenge is the inherently subjective nature of DJ transitions. Skilled DJs can often make seemingly incompatible songs work well together, which may mean that clear, consistent patterns in the data are weaker than expected or non-existent. Additionally, a binary classifier alone may not be very useful in practice, as users would still need to search through many song pairs manually; this creates a risk that the final system lacks practical usability without an automatic recommendation or mixing component. 

A second major risk is the construction of negative examples. While positive examples come from real DJ mixes, negative examples must be generated artificially, such as by randomly pairing songs or adding pairs not seen in the data. However, these pairs are not guaranteed to be truly incompatible, which may introduce noise into the training data. This could lead the model to learn whether two songs have historically been mixed together rather than whether they are inherently compatible based on their features. 

Additional risks include limitations in the dataset itself. The data is several years old and may not reflect more recent music trends, which could impact the model’s relevance. There is also a possibility of popularity bias, where songs that are more popular appear more frequently in DJ mixes, and are therefore more likely to be labeled as compatible, skewing the model toward well-known tracks

# Ethics Statement



# Tentative Timeline
We plan to structure our work to ensure a functional prototype early, followed by refinement and expansion.


## First Two Weeks:
    We will develop the data acquisition pipeline, including integrating the DJ mix dataset with Spotify API features. By the end of this phase, we aim to have a clean, usable dataset and complete initial exploratory data analysis. 

## Final Two Weeks:
    We will implement the binary classification model to predict song compatibility, along with thorough performance evaluation using a train-test split. If time permits, we will explore the extensions we have discussed, such as developing a recommendation component, an AI mixing functionality, or a way to quantify compatibility beyond binary classification. 


