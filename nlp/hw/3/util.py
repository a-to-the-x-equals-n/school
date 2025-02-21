from pathlib import Path
from typing import TypeVar

def _dir() -> Path:
    '''
    Returns the absolute path of the current script's directory.
    NOTE: The path resolution ensures compatibility with Jupyter environments

    Returns:
    --------
    Path
        A `Path` object representing the directory path.

    Source:
    -------
    Adapted from: https://www.youtube.com/watch?v=OLrC4J2-pvk&t=15s
    NOTE: "__file__" doesn't exist at the local scope; 'locals' should be 'globals'
    '''

    # returns directory where THIS script is physically located
    # or returns the directory of the CALLER
    dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    return dir


_PathLike = TypeVar('_PathLike', str, Path)
def _path(file: _PathLike, /, *, dir: _PathLike = _dir()) -> Path:
    '''
    Searches for a file by name recursively from a given directory.

    Parameters:
    -----------
    file : _PathLike
        The name of the file to search for.

    dir : _PathLike, optional
        The directory to start searching from (default: current working directory).

    Returns:
    --------
    Path
        The absolute path of the found file.
    '''
    
    if isinstance(dir, str):
        dir = Path(dir)

    if isinstance(file, Path):
        file = str(file)
        
    for path in dir.rglob(file): # recursively searches for the file
        return path.resolve() # kicks back first match
    
    raise FileNotFoundError(f"\n\n\t\"I'm sorry Dave. I'm afraid I can't find '{file}' in '{dir}'\"\n\t\t   - HAL 9000\n")