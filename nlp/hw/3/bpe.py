from pathlib import Path
from typing import TypeAlias
import re
import functools


def track(*, bugs = False):

    # if imported, ignores any `track` decorators
    if __name__ != '__main__':
        return lambda func: func
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if bugs:
                print(f'ENTERING {func.__name__}...')
            result = func(*args, **kwargs)
            if bugs:
                print(f'EXITING {func.__name__}...')
            return result
        return wrapper
    return decorator


_EOW = '_eow_'
_REP = '_rep_'

TOKEN_REGEX = re.compile(
    r'''
    # emails
    [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}|
    # URLs
    http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|
    # words with apostrophes
    \w+'\w+|
    # general words
    \w+|
    # any non-whitespace character
    [^\w\s]''',
    re.VERBOSE | re.UNICODE,
)

class BPE:
    '''
    Byte Pair Encoding (BPE) Tokenizer for subword tokenization.

    Processes text at the byte level.
    '''
    # byte-based sequences
    _BytesLike: TypeAlias = list[bytes] | list[bytearray]

    def __init__(self, fname: str | Path, rlines: int = 4000, lower: bool = False, verbose: bool = False, *replace: list[str]):
        '''
        Initializes the BPE tokenizer.

        Parameters:
        ----------
        fname : str | Path
            Path to the corpus file.

        rlines : int, optional
            The number of lines to read from the corpus (default: 4000).

        lower : bool, optional
            If True, converts the corpus to lowercase.

        verbose : bool, optional
            If True, enables debug mode, tracking intermediate steps.

        *replace : list[str]
            Custom characters to replace with `_REP`.

        Attributes:
        ----------
        vb : bool
            Debug mode flag (set by `verbose`).

        char_level : list, optional
            Stores character-level tokenization (only if `verbose` is True).

        word_level : list, optional
            Stores word-level tokenization (only if `verbose` is True).

        bigrams : tuple[tuple[str, str], int], optional
            Stores tracked bigram counts (only if `verbose` is True).

        flattened : str, optional
            Flattened string representation of the corpus (only if `verbose` is True).

        _DIR : Path
            Root directory for storing tokenizer-related files.

        _TOKEN_DIR : Path
            Directory where tokenized files are stored.

        _TOKEN_PATH_STEM : Path
            Base path for token files (excluding extensions).

        _case : bool
            If True, corpus text is converted to lowercase.

        _replace : tuple
            Characters specified for replacement.

        rules : dict
            Dictionary of learned BPE merge rules.

        corpus_txt : str
            Raw corpus text after reading `rlines` lines.

        corpus : list[list[str]]
            Preprocessed and tokenized corpus at the character level.

        vocab : set[str]
            Set of unique characters in the corpus.
        '''

        # BUG SPRAY
        self.vb = verbose 
        if self.vb:
            self.char_level = []
            self.word_level = []
            self.bigrams = []
            self.flattened = ''


        
        # FILE NAMES
        from util import _dir
        self._DIR = _dir() 
        self._TOKEN_DIR = self._DIR / f'bpe'
        self._TOKEN_PATH_STEM = self._TOKEN_DIR / Path(fname).stem


        # PREPROCESSING FLAGS
        self._case = lower
        self._replace = replace
        

        # ENCODING ATTRS
        self.rules = {}                                
        self.corpus_txt = self._read(fname, n = rlines)                     # corpus as text
        self.corpus = self._preprocess(self.corpus_txt)                     # tokenize corpus                      
        self.vocab = set(char[0] for word in self.corpus for char in word)  # unpacks to char-level
        


    def _preprocess(self, corpus: str, /) -> list[list[list[str]]]:
        '''
        Tokenizes and normalizes the corpus into character-level tokens.

        Parameters:
        ----------
        corpus : str
            The raw text corpus to be processed.

        Returns:
        -------
        list[list[list[str]]]
            A nested list of character-level tokens, where:
            - Each outer list represents a word.
            - Each inner list represents a character (including `_eow_` markers).
            - Each character is wrapped in a list to preserve structure.
        '''

        # PREPROCESS
        if self._case:
            corpus = corpus.lower()

        # clean
        # standardize whitespace symbols
        corpus = re.sub(r'\s+', ' ', corpus) # replace multiple spaces with a single space

        # replace any user-defined characters
        for u in self._replace:
            corpus = re.sub(rf'{u}', rf'{_REP}', corpus)


        # PRETOKENIZE
        # using re pattern, return corpus segmented by words
        segments = TOKEN_REGEX.findall(corpus)
        '''
        SEGMENTED WORDS EXAMPLE
        =======================
        hindered,
        by,
        some,
        problem
        '''
        
        # convert segments to word-level tokens
        # append '_eow_'
        words = [[' '.join([*word] + [_EOW])] for word in segments]
        '''
        WORD-LEVEL TOKEN EXAMPLE
        ========================
        ['h i n d e r e d _eow_']
        ['b y _eow_']
        ['s o m e _eow_']
        ['p r o b l e m _eow_']
        '''

        # convert word-level tokens with '_eow_' to character-level tokens
        chars = [[char for char in word[0].split(' ')] for word in words]
        '''
        CHAR-LEVEL TOKEN EXAMPLE
        ========================
        ['P', 'r', 'a', 'g', 'u', 'e_']
        ['S', 't', 'o', 'c', 'k', '_eow_']
        ['M', 'a', 'r', 'k', 'e', 't', '_eow_']
        ['f', 'a', 'l', 'l', 's', '_eow_']
        ['t', 'o', '_eow_']
        '''
        
        self.word_level = words
        self.char_level = chars
        self.flattened = ' '.join(ch for word in self.word_level for ch in word)
        '''
        FLATTENED EXAMPLE
        =================
        e n d a n g e r i n g _eow_ t h e _eow_ s t a b i l i t y _eow_ o f _eow_ t h e _eow_ e n t i r e _eow_ s y s t e m _eow_
        '''

        return chars


    @track(bugs = False)
    def _frequency(self, /) -> tuple[str, str]:
        '''
        Identifies the most frequent adjacent token pair (bigram).

        Returns:
        --------
        [tuple[str, str]
            The most frequent bigram.
        '''

        from collections import Counter

        # counter object is probably more efficient than how I'd iterate through counts
        bigrams = Counter(
            (word[i], word[i + 1])    # char-level 
            for word in self.corpus         # word-level (designated by '_eow_')
            for i in range(len(word) - 1)   
        )

        # returns the most frequent (best) bigram
        best, rank = bigrams.most_common(1)[0]
        if self.vb:
            print(f'\n\t[BEST] {best} [RANK] {rank}')

        # sanity stuff
        self.freq = bigrams
        self.best = best, rank

        return best, rank # kicks back the best pair to be tokenized

    
    
    def _read(self, fname: str | Path, /, *, n: int) -> str:
        '''
        Reads a limited number of lines from the corpus file and converts it to a _ByteStr.

        Parameters:
        -----------
        fname : str | Path
            File path/name to the corpus.

        n : int
            - If `n > 0`, reads the first `n` lines.
            - If `n < 0`, reads the last `|n|` lines.
        '''

        from util import _path
        fpath = _path(fname) 

        if n < 0:
            # read file in reverse using deque
            from collections import deque
            with fpath.open('rb') as f:
                lines = deque(f, maxlen = abs(n)) # read last n lines
        else:
            with fpath.open('rb') as f:
                lines = [f.readline() for _ in range(n)] # reads n lines in bytes

        return b''.join(lines).decode('utf-8', errors = 'replace') # convert joined bytes to _ByteStr


    @track(bugs = True)
    def _merge(self, pair: tuple[str, str], token: str) -> list[list[list[str]]]:
        '''
        Merges the most frequent token pair in the corpus.

        Parameters:
        -----------
        pair : tuple[str, str]
            The most frequent bigram.

        token : str
            Tokenized pair.

        Returns:
        --------
        list[list[list[str]]]
            The updated tokenized corpus, where each word is a list of character tokens.
        '''

        corpus = []

        for word in self.corpus:
            tokens = []
            i = 0

            if self.vb:
                print(f"\n\t[WORD] '{' '.join(char for char in word)}'")
                
            # update char-level tokens with new merges
            while i < len(word) - 1:

                if self.vb: print(f'\n\t\t[COMPARING] {(word[i], word[i + 1])} & {pair}')

                if (word[i], word[i + 1]) == pair:
                    
                    if self.vb: print(f'\n\t\t\t[MATCHED] {(word[i], word[i + 1])} & {pair}')
                    tokens.append(token)     # sub in new token
                    i += 2    
                                    
                else:
                    tokens.append(word[i])
                    i += 1

            # append last char-level token (if needed)
            if i == len(word) - 1:
                tokens.append(word[-1])

            # append the merges at the word-level
            corpus.append(tokens)

        return corpus  # return updated corpus


    @track(bugs = False)
    def iterate(self, iters: int = 1, /) -> None:
        '''
        Performs BPE iterations to merge the most frequent adjacent token pairs.

        Parameters:
        -----------
        iters : int, optional
            The number of merge iterations to perform (default: 1).

        Returns:
        --------
        None
            Updates the internal corpus, vocabulary, and merge rules in place.
        '''

        for _ in range(iters):
            best, _ = self._frequency()            # find most frequent bigram
            token = ''.join(best)                  # tokenize best bigram pair

            if self.vb:
                print(f'\n\t[BEST] {best} TOKEN {token}')

            self.corpus = self._merge(best, token) # update corpus with new token
            self.rules[best] = token               # store merge rule
            self.vocab.add(token)                  # add new token to vocab
    

    @track(bugs = False)
    def train(self, *, min_freq: int = 2) -> None:
        '''
        Runs the BPE training loop, merging the most frequent bigram until `min_freq` is reached.

        Parameters:
        -----------
        min_freq : int, optional
            The minimum bigram frequency to halt training (default: 2).

        Returns:
        --------
        None
            Updates the internal corpus, vocabulary, and merge rules in place.
        '''

        # iteration scatterplot data (necessary for hw assignment)
        self.x = []
        self.y = []

        while True:

            self.x.append(len(self.vocab))                         # track vocab size
            self.y.append(sum(len(word) for word in self.corpus))  # track corpus size

            best, rank = self._frequency()  # find most frequent bigram
            if rank <= min_freq:
                break

            token = ''.join(best)                  # tokenize pair
            self.corpus = self._merge(best, token) # update corpus

            self.rules[best] = token  # store merge rule
            self.vocab.add(token)     # add new token to vocab
    

    def save(self, fname: str | Path = None, /) -> None:
        '''
        Writes BPE rules and vocab to JSONs.

        Parameters:
        -----------
        fname : str | Path, optional
            The filename or file path where the model should be saved.
            If not provided, defaults to `self._TOKEN_PATH_STEM`.
        '''

        import json
        if not fname:
            # convert to type string for easier manipulation
            fname = str(self._TOKEN_PATH_STEM)
        else: 
            fname = str(self._TOKEN_DIR / Path(fname).stem)

        # creates parent dir if it doesn't already exist
        self._TOKEN_DIR.mkdir(parents = True, exist_ok = True)

        vocab_path = Path(fname + f'_VOCAB.json')
        rules_path = Path(fname + f'_RULES.json')

        rules = [(list(k), v) for k, v in self.rules.items()]   # convert tuple keys to lists
        vocab = sorted(self.vocab)                              # set to list for json compatibility

        with open(vocab_path, 'w', encoding = 'utf-8') as f:
            json.dump(vocab, f, ensure_ascii = False, indent = 2)

        with open(rules_path, 'w', encoding = 'utf-8') as f:
            json.dump(rules, f, ensure_ascii = False, indent = 2)


    def pretrained(self, dir: str | Path = None, /) -> None:
        '''
        Loads pretrained merge rules and vocabulary from JSON files.

        Parameters:
        -----------
        dir : str | Path, optional
            Directory containing the pretrained model files.
            If not provided, defaults to `self._TOKEN_PATH_STEM`.

        Returns:
        --------
        None
            Updates `self.vocab` and `self.rules` with loaded data.
        '''

        import json
        if not dir:
            vocab_path = Path(str(self._TOKEN_PATH_STEM) + f'_VOCAB.json')
            rules_path = Path(str(self._TOKEN_PATH_STEM) + f'_RULES.json')
        else:
            dir = self._DIR / Path(dir)
            vocab_path = list(dir.glob('*_VOCAB.json'))[0]
            rules_path = list(dir.glob('*_RULES.json'))[0]

            if not vocab_path or not rules_path:
                raise FileNotFoundError(f"\"I'm sorry Dave, I can't find {dir}\".\n\t -Hal 9000")
            
        # load vocab
        with open(vocab_path, 'r', encoding = 'utf-8') as f:
            self.vocab = set(json.load(f))

        # load merge rules
        with open(rules_path, 'r', encoding = 'utf-8') as f:
            self.rules = {tuple(k): v for k, v in json.load(f)}


    def sanity(self, field: str, /, *, k: int = 0) -> None:
        '''
        Displays a preview of the specified attribute in a structured format.

        Parameters:
        -----------
        field : str
            The name of the attribute to display.

        k : int, optional
            The number of items to display. If 0, prints all.

        Returns:
        --------
        None
            Prints the selected attribute in a readable format.
        '''

        attr = getattr(self, field, None)
        print(f"\n--{field.upper()}--")

        # VOCAB (set)
        if 'vocab' == field:
            vocab = sorted(self.vocab, key = lambda x: -len(x))
            print(f'=========')
            for token in vocab[-k:]:
                print(f"{repr(token)}")
            print()
            return

        # COUNTS (Counter)
        if field == 'freq':
            rules = self.freq.most_common(k)
            print(f"{'PAIRS':>10}{'COUNTS':>13}")
            print("=" * 27)
            for k, v in rules:
                print(f"{repr(k):>14}  |{v:>5}")
            print()
            return
        
        # CORPUS (list)
        if 'corpus' == field:
            print('============')
            for word in self.corpus[-k:]:
                print(word)
            print()
            return

        # RULES (dict)
        if 'rules' == field:
            print('============')
            rules = sorted(self.rules.items(), key = lambda x: -len(x[1]))
            for item in rules[-k:]:
                print(item)
            print()
            return


        # just print whatever it is
        print('**=========')
        print(attr)
        print()


    def tokenize(self, fname: str | Path, /, *, rlines = -1000, level: str = 'word', pretrained: bool = False) -> list | str:
        '''
        Applies the trained BPE rules to a new text sample.

        Parameters:
        -----------
        fname : str | Path
            File path/name to the corpus.

        rlines : int, optional
            The number of lines to read. Default is -1000 (last 1000 lines).

        level : str, optional
            The tokenization level of the output:
            - `'char'`: Returns character-level tokens as `list[list[list[str]]]`.
            - `'word'` (default) : Returns word-level tokens as `list[list[str]]`.
            - `'flat'`: Returns a fully flattened string representation.

        Returns:
        --------
        list[list[list[str]]] | list[list[str]] | str
            The tokenized corpus:
            - Character-level if `level='char'`.
            - Word-level if `level='word'`.
            - Flattened string if `level='flat'`.
        '''

        if not self.rules or pretrained:
            self.pretrained()

        # read, clean and pretokenize corpus
        corpus = self._read(fname, n = rlines)
        self.corpus = self._preprocess(corpus)

        # apply learned BPE merge rules
        for pair, token in self.rules.items():
            self.corpus = self._merge(pair, token)

        ''' TO WORD LEVEL FROM CHAR LEVEL '''
        self.to_word_level = [[' '.join(word)] for word in self.corpus if word]

        ''' To FLATTENED FROM WORD LEVEL '''
        self.to_flattened = ' '.join(word[0] for word in self.to_word_level)

        if 'flat' in level:
            return self.to_flattened
        elif 'word' in level:
            return self.to_word_level
        else:
            return self.corpus



if __name__ == '__main__':

    # init BPE
    bpe = BPE('BPE-data.txt', rlines = -10)

    bpe.pretrained()
    w = bpe.tokenize('BPE-data.txt', rlines = -10)
    # print(bpe.to_flattened[:100])
    print(bpe.corpus)


    # for t in bpe.to_word_level[:30]:
    #     print(t)
    # for _ in range(12):
    #     bpe.iterate()
    #     # bpe.sanity('best')
    #     bpe.sanity('rules')
    #     bpe.sanity('vocab')
    #     # bpe.sanity('freq', k = 1)
    #     # bpe.sanity('vocab')

    # bpe.sanity('corpus', k = 15)


