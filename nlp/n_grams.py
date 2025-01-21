from collections import Counter
from itertools import islice

'''
-- HOW IT WORKS --
    Tokenizes the text into words.
    Uses zip() to create overlapping N-grams.
    Counts occurrences of each N-gram.
    Computes probability by dividing occurrences by total N-grams.
'''

# -----------------------------------------------------------------------


''' GENERATE N-GRAMS '''

def generate_ngrams(text, n):
    """Generate n-grams from a given text."""
    words = text.split()  # Tokenize the text into words
    ngrams = zip(*[islice(words, i, None) for i in range(n)])  # Create n-grams using zip
    return [" ".join(ngram) for ngram in ngrams]  # Convert tuples to strings




''' CALCULATE N-GRAM PROBABILITIES '''

def calculate_ngram_probabilities(ngrams):
    """Calculate probabilities of n-grams."""
    total_ngrams = len(ngrams)
    ngram_counts = Counter(ngrams)
    
    probabilities = {ngram: count / total_ngrams for ngram, count in ngram_counts.items()}
    return probabilities


if __name__ == "__main__":

    text = "the dog barks and the dog runs"

    # bigrams
    bigrams = generate_ngrams(text, 2)  # Generate bigrams
    bigram_probs = calculate_ngram_probabilities(bigrams)
    print("Bigrams:", bigrams)
    print("\nBigram Probabilities:", bigram_probs)
    
    # trigrams
    trigrams = generate_ngrams(text, 3)  # Generate trigrams
    trigram_probs = calculate_ngram_probabilities(trigrams)
    print("Trigrams:", trigrams)
    print("Trigram Probabilities:", trigram_probs)