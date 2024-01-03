import string
import difflib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def tokenize(text):
    """Split the text into lowercased tokens, removing punctuation."""
    return set(text.lower().translate(str.maketrans('', '', string.punctuation)).split())


def jaccard_similarity(set1, set2):
    """Calculate the Jaccard Similarity between two sets."""
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def find_best_match(product_elements, search_query):
    search_tokens = tokenize(search_query)
    best_match_element = None
    highest_similarity = 0.0

    for product_element in product_elements:
        product_text = product_element.text
        product_tokens = tokenize(product_text)
        similarity = jaccard_similarity(search_tokens, product_tokens)

        # You could also combine this with the SequenceMatcher from difflib if needed
        sequence_similarity = difflib.SequenceMatcher(None, search_query, product_text).ratio()
        total_similarity = (similarity + sequence_similarity) / 2  # Average the two similarities

        if total_similarity > highest_similarity:
            highest_similarity = total_similarity
            best_match_element = product_element

    return best_match_element, highest_similarity


def setup_webdriver():
    """
    This function sets up the Selenium WebDriver.

    :return: A WebDriver instance
    """
    # Assuming Chrome WebDriver for demonstration purposes; you might need to configure this as needed.
    service_obj = Service()
    driver = webdriver.Chrome(service=service_obj)
    return driver

# Additional utility functions can be added here as needed
