import re

# Try pasting into code to transfer list of dictionaries.

if __name__ == "__main__":

    with open("djMix.json") as input:

        print("STARTING TO READ THE DJ MIX DATA")
        
        djMixData = input.read()
        print("\n" + djMixData[0:30])
        djMixData = djMixData.split('\"title\"')
        print("\n")
        
        print("ADDITIONAL SPLIT")
            
        for i in range(1, 40):
            djMixData[i] = re.split("\"}|\",\"", djMixData[i])[0][2:]
            print("TITLE: " + djMixData[i] + "\n")

    with open("SpotifyAudioFeaturesApril2019.csv") as input:
        #print(input[0:20])
'''
import kagglehub

# Download latest version
path = kagglehub.dataset_download("tomigelo/spotify-audio-features")

print("Path to dataset files:", path)'''