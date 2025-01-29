from hw1_util import _backoff, _context
from the_exterminator import debug
from math import log, exp
from collections import defaultdict, Counter
import random
import math
import numpy as np


DATA = {'test': '', 'train': '', 'valid': ''}

for data_split in DATA:
    fname = "tokens/wiki.{}.tokens".format(data_split)
    with open(fname, 'r') as f_wiki:
        DATA[data_split] = f_wiki.read().lower().split()

VOCAB = list(set(DATA['train']))

def train_ngram_lm(data: list[str], n: int = 3) -> dict:
    """
    Trains an n-gram language model with backoff counts:
    - For order=3, it collects trigram, bigram, and unigram counts.
    - Key: 'w1 w2' => Value: { 'w3': prob, 'w4': prob, ... }
    - Also includes backoff keys like 'w2' and '' for the same next words.
    """
    # 1) Use a defaultdict of Counters to accumulate raw counts
    counts = defaultdict(Counter)

    # 2) Prepend <S> tokens (order-1 times)
    pad = n - 1
    data = (['<S>'] * pad) + data

    # 3) Loop over positions, stopping so we don't go out of range
    #    (skip the last (order-1) tokens)
    for i in range(len(data) - (n - 1)):
        # 4) For j in [1..order], build a backoff context of length (j-1)
        #    and increment counts for the next word
        for j in range(1, n + 1):
            # j=1 => context of length 0 => '' (unigram),
            # j=2 => context of length 1 => bigram,
            # ...
            context_length = j - 1   # how many tokens in the "history"
            if i + context_length >= len(data):
                # If we try to read beyond data, break out or continue
                break

            # Build the history and the next word
            history_tokens = data[i : i + context_length]   # e.g. length = j-1
            history_str = " ".join(history_tokens)          # e.g. "" or "w1" or "w1 w2"
            
            # Next word is data[i + context_length], if in range
            next_word_index = i + context_length
            if next_word_index < len(data):
                next_word = data[next_word_index]
            else:
                continue  # skip if out of range (unlikely with the break logic above)

            # 5) Increment raw counts
            counts[history_str][next_word] += 1

    # 6) Convert counts to probabilities
    lm = {}
    for history, word_counts in counts.items():
        total = sum(word_counts.values())
        # Probability distribution for each next_word
        lm[history] = { w: (cnt / total) for w, cnt in word_counts.items() }

    return lm

def test_ngram_lm():
    print('checking empty history ...')
    lm1 = train_ngram_lm(DATA['train'], n = 1)
    assert '' in lm1, "empty history should be in the language model!"
    
    print('checking probability distributions ...')
    lm2 = train_ngram_lm(DATA['train'], n = 2 )
    sample = [sum(lm2[k].values()) for k in random.sample(list(lm2), 10)]
    assert all([a > 0.999 and a < 1.001 for a in sample]), "lm[history][word] should sum to 1!"
    
    print('checking lengths of histories ...')
    lm3 = train_ngram_lm(DATA['train'], n = 3)
    assert len(set([len(k.split()) for k in list(lm3)])) == 3, "lm object should store histories of all sizes!"
    
    print('checking word distribution values ...')
    assert lm1['']['the'] < 0.064 and lm1['']['the'] > 0.062 and \
        lm2['the']['first'] < 0.017 and lm2['the']['first'] > 0.016 and \
        lm3['the first']['time'] < 0.106 and lm3['the first']['time'] > 0.105, \
        "values do not match!"
    
    print("Congratulations, you passed the ngram check!")


    import numpy as np

