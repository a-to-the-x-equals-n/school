# Python Decision Tree Model

This Python script implements a decision tree model to calculate entropy, remainder, and information gain for a given dataset. The dataset contains features such as "shadow," "pale," "no_garlic," and a target feature "vampire," stored in a CSV file named "vampire_data.csv."

## Requirements

Use `pip` to install the following Python libraries:

```bash
pip install -r requirements.txt
```

- numpy
- pandas

## Usage

Run the `vampire_model.py` script to analyze the dataset and calculate entropy, remainder, and information gain for each feature column. The script automatically loads the dataset from the CSV file and prints the results.

## Functions

### `entropy(data)`

The `entropy` function calculates the entropy of a dataset, which measures the uncertainty or randomness of the target feature.

### `remainder(feature, data)`

The `remainder` function calculates the remainder for a given feature, which represents the amount of uncertainty remaining after partitioning the dataset based on that feature.

### `IG(feature, data)`

The `IG` function calculates the information gain for a given feature, which measures the reduction in entropy achieved by splitting the dataset based on that feature.

# Purpose

### Here's chatGPTs explanation on why this is relevant:

Information gain is a concept used in decision tree algorithms, particularly in the context of feature selection. Its purpose is to quantify the effectiveness of a feature in splitting a dataset into different classes or categories. In other words, information gain helps us determine how much a feature reduces the uncertainty (or entropy) in the dataset when used as a split criterion.

The main purpose of using information gain is as follows:

    Feature Selection: Information gain helps decide which feature to choose at each node of a decision tree. Features with higher information gain are preferred as they provide more discriminatory power to classify instances into different classes.

    Building Decision Trees: In decision tree algorithms like ID3 (Iterative Dichotomiser 3) and C4.5, information gain is used to select the best feature to split the dataset at each node. By recursively selecting features with high information gain, decision trees can efficiently partition the dataset into subsets that are more homogeneous with respect to the target variable.

    Reducing Entropy: Information gain aims to maximize the reduction in entropy (or other impurity measure) achieved by splitting the dataset based on a particular feature. This reduction in entropy corresponds to an increase in the homogeneity of the subsets, making them more suitable for classification.

