from math import log, exp
from collections import defaultdict, Counter
import hw1_util as util

DATA = {'test': '', 'train': '', 'valid': ''}

for data_split in DATA:
    fname = util._path("wiki.{}.tokens".format(data_split))
    with open(fname, 'r') as f_wiki:
        DATA[data_split] = f_wiki.read().lower().split()
        
VOCAB = list(set(DATA['train']))


def train_ngram_lm(data: list[str], n: int = 3) -> dict[str, dict[str, float]]:
    """ 
    Trains an n-gram language model with backoff support.

    Parameters:
    -----------
    data : list of str
        A list of tokens representing the training dataset.
    n : int, optional
        The order of the n-gram model. Defaults to 3.

    Returns:
    --------
    dict of {str: dict of {str: float}}
        A dictionary where:
        - Keys are space-separated strings representing the history (n - 1 context).
        - Values are dictionaries mapping possible next words to their probabilities.
    """
    
    n -= 1
    data = (['<S>'] * n) + data
    lm = defaultdict(Counter)
    
    # collect n..0-grams
    for i in range(len(data) - n): # up to len(data - n)
        backoff = util._train(data[i : i + n])
        w = data[i + n]

        while(h := next(backoff, '')): 
            lm[h][w] += 1
        else: 
            # explicitly handle empty histories
            lm[''][w] += 1 # generator evaluates as None once yield '' ; loop never entered when h = ''

    # convert raw counts into MLEs
    lm = { 
        h : {w: count / sum(word_counts.values()) for w, count in word_counts.items()} 
        for h, word_counts in lm.items() 
    }
    return lm



def compute_perplexity(lm: dict[str, dict[str, float]], data: list[str], vocab: list[str], n: int = 3) -> float:
    """
    Computes perplexity using backoff logic for an n-gram language model.

    Parameters:
    -----------
    lm  : dict of {str: dict of {str: float}}
        The language model returned by train_ngram_lm (with backoff counts).
        - Keys are space-separated history strings (n - 1 context).
        - Values are dictionaries mapping next words to probabilities.
    data  : list of str.
        Tokenized test data sequence.
    vocab : list of str
        list of unique tokens from training.
    n     : int, the original n (e.g. 3 => trigram). We'll internally do (n -= 1).

    Returns:
    --------
    perplexity : float
        The perplexity of 'data' under the language model 'lm'.
    """

    n -= 1  # pad
    data = (['<S>'] * n) + data
    T, log_sum = 0, 0.0

    for i in range(len(data) - n):
        backoff = util._train(data[i : i + n])
        w = data[i + n]

        # probability lookup
        while (h := next(backoff, '')):  # backoff n-1 grams
            if h in lm and w in lm[h]:
                prob = lm[h][w] # history found
                break # end backoff
        else:
            prob = lm[''][w] if w in lm[''] else 1.0 / len(vocab)  # fallback to 1 / |vocab|

        log_sum += log(prob) # accumulate log prob
        T += 1

    # perplexity = exp( - (1/T) * sum of log probs )
    ppl = exp(-log_sum / T)
    return ppl


if __name__ == "__main__":

    benchmarks = [795, 203, 141, 130]
    for i in range(1, 5):
        print(f'[{i}-GRAM]')
        lm = train_ngram_lm(DATA['train'], n = i)
        ppl = compute_perplexity(lm, DATA['test'], VOCAB, n = i)
        print(f'\tEXPECTED : {benchmarks[i - 1]}\n\tACTUAL   : {ppl:.2F}')