from collections import Counter

# Define the list of words
words = [
    "Abrupt",
    "Agility",
    "Anticipation",
    "Anxious",
    "Anxious",
    "Anxious",
    "Anxious",
    "Anxious",
    "Anxious",
    "Anxious",
    "Apprehensive",
    "Apprehensive",
    "Apprehensive",
    "Apprehensive",
    "Apprehensive",
    "At_last",
    "Awesome",
    "Awesome",
    "Be_agile",
    "Better",
    "Better",
    "Bright",
    "Cautious",
    "Cautiously_Optimistic",
    "Challenge",
    "Challenge_accepted",
    "Challenged",
    "Challenging",
    "Challenging",
    "Challenging",
    "Change",
    "Change",
    "Change_is_always_good",
    "Change_is_good",
    "Chaos",
    "Clarity",
    "Clarity",
    "Collaborative",
    "Collective",
    "Committed",
    "Complex",
    "Concerned",
    "Confident",
    "Confident",
    "Confident",
    "Confident",
    "Confuse",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confused",
    "Confusing",
    "Confusing",
    "Confusion",
    "Confusion",
    "Connect",
    "Connected",
    "Connected",
    "Connected",
    "Continuous_Improvement",
    "Cool",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Curious",
    "Daunted",
    "Depressed",
    "Developing",
    "Digital",
    "Direction",
    "Disconnected",
    "Doubtful",
    "Dubious",
    "Duplication",
    "Efficient",
    "Empowered",
    "Empowered",
    "Empowered",
    "Encouraging",
    "Encouraging",
    "Energetic",
    "Energised",
    "Energised",
    "Energised",
    "Energised",
    "Energized",
    "Energized",
    "Enthused",
    "Enthusiastic",
    "Enthusiastic",
    "Entusiastic",
    "Evolution",
    "Excellent",
    "Excellent",
    "Excellent",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited",
    "Excited_about_evolution",
    "Excitement",
    "Exciting",
    "Exciting",
    "Exciting",
    "Exciting",
    "Exciting",
    "Exhausted",
    "Existed",
    "Expectant",
    "Expectant",
    "Expectation",
    "Expectation",
    "Exquisite",
    "Fantastic",
    "Fantastic",
    "Flabbergasted",
    "Flexible",
    "Fruitful",
    "Frustrated",
    "Future_looking",
    "GeoTec",
    "Good",
    "Great",
    "Great",
    "Great_idea",
    "Growing",
    "Happy",
    "Happy",
    "Happy",
    "Hope",
    "Hopeful",
    "Hopeful",
    "Hopeful",
    "Hopeful",
    "Hopeful",
    "Hopeful",
    "Hopeful",
    "Hopeful",
    "Hopeful",
    "Hopeful",
    "Improvement",
    "Informed",
    "Innovative",
    "Inspired",
    "Inspired",
    "Interested",
    "Interested",
    "Interesting",
    "Interesting",
    "Invested",
    "Invigorated",
    "Left_out",
    "Looking_forward",
    "Lost",
    "Matrix",
    "Mixed_emotions",
    "Money_money_money",
    "More_opportunities",
    "Motivated",
    "Motivated",
    "Motivating",
    "Necessary",
    "Neutral",
    "Neutral",
    "Neutral",
    "New_possibilities",
    "No_visibility_on_growth",
    "Not_clear",
    "Not_supported",
    "Nothing_mich",
    "Observant",
    "Ok",
    "One_d_t_is_good",
    "One_DnT",
    "One_team_to_excel_value",
    "Open_minded",
    "Opportunities",
    "Opportunities",
    "Opportunities",
    "Opportunity",
    "Opportunity",
    "Opportunity",
    "Opportunity",
    "Opportunity",
    "Optimistic",
    "Optimistic",
    "Optimistic",
    "Optimistic",
    "Optimistic",
    "Optimistic",
    "Organised",
    "Overlap",
    "Overloaded",
    "Overwhelmed",
    "Overworked",
    "Passionate",
    "Passionate",
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Possibilities",
    "Potato",
    "Promising",
    "Promising",
    "Questioned",
    "Quirous",
    "Relieved",
    "Relieved",
    "Responsibility",
    "Responsibility",
    "Restarting",
    "Revitalised",
    "Scared",
    "Sceptical",
    "Share",
    "Spinach",
    "Strong",
    "Supercharged",
    "Superficial",
    "Team_effort",
    "Thankful",
    "Tholing",
    "Thrilled",
    "Together",
    "Trepidation",
    "Uncertain",
    "Uncertain",
    "Uncertainty",
    "Uncertainty",
    "Unclear",
    "Uneasy",
    "Unprepared",
    "Unsettled",
    "Unsupported",
    "Unsure",
    "Unsure",
    "Unsure",
    "Value",
    "Valued",
    "Valued",
    "Wait",
    "Whats_in_it",
    "Wonderful",
    "Worried",
    "Worried",
    "Worried",
    "Worried",
    "Worried",
    "Worried",
    "Worried",
    "Worried"
]

# Normalize the words by replacing underscores with spaces and converting to lowercase
normalized_words = [word.replace('_', ' ').lower() for word in words]

# Count occurrences of each normalized word
normalized_word_counts = Counter(normalized_words)

# Create a list of strings with the count of each normalized word
aggregated_normalized_list = [f"{word} ({count})" if count > 1 else word for word, count in normalized_word_counts.items()]

# Print the aggregated list
print(aggregated_normalized_list)