def generate_text(lm: dict, vocab: list, context: str = "he is the", order: int = 3, num_tok: int = 25) -> str:
    """
    Generates text using an n-gram (backoff) language model.

    Parameters:
    -----------
    lm : dict
        The language model dictionary returned by train_ngram_lm().
    vocab : list
        List of unique word types from the training set.
    context : str
        A space-separated string of tokens to warm up generation.
    order : int
        Order of the language model (e.g. 3 for trigram).
    num_tok : int
        Number of tokens to generate after 'context'.

    Returns:
    --------
    A space-separated string of the generated text.
    """
    # 1) Parse input context into tokens
    history_tokens = context.split()

    # Generate tokens one by one
    for _ in range(num_tok):
        
        # 2) Build a history string of up to (order-1) tokens
        #    e.g. if order=3, we keep the last 2 tokens
        h_len = order - 1
        if len(history_tokens) >= h_len:
            # Keep only the last (order-1) tokens
            history_str = " ".join(history_tokens[-h_len:])
        else:
            # If not enough tokens, just join what we have
            history_str = " ".join(history_tokens)

        # 3) Apply backoff if this history is not in the model
        h_backoff = _backoff(lm, history_str)

        # 4) If we still don't find h_backoff (i.e. h_backoff == '' and '' not in lm),
        #    we do a uniform random choice from vocab
        if h_backoff not in lm:
            next_word = np.random.choice(vocab)
        else:
            # 5) Retrieve the distribution for the current history
            dist = lm[h_backoff]   # e.g. {"the": 0.5, "is": 0.25, ...}

            # 6) Convert dict keys and values to arrays for np.random.choice
            words, probs = zip(*dist.items())  # words=(...), probs=(...)
            words = list(words)
            probs = list(probs)

            # 7) Sample the next token from this distribution
            next_word = np.random.choice(words, p=probs)

        # 8) Append to our growing sequence
        history_tokens.append(next_word)

    # 9) Return the entire sequence as a string
    return " ".join(history_tokens)



import math

def compute_perplexity(lm, data, vocab, order=3):
    """
    Computes perplexity using backoff logic for an n-gram language model.

    Starter code structure:
    1. Decrease 'order' by 1
    2. Pad the data with <S> tokens
    3. For each token to predict (h, w):
       - 'h' is the current history (joined by spaces)
       - 'w' is the next token
       - If h is not in lm, back off by dropping the first token.
       - If no history is found, fallback to 1/|vocab|.
    4. Sum up log(prob) for all tokens, exponentiate at the end.

    Parameters:
    -----------
    lm    : dict
        The language model returned by train_ngram_lm (with backoff counts).
    data  : list of tokens (test data).
    vocab : list of unique tokens from training.
    order : int, the original n (e.g. 3 => trigram). We'll internally do (order -= 1).

    Returns:
    --------
    perplexity : float
        The perplexity of 'data' under the language model 'lm'.
    """

    # We'll use math.log / math.exp for numeric stability
    order -= 1  # e.g. if user says 3 => now 2 (the 'history' length)
    data = ['<S>'] * order + data  # pad data with (order) <S>
    
    log_sum = 0.0
    T = 0  # We'll count how many tokens we're predicting

    for i in range(len(data) - order):
        # h is history of length 'order', w is next token
        h, w = ' '.join(data[i : i + order]), data[i + order]

        # Backoff logic:
        # 1) While h not in lm and h is not empty, drop the first token.
        backoff_h = h
        while backoff_h not in lm and backoff_h:
            # Drop the first word from backoff_h
            backoff_h = ' '.join(backoff_h.split()[1:])

        # Probability lookup:
        if backoff_h in lm and w in lm[backoff_h]:
            prob = lm[backoff_h][w]
        else:
            # If we still can't find it => fallback to 1/|vocab|
            prob = 1.0 / len(vocab)

        # Accumulate log(prob)
        log_sum += math.log(prob)
        T += 1

    # Perplexity = exp( - (1/T) * sum of log probs )
    ppl = math.exp(-log_sum / T)
    return ppl


def train_ngram_lm_exact(data: list[str], n: int) -> dict:
    """
    Trains an EXACT n-gram model (no backoff in one dictionary).
    Only collects n-grams (context of length n-1, plus 1 next word).
    """
    from collections import defaultdict, Counter

    # 1) Pad with (n-1) <S> tokens
    pad = n - 1
    data = (["<S>"] * pad) + data

    counts = defaultdict(Counter)

    # 2) Collect exactly n-grams
    for i in range(len(data) - pad):
        # context tokens => data[i : i+(n-1)]
        ctx_tokens = data[i : i + pad]
        context_str = " ".join(ctx_tokens)
        next_word = data[i + pad]
        counts[context_str][next_word] += 1

    # 3) Convert to probabilities
    lm = {}
    for ctx, cdict in counts.items():
        total = sum(cdict.values())
        lm[ctx] = {w: cnt / total for w, cnt in cdict.items()}
    return lm




if __name__ == "__main__":

    
    # models should be around 795, 203, 141, and 130 respectively
    for o in [1, 2, 3, 4]:
        lm = train_ngram_lm(DATA['train'], n = o)
        print(f"[{o}-GRAM]: ppl {compute_perplexity(lm = lm, data = DATA['test'], vocab = VOCAB, order = o)}")
        

   
    