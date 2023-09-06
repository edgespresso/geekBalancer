from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
import numpy as np
import re
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk.metrics import edit_distance
from nltk.corpus import wordnet_ic

def levenshtein_distance(s1, s2):
    """Compute the Levenshtein distance between two strings."""
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = np.arange(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances

    return distances[-1]

def closest_word(stemmed_word, word_list):
    """Find the closest word from word_list to the given stemmed_word."""
    min_distance = float('inf')
    closest = ""
    print(f"\nStemmed word: {stemmed_word}")
    for word in word_list:
        distance = levenshtein_distance(stemmed_word, word)
        if distance < min_distance:
            min_distance = distance
            closest = word
            print(f"Closest word: {closest}")
    return closest

def process_words_stemming_only(word_list):
    """
    Process the list of words using stemming.
    """
    processed_list = []
    for word in word_list:
        # Stem the word
        print(f"*******************Orignal word: {word}")
        stemmed_word = stemmer.stem(word)
        processed_list.append(stemmed_word.capitalize())  # Capitalize the processed word
    
    return processed_list

def print_word_counts_alpha_order(word_counts):
    sorted_counts = sorted(word_counts.items(), key=lambda x: (x[0].lower(), x[1]))
    for word, count in sorted_counts:
        print(f"{word}: {count}")

def print_word_counts(word_counts):
    sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_counts:
        print(f"{word}: {count}")

def replace_words_in_list(words, replace_dict):
    """
    Replace words in the list based on a given dictionary.
    
    Parameters:
    - words: List of words.
    - replace_dict: Dictionary containing word replacements.
    
    Returns:
    Modified list of words.
    """
    return [replace_dict.get(word, word) for word in words]

# Define the words
words = [
    'Abrupt', 'Agility', 'Anticipate', 'Anxious', 'Anxious', 'Anxious', 'Anxious', 'Anxious', 'Anxious', 'Anxious', 
    'Apprehensive', 'Apprehensive', 'Apprehensive', 'Apprehensive', 'Apprehensive', 'At_last', 'Awesome', 'Awesome', 
    'Be_agile', 'Better', 'Better', 'Bright', 'Cautious', 'Cautiously_Optimistic', 'Challenging', 'Challenge_accepted', 
    'Challenging', 'Challenging', 'Challenging', 'Challenging', 'Change', 'Change', 'Change', 'Change', 'Chaos', 'Clarity', 
    'Clarity', 'Collaborative', 'Collective', 'Committed', 'Complex', 'Concerned', 'Confident', 'Confident', 'Confident', 
    'Confident', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 
    'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 
    'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 
    'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 'Confused', 
    'Confused', 'Confused', 'Confused', 'Confused', 'Connected', 'Connected', 'Connected', 'Connected', 
    'Continuous_Improvement', 'Cool', 'Curious', 'Curious', 'Curious', 'Curious', 'Curious', 'Curious', 'Curious', 'Curious', 
    'Curious', 'Curious', 'Curious', 'Curious', 'Curious', 'Daunted', 'Depressed', 'Developing', 'Digital', 'Direction', 
    'Disconnected', 'Doubtful', 'Dubious', 'Duplication', 'Efficient', 'Empowered', 'Empowered', 'Empowered', 'Encouraging', 
    'Encouraging', 'Energetic', 'Energised', 'Energised', 'Energised', 'Energised', 'Energized', 'Energized', 'Enthused', 
    'Enthusiastic', 'Enthusiastic', 'Entusiastic', 'Evolution', 'Excellent', 'Excellent', 'Excellent', 'Excited', 'Excited', 
    'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 
    'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 
    'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 
    'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 
    'Excited', 'Excited', 'Excited', 'Excited', 'Excited', 'Excited_about_evolution', 'Excitement', 'Exciting', 'Exciting', 
    'Exciting', 'Exciting', 'Exciting', 'Exhausted', 'Existed', 'Expectant', 'Expectant', 'Expectation', 'Expectation', 
    'Exquisite', 'Fantastic', 'Fantastic', 'Flabbergasted', 'Flexible', 'Fruitful', 'Frustrated', 'Future_looking', 'GeoTec', 
    'Good', 'Great', 'Great', 'Great_idea', 'Growing', 'Happy', 'Happy', 'Happy', 'Hope', 'Hopeful', 'Hopeful', 'Hopeful', 
    'Hopeful', 'Hopeful', 'Hopeful', 'Hopeful', 'Hopeful', 'Hopeful', 'Hopeful', 'Hopeful', 'Improvement', 'Informed', 
    'Innovative', 'Inspired', 'Inspired', 'Interested', 'Interested', 'Interesting', 'Interesting', 'Invested', 'Invigorated', 
    'Left_out', 'Looking_forward', 'Lost', 'Matrix', 'Mixed_emotions', 'Money_money_money', 'More_opportunities', 'Motivated', 
    'Motivated', 'Motivating', 'Necessary', 'Neutral', 'Neutral', 'Neutral', 'New_possibilities', 'No_visibility_on_growth', 
    'Not_clear', 'Not_supported', 'Nothing_mich', 'Observant', 'Ok', 'One_d_t_is_good', 'One_DnT', 'One_team_to_excel_value', 
    'Open_minded', 'Opportunities', 'Opportunities', 'Opportunities', 'Opportunity', 'Opportunity', 'Opportunity', 
    'Opportunity', 'Opportunity', 'Optimistic', 'Optimistic', 'Optimistic', 'Optimistic', 'Optimistic', 'Optimistic', 
    'Organised', 'Overlap', 'Overloaded', 'Overwhelmed', 'Overworked', 'Passionate', 'Passionate', 'Positive', 'Positive', 
    'Positive', 'Positive', 'Possibilities', 'Potato', 'Promising', 'Promising', 'Questioned', 'Quirous', 'Relieved', 
    'Relieved', 'Responsibility', 'Responsibility', 'Restarting', 'Revitalised', 'Scared', 'Sceptical', 'Share', 'Spinach', 
    'Strong', 'Supercharged', 'Superficial', 'Team_effort', 'Thankful', 'Tholing', 'Thrilled', 'Together', 'Trepidation', 
    'Uncertain', 'Uncertain', 'Uncertainty', 'Uncertainty', 'Unclear', 'Uneasy', 'Unprepared', 'Unsettled', 'Unsupported', 
    'Unsure', 'Unsure', 'Unsure', 'Value', 'Valued', 'Valued', 'Wait', 'Whats_in_it', 'Wonderful', 'Worried', 'Worried', 
    'Worried', 'Worried', 'Worried', 'Worried', 'Worried', 'Worried',
]

# Define the replacement dictionary (change <first word> to <second word> in pair)
replace_words = {
    "Uncertainty": "Uncertain",
    "Challenge_accepted": "Challenging",
    "Energised": "Energized",
    "Energetic": "Energized",
    "Excited_about_evolution": "Excited",
    "Cautiously_Optimistic": "Optimistic",
    "Be_agile": "Agility",
    "One_Dnt_is_good": "One_Team",
    "One_DnT": "One_Team",
    "One_team_to_excel_value": "One_Team",
    "Quorious": "Curious",
    "Entusiastic": "Enthusiastic",
    "Excitement": "Excited",

}

print("\nORIGINAL WORDS:")
print(words)
print(f"Number of original words: {len(words)}")
print("")


# Use the function
modified_words = replace_words_in_list(words, replace_words)

print("\nMANUALLY MODIFIED WORDS:")
print(modified_words)
print(f"Number of modified words: {len(modified_words)}")
print("")
words = modified_words

# Instantiate the stemmer
stemmer = PorterStemmer()

# Process the words using only stemming
processed_words_stemming = process_words_stemming_only(words)

# Replace each stemmed word with the closest word from the original list
corrected_words = [closest_word(word, words) for word in processed_words_stemming]

# Print the corrected words
print("\nAUTO COMBINED WORDS:")
print(sorted(corrected_words)) #sorted in alpha order   
print(f"Number of corrected words: {len(corrected_words)}")
print("")

# Count the frequency of each corrected word
corrected_words_count = Counter(corrected_words)

# Print the final words with counts:
print("\nFINAL WORDS with COUNTS:")
#print_word_counts(corrected_words_count)
print_word_counts_alpha_order(corrected_words_count)

# Generate the word cloud using corrected words
wordcloud_corrected = WordCloud(width=1000, height=500, background_color='white', colormap='viridis').generate_from_frequencies(corrected_words_count)

# Plot the word cloud
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud_corrected, interpolation="bilinear")
plt.axis('off')
plt.savefig('corrected_wordcloud.png')
plt.close()
print("")
print("Word cloud saved to corrected_wordcloud.png")


