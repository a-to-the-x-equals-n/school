import numpy as np
from math import log, exp
from collections import defaultdict, Counter
import random
import hw1_util as util

DATA = {'test': '', 'train': '', 'valid': ''}

for data_split in DATA:
    fname = util._dir() / "wiki.{}.tokens".format(data_split)
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
        gen = util._train(data[i : i + n])
        w = data[i + n]

        while(h := next(gen, '')): 
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

def generate_text(lm: dict[str, dict[str, float]], vocab: list[str], context: str = "he is the", n: int = 3, n_tokens: int = 25) -> str:
    """
    Generates text using an n-gram language model with backoff support.

    Parameters
    ----------
    lm : dict[str, dict[str, float]]
        The trained n-gram language model where:
        - Keys are space-separated history strings (n-1 context).
        - Values are dictionaries mapping next words to their probabilities.
    vocab : list[str]
        A list of unique words from the training dataset, used for fallback sampling.
    context : str, optional
        The initial text to seed the text generation process. Defaults to "he is the".
    n : int, optional
        The order of the n-gram model. Defaults to 3 (trigram model).
    n_tokens : int, optional
        The number of tokens to generate. Defaults to 25.

    Returns
    -------
    str
        A space-separated string representing the generated text.
    """

    n -= 1
    history = context.split()[:n]
    out = context.split()
    
    for _ in range(n_tokens):
        # h = _backoff(lm, " ".join(history)) # backoff (n - 1) if history isn't found in lm

        # probability lookup
        gen = _train(history[i : i + n])

        while (h := next(gen, '')):  # backoff n-1 grams
            if h in lm or lm['']:
                a, p = zip(*lm[h].items()) # w = [...] p = [...]
                w = np.random.choice(a = a, p = p)
                break
        else:
            w = np.random.choice(a = vocab) 

        # convert dict keys and values to arrays for np.random.choice sampling
        # if h in lm:
        #     a, p = zip(*lm[h].items()) # w = [...] p = [...]
        #     w = np.random.choice(a = a, p = p)
        # else:
        #     w = np.random.choice(a = vocab) # fallback to random selection
         
        out.append(w) # append to growing sequence 
        history = (history + [w])[-n:]
    return " ".join(out) # return full generated text



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
    T = 0 # accumulator for token count
    log_sum = 0.0 

    for i in range(len(data) - n):
        gen = util._train(data[i : i + n])
        w = data[i + n]

        # probability lookup
        while (h := next(gen, '')):  # backoff n-1 grams
            if h in lm and w in lm[h]:
                prob = lm[h][w]
                break
        else:
            prob = lm[''][w] if w in lm[''] else 1.0 / len(vocab)  # fallback to 1 / |vocab|

        log_sum += log(prob) # accumulate log prob
        T += 1

    # perplexity = exp( - (1/T) * sum of log probs )
    ppl = exp(-log_sum / T)
    return ppl

def test_ngram_lm():
    global DATA
  
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

    
if __name__ == "__main__":

    # test_ngram_lm()
    
    # for i in range(1, 5):
    #     lm = train_ngram_lm(DATA['train'], n = i)
    #     print(f"[{i}-GRAM]: {generate_text(lm, vocab = VOCAB, context = 'he is the', n = i)}")

    benchmarks = [795, 203, 141, 130]
    for i in range(1, 5):
        print(f'[{i}-GRAM]')
        lm = train_ngram_lm(DATA['train'], n = i)
        ppl = compute_perplexity(lm, DATA['test'], VOCAB, n = i)
        print(f'\tEXPECTED : {benchmarks[i - 1]}\n\tACTUAL   : {ppl:.2F}')