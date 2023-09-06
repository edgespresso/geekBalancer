from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Define the words
words = [
    'Abrupt', 'Agility', 'Anticipation', 'Anxious', 'Anxious', 'Anxious', 'Anxious', 'Anxious', 'Anxious', 'Anxious', 
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

def print_word_counts(word_counts):
    sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_counts:
        print(f"{word}: {count}")


# Count the frequency of each word
words_count = Counter(words)

# Generate the word cloud
wordcloud = WordCloud(width = 1000, height = 500, background_color ='white', colormap='viridis').generate_from_frequencies(words_count)

# Plot the word cloud
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.savefig('wordcloud.png')
plt.close()

# Example usage:
print_word_counts(words_count)
