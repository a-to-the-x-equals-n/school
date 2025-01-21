import numpy as py
import pandas as pd
import os
from pathlib import Path



# Finds the absolute path
ABSOLUTE_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


# calculate entropy
def entropy(data):

    # Calculate the frequency of each class label in the target column
    levels = dict(data[data.columns[-1]].value_counts())

    # Total number of instances
    n = data.iloc[:,-1].size

    # Calculate entropy using the formula
    return -1 * sum([(levels[x] / n) * py.log2((levels[x]/ n)) for x in levels.keys()])

# Function to calculate remainder
def remainder(feature, data):

    # Calculate the frequency of each value in the feature column
    levels = dict(feature.value_counts())

    # Extract the target feature column
    target = data.iloc[:,-1]

    # Total number of instances (rows)
    n = feature.size

    # Creates a partitioned data set with only the current feature column with the target column
    partitioned_data = pd.DataFrame({'d': feature, 't': target})

    # Calculate the remainder
    return sum((levels[x] / n ) * entropy(partitioned_data[partitioned_data['d'] == x]) for x in levels.keys())



# Information gain
def IG(feature, data):
    return entropy(data) - remainder(feature, data)


# Main function
def main():

    # Get the absolute path to the file
    filepath = ABSOLUTE_PATH / "vampire_data.csv"

    # Load the dataset
    vampires = pd.read_csv(filepath)


    # --EXAMPLE OUTPUT FOR TESTING--

    # Iterate through each column -- except the last column which is the target feature
    for column in vampires.columns[:-1]:

    # Print column name and corresponding entropy, remainder, and information gain
        print(f'\nColumn: {column}\nEntropy: {entropy(vampires)}\nRemainder: {remainder(vampires[column], vampires)}\nInfo Gain: {IG(vampires[column], vampires)}\n\n')




if __name__ == "__main__":

    main()
