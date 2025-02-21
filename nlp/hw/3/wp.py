from tokenizers import Tokenizer, trainers
from tokenizers.models import WordPiece as WP
from tokenizers.pre_tokenizers import Whitespace
from pathlib import Path



class WordPiece:

    def __init__(self, fname: str | Path, /, *, rlines: int = 0, vocab_size: int = 4000, min_freq: int = 2) -> None:
        '''
        Initializes the WordPiece tokenizer, loads the dataset, and sets up training parameters.

        Parameters:
        -----------
        fname : str | Path
            Path to the dataset file.

        rlines : int, optional
            The number of lines to read from the corpus. Default is 4000.

        vocab_size : int, optional
            The number of new tokens to be learned and added to the base vocabulary. Default is 4000.

        min_freq : int, optional
            Minimum frequency for a token to be included in the vocabulary. Default is 2.

        Attributes:
        ----------
        tokenizer : Tokenizer
            The core WordPiece tokenizer.
            - Uses '_unk_' as the unknown token, mapping out-of-vocabulary words to '_unk_'.
            - Ensures all processed text is tokenized according to learned subword rules.

        trainer : WordPieceTrainer
            Trainer object responsible for learning subword tokenization rules.
            - `vocab_size` defines the final vocabulary size.
            - `min_frequency` filters out tokens appearing fewer times than this threshold.
            - `special_tokens` includes:
                - 'pad_'    : Padding token for batch processing.
                - '_unk_'   : Unknown token for out-of-vocabulary words.
                - '_cls_'   : Classification token for NLP models.
                - '_sep_'   : Separator token for sentence-pair tasks.
                - '_mask_'  : Mask token used for masked language modeling.
            - `continuing_subword_prefix = "##"` signals that a token is a subword and not a standalone word.

        corpus_txt : str
            Raw corpus text after reading `rlines` lines.

        vocab : set[str]
            Set of unique tokens extracted from the corpus.

        max : int
            Final vocabulary size (`len(vocab) + vocab_size`).
        '''
        
        self.fname = fname
        self.min_freq = min_freq
        self.token_vocab = ['_pad_', '_unk_', '_cls_', '_sep_', '_mask_']
        self.tokenizer = Tokenizer(WP(unk_token = '_unk_'))
        self.tokenizer.pre_tokenizer = Whitespace()
        self.special_tokens = ['_pad_', '_unk_', '_cls_', '_sep_', '_mask_']
        self.tokenizer.add_special_tokens(self.special_tokens)

        self.corpus_txt = self._read(fname, n = rlines)        # load dataset
        self.vocab = set(self.corpus_txt)               # extract tokens
        self.max = len(self.vocab) + vocab_size         # final vocabulary size

        self.trainer = trainers.WordPieceTrainer(
            vocab_size = self.max,
            min_frequency = min_freq,
            special_tokens = self.special_tokens,
            continuing_subword_prefix = "##"
        )

        # for token in special_tokens:
        #     self.tokenizer.model.add_token(token)



    def _read(self, fname: str | Path, /, *, n: int) -> str:
        '''
        Reads a specified number of lines from the dataset and returns the text.

        Parameters:
        -----------
        fname : str | Path
            Path to the dataset file.

        n : int
            - If `n > 0`, reads the first `n` lines.
            - If `n < 0`, reads the last `|n|` lines.
            - If `n == 0`, reads the entire file.

        Returns:
        --------
        text: str
            The extracted text from the dataset.
        '''

        from util import _path
        self.fpath = fpath = _path(fname) 
        self.fpath = str(self.fpath)

        if n < 0:
            # read file in reverse using deque
            from collections import deque
            with fpath.open('r') as f:
                lines = deque(f, maxlen = abs(n))           # read last 'n' lines
        elif n > 0:
            with fpath.open('r') as f:
                lines = [f.readline() for _ in range(n)]    # reads 'n' lines in bytes
        else:
            with open(fpath, 'r', encoding = 'utf-8') as f:
                lines = f.read()                            # read entire file

        text = ''.join(lines)
        return text



    def train(self, iter: bool = True, chunks: int = 100, file_path: str = "BPE-data.txt") -> None:
        '''
        Trains the WordPiece tokenizer on the given dataset.

        Parameters:
        -----------
        file_path : str, optional
            Path to the text dataset. Default is "BPE-data.txt".
        '''
        self.x = []  # Track vocabulary size at each step
        self.y = []  # Track corpus length at each step

        self.tokenizer.add_special_tokens(self.special_tokens)

        if not iter:
            return self.tokenizer.train([str(self.fpath)], self.trainer)
        else:

            lines = self.corpus_txt.split('\n')
            chunk_size = max(1, len(lines) // chunks)

            while True:
                # We have one tokenizer. Merges accumulate each chunk
                for i in range(1, chunks + 1):

                    subset = '\n'.join(lines[: i * chunk_size])
                    # train from this partial subset
                    self.tokenizer.train_from_iterator([subset], self.trainer)
                    # current vocabulary size
                    vocab_size = len(self.tokenizer.get_vocab())
                    self.x.append(vocab_size)
                    # measure how it tokenizes this partial subset, encode 'subset'.
                    tokenized_corpus = [
                        self.tokenizer.encode(text).tokens
                        for text in self.corpus_txt.split('\n')
                    ]
                    self.corpus_length = sum(len(tokens) for tokens in tokenized_corpus)
                    self.y.append(self.corpus_length)
                    # sentinel
                    if vocab_size >= self.max:
                        return
                    self._reset_tokenizer()


    def _reset_tokenizer(self) -> None:
        self.tokenizer = Tokenizer(WP(unk_token = '_unk_'))
        self.tokenizer.pre_tokenizer = Whitespace()
        self.special_tokens = ['_pad_', '_unk_', '_cls_', '_sep_', '_mask_']
        self.tokenizer.add_special_tokens(self.special_tokens)

        self.trainer = trainers.WordPieceTrainer(
            vocab_size = self.max,
            min_frequency = self.min_freq,
            special_tokens = self.special_tokens,
            continuing_subword_prefix = "##"
        )

                

    def save(self, file_path: str = "wp/wp_VOCAB.json") -> None:
        '''
        Saves the trained tokenizer.

        Parameters:
        -----------
        file_path : str, optional
            File path to save the tokenizer model. Default is "wordpiece_tokenizer.json".
        '''

        from util import _dir
        fpath = str(_dir() / Path(f'wp/wp_VOCAB.json'))
        self.tokenizer.save(fpath)



    def pretrained(self, file_path: str = "wp/wp_VOCAB.json") -> None:
        '''
        Loads a pre-trained tokenizer.

        Parameters:
        -----------
        file_path : str, optional
            Path to the saved tokenizer model. Default is "wordpiece_tokenizer.json".
        '''

        from util import _dir
        fpath = str(_dir() / Path(f'wp/wp_VOCAB.json'))
        self.tokenizer = Tokenizer.from_file(fpath)


    def tokenize(self, corpus: str | Path, rlines: int = -1000)-> list[str]:
        '''
        Tokenizes a given text using the trained tokenizer.

        Parameters:
        -----------
        text : str
            Input sentence to tokenize.

        Returns:
        --------
        list[str]
            List of tokenized subwords.
        '''
         
        if '.txt' in corpus:
            corpus = self._read(corpus, n = rlines)
            return self.tokenizer.encode(corpus).tokens
        else:
            return self.tokenizer.encode(corpus).tokens
            
