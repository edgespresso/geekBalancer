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
from textblob import TextBlob
import matplotlib.pyplot as plt
import nltk
from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import sentiwordnet as swn

def plot_sentiment(words, filename):
    sentiment_scores = []
    for word in words:
        # Calculate the sentiment polarity of the word
        blob = TextBlob(word)
        sentiment_score = blob.sentiment.polarity
        sentiment_scores.append(sentiment_score)
    # Plot the sentiment scores
    plt.plot(sentiment_scores)
    plt.xlabel("Word index")
    plt.ylabel("Sentiment score")
    plt.title("Sentiment analysis of words")
    plt.savefig(filename)
    plt.close()

def calculate_sentiment(words):
    sentiment_scores = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    for word in words:
        # Calculate the sentiment polarity of the word
        blob = TextBlob(word)
        sentiment_score = blob.sentiment.polarity
        sentiment_scores.append(sentiment_score)
        # Classify the sentiment as positive, neutral, or negative
        #print(f"Word: {word}, Sentiment: {sentiment_score}")
        if sentiment_score > 0:
            positive_count += 1
        elif sentiment_score == 0:
            neutral_count += 1
        else:
            negative_count += 1
    # Calculate the average sentiment polarity of the list
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    # Classify the sentiment as positive, neutral, or negative
    if avg_sentiment > 0:
        sentiment = "positive"
    elif avg_sentiment == 0:
        sentiment = "neutral"
    else:
        sentiment = "negative"
    return (sentiment, positive_count, neutral_count, negative_count)

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
            #print(f"Closest word: {closest}")
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

def create_gauge_chart(score, filename):
    # Define the colors for the gauge chart
    red = "#FF0000"
    yellow = "#FFFF00"
    green = "#00FF00"
    # Define the ranges for the gauge chart
    red_range = np.arange(-1, -0.5, 0.01)
    yellow_range = np.arange(-0.5, 0.5, 0.01)
    green_range = np.arange(0.5, 1, 0.01)
    # Create the gauge chart
    fig, ax = plt.subplots()
    ax.set_ylim([-1, 1])
    ax.set_xlim([-1, 1])
    ax.add_artist(plt.Circle((0, 0), 1, color=red, alpha=0.2))
    ax.add_artist(plt.Circle((0, 0), 1, color=yellow, alpha=0.2))
    ax.add_artist(plt.Circle((0, 0), 1, color=green, alpha=0.2))
    ax.plot(np.cos(red_range * np.pi), np.sin(red_range * np.pi), color=red, linewidth=10)
    ax.plot(np.cos(yellow_range * np.pi), np.sin(yellow_range * np.pi), color=yellow, linewidth=10)
    ax.plot(np.cos(green_range * np.pi), np.sin(green_range * np.pi), color=green, linewidth=10)
    ax.plot([0, score], [0, np.sqrt(1 - score**2)], color="black", linewidth=10)
    ax.plot([0, score], [0, -np.sqrt(1 - score**2)], color="black", linewidth=10)
    ax.plot(score, np.sqrt(1 - score**2), marker="o", markersize=20, color="black")
    ax.axis("off")
    plt.savefig(filename)
    plt.close()

def create_donut_chart(positive_count, neutral_count, negative_count, filename):
    # Define the data for the donut chart
    data = [positive_count, neutral_count, negative_count]
    labels = ["Positive", "Neutral", "Negative"]
    colors = ["#00FF00", "#FFFF00", "#FF0000"]
    # Create the donut chart
    fig, ax = plt.subplots()
    wedges, _, labels = ax.pie(data, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, pctdistance=0.85, textprops={'fontsize': 14})
    ax.add_artist(plt.Circle((0, 0), 0.7, color="white"))
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
        x = np.cos(np.radians(angle))
        y = np.sin(np.radians(angle))
        ax.annotate(f"{labels[i]} ({data[i]/sum(data)*100:.1f}%)", xy=(x, y), fontsize=14, ha="center", va="center")
    ax.set_title("Sentiment analysis of words", fontsize=16)
    plt.savefig(filename)
    plt.close()

