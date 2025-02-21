from typing import Generator
from pathlib import Path
import inspect


def _train(h: list[str]) -> Generator[str, None, None]:
    '''
    Generates backoff n-grams for a given sequence.
    
    Parameters:
    -----------
    h : list of str
        A sequence of words representing an (n-1)-gram history.

    Yields:
    -------
    str
        A space-separated string representing an n-gram, progressively backed off.
        The final yield is an empty string (''), indicating no context.
    
    Example:
    --------
    >>> list(_train(["the", "quick", "brown"]))
    ['the quick brown', 'the quick', 'the', '']
    '''

    if not h: 
        yield ''
        return
    yield ' '.join(h)
    yield from _train(h[:-1])


def _path(f: str | Path, dir: str | Path = Path.cwd()) -> Path:
    """
    Searches for a file by name recursively from a given directory.

    Parameters:
    -----------
    f : str or Path
        The name of the file to search for.
    dir : str or Path, optional
        The directory to start searching from (default: current working directory).

    Returns:
    --------
    Path
        The absolute path of the found file.
    """

    assert dir is Path or dir is str, f'\n\n[INVALID ARGS]: \n\tFunction only accepts type str or Path for <dir> arg.\n\n[INSPECT]:\n\t{_path.__name__}{inspect.signature(_path)}\n'
    
    if isinstance(dir, str):
        dir = Path(dir)
       
    for path in dir.rglob(f): # recursively searches for the file
        return path.resolve() # kicks back first match

    raise FileNotFoundError(f"\"I'm sorry Dave. I'm afraid I can't find '{f}' in {dir}\"\n - HAL 9000")



def _dir() -> Path:
    '''
    Returns the absolute path of the current script's directory.

    If the script is running as a standalone file, it resolves the directory
    of the script using `__file__`. If `__file__` is not available, it falls back to 
    the current working directory.

    Returns:
    --------
    Path
        A `Path` object representing the directory path.

    Source:
    -------
    https://www.youtube.com/@CodingIsFun
    https://www.youtube.com/watch?v=OLrC4J2-pvk&t=15s
    '''
    dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    return dir