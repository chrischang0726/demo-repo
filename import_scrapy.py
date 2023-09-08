import re
from zenrows import ZenRowsClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize, pos_tag
from collections import Counter
import csv

# Download NLTK data (if not already downloaded)
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

# Initialize the ZenRowsClient with your API key and parameters
zenrows_client = ZenRowsClient("a9b63948d66b35f3682a8a0ad4b6d051cb941e0e")

# Define the URL of the webpage to scrape using ZenRows
base_url = "https://bestcompany.com/health-insurance/company/bluecross-blueshield?page={page}#reviews"

# Define parameters for ZenRows request
params = {"autoparse": "true"}

# Define the number of pages to scrape
num_pages = 15 # Change this to the desired number of pages

# Create an empty list to store all adjectives across all pages
all_adjectives = []

# Iterate through the specified number of pages
for page_number in range(1, num_pages + 1):
    # Construct the full URL for the current page
    current_url = base_url.format(page=page_number)

    # Use ZenRows to fetch the webpage content with autoparsing
    zenrows_response = zenrows_client.get(current_url, params=params)

    # Check if ZenRows response contains text content
    if not zenrows_response.text:
        # No more pages or error occurred, exit the loop
        break

    # Get the webpage content from ZenRows response
    webpage_content = zenrows_response.text

    # Remove symbols and punctuation
    webpage_content = re.sub(r'[^\w\s]', '', webpage_content)

    # Tokenize the cleaned text into words
    words = word_tokenize(webpage_content)

    # Perform part-of-speech tagging to identify adjectives
    tagged_words = pos_tag(words)

    # Define a list of generic adjectives to exclude
    exclude_adjectives = ["much", "type", "url", "next", "great", "good", "many", "sure", "same", "different", "able", "other", "itemreviewed", "ratingvalue", "medical"]

    # Filter only adjectives (JJ) from the tagged words and exclude generic adjectives
    adjectives = [word for word, tag in tagged_words if tag == "JJ" and word.lower() not in exclude_adjectives]

    # Append the adjectives from the current page to the list
    all_adjectives.extend(adjectives)

# Create a word frequency count of adjectives across all pages
adjective_counts = Counter(all_adjectives)

# Get the top 100 adjectives with their frequencies
top_100_adjectives = adjective_counts.most_common(100)

# Create a WordCloud with frequencies
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    # Pass the dictionary of word frequencies as input
    prefer_horizontal=1.0,  # Controls the direction of words
)
wordcloud.generate_from_frequencies(dict(top_100_adjectives))  # Use word frequencies

# Display the WordCloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("BlueShiled's Top 100")
plt.show()

# Export top 100 words and their frequencies to a CSV file
with open("top_100_adjectives.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Word", "Frequency"])
    for word, frequency in top_100_adjectives:
        csv_writer.writerow([word, frequency])


