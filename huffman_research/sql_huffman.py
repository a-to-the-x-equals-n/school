from huffman import HuffmanCoding
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.types import LargeBinary, Text
from pathlib import Path
import os
import gc
import json
import subprocess
from util import load_vars



class HuffmanSql(HuffmanCoding):
    """
    A class derived from HuffmanCoding that adds functionality to interact with SQL databases.
    This class can be used to store and retrieve Huffman-encoded data from a database.
    """
    def __init__(self, path, db_URL, huff_URL):
        """
        Initialize the Huffsql class by initializing the superclass HuffmanCoding with a path,
        and setting up database engines for operations.
        """
        super().__init__(path) # Initialize the base class with the path
        self.engine = create_engine(db_URL)  # Engine for the database where raw data might be stored
        self.huff_engine = create_engine(huff_URL)  # Engine for the database to store compressed data
        self.table = ''
        self.huff_table = ''



    def __del__(self):
        """
        Explicitly handle the cleanup of resources by dropping tables from their respective databases.
        """
        try:
            # Drop the main table from the main database
            with self.engine.connect() as conn:
                conn.execute(f"DROP TABLE IF EXISTS {self.table}")
            print(f"Table {self.table} has been removed.")

        except Exception:
            print(f"No table named {self.table} currently exists.")

        try:
            # Drop the Huffman compressed table from the Huffman database
            with self.huff_engine.connect() as conn:
                conn.execute(f"DROP TABLE IF EXISTS {self.huff_table}")
            print(f"Table {self.huff_table} has been removed.")

        except Exception:
            print(f"No table named {self.huff_table} currently exists.")
    



    ''' Creating SQL tables '''


    def csv_to_table(self, chunk = 5000):
        """
        Reads a CSV file in chunks if it's large and uploads each chunk to the specified SQL table.

        Args:
            chunk (int): Number of rows per chunk.
        """
        # Calculate the file size in megabytes
        file_size_mb = os.path.getsize(self.path) / (1024 * 1024)

        # Get table name
        self.table = Path(self.path).stem # The stem property returns the file name without the suffix
        
        try:
            # Determine if the file should be read in chunks
            if file_size_mb > 20:
                print(f"File size is {file_size_mb:.2f} MB, reading and uploading in chunks.")

                for chunk in pd.read_csv(self.path, chunksize = chunk):
                    chunk.to_sql(name=self.table, con=self.engine, if_exists='append', index=False)

                    print("Uploaded a chunk to the database.")
            else:
                print(f"File size is {file_size_mb:.2f} MB, reading the entire file and uploading.")

                data = pd.read_csv(self.path)
                data.to_sql(name=self.table, con=self.engine, if_exists='replace', index=False)

                print("Uploaded the entire data to the database.")

        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")



    def sample_csv_to_table(self, max = 500):
        """
        Reads a maximum of 500 rows from a CSV file and uploads them to the specified SQL table.

        Args:
            max (int): Maximum number of rows to read.
        """
        
        # Get table name from the file path
        self.table = f'{Path(self.path).stem}_sampled'  # The stem property returns the file name without the suffix 
        path = f'sampled/{self.table}.csv'
        try:
            # Read only the first 'max_rows' rows from the CSV file
            data = pd.read_csv(self.path, nrows = max)
            
            
            # Upload the data to the SQL database
            data.to_sql(name = self.table, con = self.engine, if_exists='replace', index=False)

            # Save the sampled data to a CSV file in the same directory as the original
            data.to_csv(path, index=False)
            
            print(f"L121 : SAMPLE_CSV_TO_TABLE : Uploaded {max} rows of sample data to the database table {self.table}.")

        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")



    def compressed_to_table(self, compressed_data):
        """
        Uploads compressed data to a SQL database table.

        Args:
            compressed_data (pd.DataFrame): The DataFrame containing compressed data and metadata.

        Raises:
            SQLAlchemyError: If there is an issue with database connection or SQL execution.
        """
        # Define the table name where the compressed data will be stored.
        self.huff_table = f'{self.table}_compressed'
        
        # Define column data types dynamically based on DataFrame structure
        # Assuming all columns except the last two are byte arrays
        dtype_dict = {col: LargeBinary for col in compressed_data.columns[:-1]}

        # Add the data types for the last two columns which are metadata JSON strings
        dtype_dict.update({compressed_data.columns[-1]: Text}) # 'reverse_mapping' column

        for col in compressed_data.columns[:-1]:  # Exclude metadata columns
            if not isinstance(compressed_data[col].iloc[0], bytes):
                compressed_data[col] = compressed_data[col].apply(lambda x: x if isinstance(x, bytes) else str(x).encode())

        try:
            # Upload the DataFrame to the SQL database, replacing any existing data in the table.
            compressed_data.to_sql(
                name=self.huff_table,
                con=self.huff_engine,
                if_exists='replace',
                index=False,
                dtype=dtype_dict  # specify column data types here
            )
            print("L160 : COMPRESSED_TO_TABLE : Uploaded the entire data to the database.")

        except SQLAlchemyError as e:
            # Handle potential errors during the upload process and print an error message.
            print(f"An error occurred: {e}")


    def to_table(self, data):
        
        try:
            # Upload the DataFrame to the SQL database, replacing any existing data in the table.
            data.to_sql(name = self.table, con =self.engine, if_exists='replace', index=data.index)
            print("L160 : COMPRESSED_TO_TABLE : Uploaded the entire data to the database.")

        except SQLAlchemyError as e:
            # Handle potential errors during the upload process and print an error message.
            print(f"An error occurred: {e}")


    ''' Fetching SQL tables '''


    def fetch_all(self):
        """ Fetches all data from the specified table and returns it as a DataFrame. """

        query = f"SELECT * FROM {self.table}"

        try:
            data = pd.read_sql(query, self.engine)
            print("L179 : FETCH_ALL : Data fetched successfully.")

            return data
        
        except SQLAlchemyError as e:
            print(f"An error occurred while fetching data: {e}")


    def fetch_all_compressed(self):
        """ Fetches all data from the specified table and returns it as a DataFrame. """

        query = f"SELECT * FROM {self.huff_table}"

        try:
            data = pd.read_sql(query, self.huff_engine)
            
            for col in data.columns[:-1]:  # Exclude metadata columns
                if not isinstance(data[col].iloc[0], bytes):
                    print(f"L205 : FETCH_ALL_COMPRESSED : Data type issue in column: {col}")
                    return data
            print("L198 : FETCH_ALL : Data fetched successfully.")
            return data
        
        except SQLAlchemyError as e:
            print(f"An error occurred while fetching data: {e}")

        


    ''' Huffman compression on SQL tables '''


    def compress(self, data):
        """
        Compresses each column of the DataFrame, stores the compressed data back into the DataFrame,
        and saves the Huffman encoding metadata as JSON.

        Args:
            data (pd.DataFrame): The DataFrame containing the data to be compressed.
        """
        reverse_mappings = {}  # Initialize an empty dictionary to store all reverse mappings

        # Create a temporary DataFrame to store binary data
        binary_data = pd.DataFrame(index=data.index)

        # Iterate over columns to compress data.
        for column in data.columns:

            # Compress each column using Huffman encoding and store the results.
            binary_data[column] = self.compress_column(data[column])

            reverse_mappings[f'{column}_reverse_mapping'] = self.reverse_mapping  # Store each column's mapping
            self.reset_attrs()  # Clear Huffman tree and mappings


        # Serialize and store all reverse mappings as JSON in a new column
        binary_data['reverse_mapping'] = json.dumps(reverse_mappings)

        # Return resources from this larger df
        del data
        gc.collect() # Force garbage collector

        return binary_data



    def compress_column(self, column):
        """
        Compress a single column of data using Huffman encoding and return the compressed data.

        Args:
            column (pd.Series): A pandas Series representing a single column of data to be compressed.

        Returns:
            b_col (bytearray): An array containing the compressed data (bytes).
        """

        # Convert the entire column to a single string to facilitate Huffman compression.
        text = ''.join(column.astype(str)).rstrip() # Strip any trailing whitespace characters from the end of the text.
        frequency = self.make_frequency_dict(text) # Build the frequency dictionary from the text.

        self.make_heap(frequency) # Create a priority queue (min-heap) from the frequency dictionary.
        self.merge_nodes() # Merge nodes in the heap until only one remains; this is the root of the Huffman tree.
        self.make_codes() # Generate Huffman codes from the Huffman tree.
        
        b_col = column.apply(lambda x: self.compress_row(str(x)))
        
        return b_col


    
    def compress_row(self, row):
        """
        Compress a single row of data using the Huffman encoding scheme.

        Args:
            row (str): The text of the row to be compressed.

        Returns:
            bytearray: The compressed data as a byte array.
        """
        # Encode the text using the Huffman codes previously generated.
        # This function maps the characters in the row to their corresponding codes.
        encoded_text = self.get_encoded_text(row)
        # Pad the encoded text to ensure its length is a multiple of 8 bits
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        # Convert the padded encoded text into a byte array.
        b = self.get_byte_array(padded_encoded_text)

        return b



    def reset_attrs(self):
        """Reset the Huffman tree and mappings."""
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
    



    ''' Huffman decompression on SQL tables '''
     

    def decompress(self, compressed_data):
        """
        Decompresses all data in the DataFrame using stored Huffman encoding metadata.

        Args:
            compressed_df (pd.DataFrame): DataFrame containing the compressed data and metadata.

        Returns:
            pd.DataFrame: DataFrame with decompressed data.
        """
        # Initialize a DataFrame to store decompressed data
        decompressed_data = pd.DataFrame(index = compressed_data.index)

        # Load the reverse mapping for this column
        reverse_mapppings = json.loads(compressed_data.at[0, 'reverse_mapping'])
        
        # Iterate over each column in the compressed DataFrame (skip metadata columns)
        for column in compressed_data.columns[:-1]:  # The last two columns are always 'codes' and 'reverse_mapping'

            # Load the reverse mapping for this column
            map = reverse_mapppings[f'{column}_reverse_mapping']

            # Decompress each cell in the column using the loaded reverse mapping
            decompressed_data[column] = compressed_data[column].apply(lambda x: self.decompress_helper(x, map))

        return decompressed_data



    def decompress_helper(self, compressed_col, reverse_map):
        """
        Decompresses binary data for a single column using the reverse mapping metadata.

        Args:
            compressed_col (bytes): The compressed column as a byte array.
            reverse_map (dict): Huffman reverse mappings used for decoding.

        Returns:
            str: The decompressed text.
        """

            # Check and convert memoryview to bytes if necessary
        if isinstance(compressed_col, memoryview):
            compressed_col = compressed_col.tobytes()

        assert_text = "L352 : DECOMPRESS_HELPER : Type of compressed_col:", type(compressed_col)  # Debugging output
        assert isinstance(compressed_col, bytes), assert_text

        bit_string = ''
        # Convert bytes to bit string
        for byte in compressed_col:
            bits = bin(byte)[2:].rjust(8, '0')  # Convert byte to a binary string, padding to 8 bits
            bit_string += bits

        # Remove padding from the bit string to get the pure encoded text
        encoded_text = self.remove_padding(bit_string)

        # Set up Huffman tree or use reverse_mapping to decode the text
        self.reverse_mapping = reverse_map  # Assuming the parent class can use this directly
        decompressed_text = self.decode_text(encoded_text)

        return decompressed_text




    ''' Export database tables '''


    def export_as_sql(self, db, table, user,  host = 'localhost', port = 5432):
        """
        Exports a specific table to an SQL file using pg_dump.

        Args:
            table_name (str): The name of the table to export.
            output_path (str): The file path where the SQL dump should be saved.
        """
        output_path = f'datasets/{table}.sql'

        # Command to run pg_dump for a specific table
        command = [
            "pg_dump",
            "--table", table,
            "--file", output_path,
            "--username", user,
            "--host", host,
            "--port", str(port),
            db
        ]

        # Run the command using subprocess
        try:
            subprocess.run(command, check=True)
            print(f"Table {table} has been successfully exported to {output_path}.")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while exporting the table: {e}")



    def export(self, table):
        """
        Exports a table from the SQL database to a CSV file.

        Args:
            table_name (str): The name of the table to export.
            output_path (str): The file path where the CSV should be saved.
            engine (URL): the database you wish to connect to.
        """
        output_path = f'{table}_decompressed.csv' if table in self.table else f'{table}.bin'
        engine = self.engine if table in self.table else self.huff_engine

        # Connect to the database and download the table content into a DataFrame
        with engine.connect() as connection:
            df = pd.read_sql_table(table, con=connection)

        

        # Save the DataFrame to a CSV file
        df.to_csv("sampled/" + output_path, index=False)
        print(f"L390 : EXPORT_AS_CSV : Table {table} has been successfully exported to {output_path}.")



if __name__ == "__main__":
    """
    This block is the starting point of the script when it's run as the main program.
    It initializes the HuffmanSql compression process for a specified file.
    It exports the inital csv file as an sql table, then compresses the data.
    The compressed data is then exported as an bin file.

    With the compressed and non compressed data in csv file format, overall size can be compared.
    """
    # Define the path to the text file that will be compressed.
    path = "test_data/fraud_test.csv"

    # Load url engines from environment variables
    url, huff_url = load_vars("DATABASE_URL", "HUFF_DB_URL")
    
    # Create an instance of HuffmanSql
    h = HuffmanSql(path, url, huff_url)

    h.sample_csv_to_table() # Load source file and store as db table
    data = h.fetch_all() # Fetch new db table

    binary_data = h.compress(data) # Compress new table
    h.compressed_to_table(binary_data) # Store compressed table in db
    h.export(h.huff_table) # Export compressed table as bin file from db

    binary_table = h.fetch_all_compressed()
    decompressed_table = h.decompress(binary_table)
    h.to_table(decompressed_table)
    h.export(h.table)


    # clean up
    del h # WARNING : deletes all tables (if they exist) in both the 'url' and 'huff_url' databases
    gc.collect()