def create_pie_chart(positive_count, neutral_count, negative_count, filename):
    # Define the data for the pie chart
    data = [positive_count, neutral_count, negative_count]
    labels = ["Positive", "Neutral", "Negative"]
    colors = ["#00FF00", "#FFFF00", "#FF0000"]
    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, textprops={'fontsize': 14})
    ax.set_title("Sentiment analysis of words", fontsize=16)
    plt.savefig(filename)
    plt.close()


def calculate_afinn_sentiment(words):
    afinn = Afinn()
    sentiment_scores = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    for word in words:
        # Calculate the sentiment polarity of the word
        sentiment_score = afinn.score(word)
        sentiment_scores.append(sentiment_score)
        # Classify the sentiment as positive, neutral, or negative
        print(f"Word: {word}, Sentiment: {sentiment_score}")
        if sentiment_score > 0:
            positive_count += 1
        elif sentiment_score == 0:
            neutral_count += 1
        else:
            negative_count += 1
    # Calculate the average sentiment polarity of the list
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    # Classify the sentiment as positive, neutral, or negative
    if avg_sentiment > 0:
        sentiment = "positive"
    elif avg_sentiment == 0:
        sentiment = "neutral"
    else:
        sentiment = "negative"
    return sentiment, positive_count, neutral_count, negative_count, avg_sentiment
    
def calculate_sentiwordnet_sentiment(words):
    sentiment_scores = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    for word in words:
        # Calculate the sentiment polarity of the word
        synsets = list(swn.senti_synsets(word))
        if synsets:
            sentiment_score = synsets[0].pos_score() - synsets[0].neg_score()
        else:
            sentiment_score = 0
        sentiment_scores.append(sentiment_score)
        # Classify the sentiment as positive, neutral, or negative
        print(f"Word: {word}, Sentiment: {sentiment_score}")
        if sentiment_score > 0:
            positive_count += 1
        elif sentiment_score == 0:
            neutral_count += 1
        else:
            negative_count += 1
    # Calculate the average sentiment polarity of the list
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    # Classify the sentiment as positive, neutral, or negative
    if avg_sentiment > 0:
        sentiment = "positive"
    elif avg_sentiment == 0:
        sentiment = "neutral"
    else:
        sentiment = "negative"
    return sentiment, positive_count, neutral_count, negative_count, avg_sentiment

def calculate_vader_sentiment_OLD(words):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    for word in words:
        # Calculate the sentiment polarity of the word
        sentiment_score = analyzer.polarity_scores(word)["compound"]
        sentiment_scores.append(sentiment_score)
        # Classify the sentiment as positive, neutral, or negative
        print(f"Word: {word}, Sentiment: {sentiment_score}")
        if sentiment_score > 0:
            positive_count += 1
        elif sentiment_score == 0:
            neutral_count += 1
        else:
            negative_count += 1
    # Calculate the average sentiment polarity of the list
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    # Classify the sentiment as positive, neutral, or negative
    if avg_sentiment > 0:
        sentiment = "positive"
    elif avg_sentiment == 0:
        sentiment = "neutral"
    else:
        sentiment = "negative"
    return sentiment, positive_count, neutral_count, negative_count, avg_sentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def calculate_vader_sentiment_with_top_words(words):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    positive_words = []
    negative_words = []
    neutral_words = []
    for word in words:
        # Calculate the sentiment polarity of the word
        sentiment_score = analyzer.polarity_scores(word)["compound"]
        sentiment_scores.append(sentiment_score)
        # Classify the sentiment as positive, neutral, or negative
        if sentiment_score > 0:
            positive_count += 1
            positive_words.append((word, sentiment_score))
        elif sentiment_score == 0:
            neutral_count += 1
            neutral_words.append((word, sentiment_score))
        else:
            negative_count += 1
            negative_words.append((word, sentiment_score))
    # Sort the positive, negative, and neutral words by sentiment score
    positive_words.sort(key=lambda x: x[1], reverse=True)
    negative_words.sort(key=lambda x: x[1])
    neutral_words.sort(key=lambda x: x[1])
    # Get the top 5 positive, negative, and neutral words
    words = set(words)
    top_positive_words = set([word[0] for word in positive_words[:20] if word[0] not in negative_words and word[0] not in neutral_words])
    top_negative_words = set([word[0] for word in negative_words[:20] if word[0] not in positive_words and word[0] not in neutral_words])
    top_neutral_words = set([word[0] for word in neutral_words[:20] if word[0] not in positive_words and word[0] not in negative_words])
    # Calculate the average sentiment polarity of the list
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    # Classify the sentiment as positive, neutral, or negative
    if avg_sentiment > 0:
        sentiment = "positive"
    elif avg_sentiment == 0:
        sentiment = "neutral"
    else:
        sentiment = "negative"
    return sentiment, positive_count, neutral_count, negative_count, avg_sentiment, top_positive_words, top_negative_words, top_neutral_words

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

