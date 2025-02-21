# <font color = #6fde6f> Cryptoanalysis Assignment </font>

This project explores methods for cracking a classical ciphers using Python and character statistics.

The <font color = #296649>**Shift Cipher**</font> was solved by a brute force approach.  

The <font color = #296649>**Substitution Cipher**</font> was solved by visualizing ngram data and making informed deductions.

<font color = ##c78728>*...with A LOT of trial and error...*</font>


## <font color = #6fde6f>Files</font>

- `decrypt_hw.ipynb` : Jupyter notebook showcasing the techniques and code used to break the ciphers.
- `util.py` : helper functions.
- `Makefile` : automates env setup and dependencies.
- `data/bigram_matrix.csv` : the frequencies of character bigrams transcribed from [English-Stats.pdf](https://ecu.instructure.com/courses/145373/files/16492685?module_item_id=4721826) to a `.csv`.


## <font color = #6fde6f> Quick Setup </font>


> **NOTE:** *Since Makefile runs each command in a new shell session, it gets weird because you would normally have to  **reactivate** the venv with each* `make <command>`.   
>  
>*This Makefile avoids the issue by directly calling the Python binary that's copied into the venv from* `make start`.  

### <font color = #6fde6f> Makefile </font>

```bash
make start    # sets up virtual env
make reqs     # installs dependencies w/ requirements.txt
make notebook # (optional) open in Jupyter
make end      # clean up
```

## <font color = #6fde6f>Requirements</font>
- Python3
- NumPy
- Jupyter  *(optional)*
