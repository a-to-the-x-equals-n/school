import numpy as np
from numpy.typing import NDArray
from collections import defaultdict, Counter


ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
ALPHA_STATS = [
    0.0659, 0.012, 0.0225, 0.0343, 0.1026, 0.018, 0.0163, 0.0492, 0.0562, 0.0012,
    0.0062, 0.0325, 0.0194, 0.0545, 0.0606, 0.0156, 0.0008, 0.0483, 0.0511, 0.0731, 
    0.0223, 0.0079, 0.0191, 0.0012, 0.0159, 0.0006
]

ALPHA_IMAP = dict(zip(ALPHABET, range(len(ALPHABET))))
R_ALPHA_IMAP = {i: ch for ch, i in ALPHA_IMAP.items()}


def _imap(s: list[str] = ALPHABET) -> dict[str, int]:
    """ 
    Constructs a character-to-index mapping for given alphabet.

    Parameters
    ----------
    lang : list[str], optional
        A list of characters representing the alphabet. Defaults to ALPHABET.

    Returns
    -------
    dict[str, int]
        A dictionary where each character in `s` is mapped to its corresponding index.
    """
    c = np.unique(ar = list(s))
    return dict(zip(c, range(len(c))))

def _frequency(s: str | list[str] | defaultdict[str, Counter]) -> dict[str, float]:
    """ 
    Computes the relative frequency of each character or n-gram in the input.

    Parameters
    ----------
    s : str | list[str] | defaultdict[str, Counter]
        The input data to analyze:
        - If `s` is a string, counts character occurrences.
        - If `s` is a list of strings, flattens it and counts character occurrences.
        - If `s` is a defaultdict of Counters, treats keys as prefixes and 
          counts n-grams using the nested Counters.

    Returns
    -------
    dict[str, float]
        A dictionary where each key is a unique character or n-gram, and the 
        corresponding value is its relative frequency in the dataset, rounded to 4 decimal places.
    """

    if isinstance(s, defaultdict): # flatten dict
        s = {f"{prefix}{char}": count for prefix, counter in s.items() for char, count in counter.items()}
        ch, cts = list(s.keys()), np.array(list(s.values())) # extract counts
    else:
        ch, cts = np.unique(ar = list(s), return_counts = True) # convert input str | list to character counts

    t = np.sum(cts)
    return {ch[i]: round(cts[i] / t, 4) for i in range(len(ch))}
    
def _ngrams(s: list[str] | str, n: int = 3) -> defaultdict[str, Counter]:
    """ 
    Computes ngrams frequency counts from a given input sequence.

    Parameters
    ----------
    s : list[str] | str
        The input text or list of characters to analyze.

    n : int, optional
        The size of the n-grams. Defaults to 3 for trigrams.

    Returns
    -------
    defaultdict[str, Counter]
        A dictionary where each key is a starting character, and the value 
        is a Counter object mapping n-gram suffixes to their frequency counts.
    """
    ngrams = defaultdict(Counter)

    for i in range(len(s) - n):
        c, next_c = s[i], s[i + 1 : i + n]
        ngrams[c][next_c] += 1
    return ngrams

def _ngram_to_M(s: list[str] | str, n: int = 3) -> tuple[NDArray[np.int16], dict[str, int], dict[str, int]]:
    """ 
    Converts n-gram frequency data into a co-occurrence matrix representation.

    Parameters
    ----------
    s : list[str] | str
        The input text or list of characters from which to generate n-grams.

    Returns
    -------
    tuple[NDArray[np.int16], dict[str, int], dict[str, int]]
        - A NumPy matrix (n x m) of type int16, where rows represent single characters
          and columns represent bigrams.
        - A dictionary mapping row characters to their corresponding indices in the matrix.
        - A dictionary mapping column bigrams to their corresponding indices in the matrix.
    """

    ngram = _ngrams(s, n) # ngram frequency data

    # extract all unique bigrams
    # unpacks all counts from the nested counters
    col_keys = sorted(set().union(*[set(v.keys()) for v in ngram.values()]))
    row_keys = sorted(set(ngram.keys())) # unique single characters (row labels)

    # mappings from characters/bigrams to their respective indices
    row_imap = {c: i for i, c in enumerate(row_keys)}
    col_imap = {bigram: i for i, bigram in enumerate(col_keys)}

    M = np.zeros(shape = (len(row_keys), len(col_keys)), dtype = np.int16)

    # populate matrix with the counts from the ngram
    for row, counter in ngram.items():
        for col, count in counter.items():
            M[row_imap[row], col_imap[col]] = count

    return M, row_imap, col_imap

def _topk(d: dict[str, float | int] | list[str] | str, k: int = 10) -> dict[str, float | int]:
    """ 
    Returns the top `k` key-value pairs from a dictionary or frequency counts from a string/list.

    Parameters
    ----------
    d : dict[str, float | int] | list[str] | str
        The input dictionary to sort, or a string/list to compute frequency counts.

    k : int, optional
        The number of top elements to return. Defaults to 10.

    Returns
    -------
    dict[str, float | int]
        A dictionary containing the top `k` key-value pairs from `d`, sorted in descending order by value.
    """

    if isinstance(d, defaultdict): # flatten defaultdict[Counter] to dict
        d = {f"{prefix}{char}": count for prefix, counter in d.items() for char, count in counter.items()}

    if isinstance(d, (str, list)): # convert input str | list to character counts
        ch, cts = np.unique(ar = list(d), return_counts = True) 
        d = dict(zip(ch, cts))
    
    return dict(sorted(d.items(), key = lambda item: item[1], reverse = True)[:k])
    
def _canvas(t: str, r: str, canvas: list[str], cipher: list[str], width: int = 63) -> list[str]:
    """ 
    Replaces occurrences of `t` (target) in `canvas` at the indices found in `cipher`, and swaps them with `r` (replacement).

    Parameters
    ----------
    t : str
        The target character to be replaced.

    r : str
        The replacement character.

    canvas : list[str]
        The plaintext content to be updated.

    cipher : list[str]
        The ciphertext used to find occurrences of `t`.

    width : int, optional
        The width of each line in the formatted output. Defaults to 63.

    Returns
    -------
    list[str]
        A list of strings representing the modified canvas, split into lines of `width` characters.
    """

    # list of the indices for all occurrences of `t`
    t_indices = [i for i, ch in enumerate("".join(cipher)) if ch == t]

    canvas = list("".join(canvas))

    # swap 't' with 'r' in relative indices
    for i in t_indices:
        canvas[i] = r

    # flatten canvas
    canvas = "".join(canvas)

    # split BACK into lines of `width` characters
    canvas = [canvas[i : i + width] for i in range(0, len(canvas), width)]
    return canvas