# Calculate the sentiment of the words
sentiment, positive_count, neutral_count, negative_count = calculate_sentiment(words)

# Print the sentiment and counts
print(f"The sentiment of the words is {sentiment}")
print(f"Number of positive words: {positive_count}")
print(f"Number of neutral words: {neutral_count}")
print(f"Number of negative words: {negative_count}")

# Plot the sentiment scores of the words and save the plot to a PNG file
plot_sentiment(words, "sentiment_plot.png")

# Create a gauge chart for the sentiment score of the words and save the chart to a PNG file
score = 0 if sentiment == "neutral" else (1 if sentiment == "positive" else -1)
create_gauge_chart(score, "sentiment_gauge.png")

# Create a donut pie chart for the sentiment of the words and save the chart to a PNG file
create_donut_chart(positive_count, neutral_count, negative_count, "sentiment_donut.png")


# Create a pie chart for the sentiment of the words and save the chart to a PNG file
create_pie_chart(positive_count, neutral_count, negative_count, "sentiment_pie.png")





print("")
print("VADER SENTIMENT ANALYSIS:")
## Calculate the VADER Sentiment Scores of the words
#sentiment, positive_count, neutral_count, negative_count, avg_sentiment = calculate_vader_sentiment(words)
# Call the function to get the sentiment and top words
sentiment, positive_count, neutral_count, negative_count, avg_sentiment, top_positive_words, top_negative_words, top_neutral_words = calculate_vader_sentiment_with_top_words(words)

# Print the VADER Sentiment Scores
print(f"Sentiment: {sentiment}")
print(f"Number of positive words: {positive_count}")
print(f"Number of neutral words: {neutral_count}")
print(f"Number of negative words: {negative_count}")
print(f"Average sentiment score: {avg_sentiment}")
print(f"Top positive words: {', '.join(top_positive_words)}")
print(f"Top negative words: {', '.join(top_negative_words)}")
print(f"Top neutral words: {', '.join(top_neutral_words)}")

#nltk.download('sentiwordnet')
#print("")
#print("SENTIWORDNET ANALYSIS:")
## Calculate the SentiWordNet Sentiment Scores of the words
#sentiment, positive_count, neutral_count, negative_count, avg_sentiment = calculate_sentiwordnet_sentiment(words)

## Print the SentiWordNet Sentiment Scores
#print(f"Sentiment: {sentiment}")
#print(f"Number of positive words: {positive_count}")
#print(f"Number of neutral words: {neutral_count}")
#print(f"Number of negative words: {negative_count}")
#print(f"Average sentiment score: {avg_sentiment}")


#print("")
#print("AFINN ANALYSIS:")
## Calculate the AFINN Sentiment Scores of the words
#sentiment, positive_count, neutral_count, negative_count, avg_sentiment = calculate_afinn_sentiment(words)##
#
# Print the AFINN Sentiment Scores
#print(f"Sentiment: {sentiment}")
#print(f"Number of positive words: {positive_count}")
#print(f"Number of neutral words: {neutral_count}")
#print(f"Number of negative words: {negative_count}")
#print(f"Average sentiment score: {avg_sentiment}")