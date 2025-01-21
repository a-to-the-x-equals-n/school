import numpy as np
import pandas as pd


def z_score(x: float | np.float32, mu: np.float32, sigma: np.float32) -> np.float32:
    '''
    - x: feature value
    - mu: mean of the feature
    - sigma: std of the feature
    '''
    return (x - mu) / sigma if sigma > 0 else 0



def prob_density_func(x: float | np.floating, data: np.ndarray, dof: int = 1) -> np.float32:
    '''
    Parameters:
    - x: The feature value
    - data: NumPy array of feature data
    '''

    if not isinstance(x, np.floating):
        x = np.float32(x)
    
    mu = np.mean(a = data, dtype = np.float32)
    sigma = np.std(a = data, dtype = np.float32, ddof = dof)
    z = z_score(x, mu, sigma)

    # Returns Gaussian PDF probability
    return 1 / (np.sqrt(2 * np.pi * sigma**2) * np.exp(z**2 / 2))



def bayes_query(data: np.ndarray, query: list, idx: int = 0) -> float:
    '''
    - data: NumPy 2D array (features as columns, samples as rows)
    - features: NumPy array of column indices corresponding to feature columns
    - values: NumPy array of feature values we are conditioning on
    - idx: The current index for recursion (default: 0)
    '''

    if idx >= data.shape[1] - 1: # base case
        return 1.0
    
    val = query[idx]
    current_column = data[:, idx]
    value_count = np.sum(current_column == val)
    total_events = data.shape[0] # number of rows in current recursion step

    # P(X_i | C)
    prob = value_count / total_events if total_events > 0 else 0 # safe division

    if prob == 0:
        return 0 # impossible case; 0% probability
    
    # reduce dataset for the next step
    next_subset = data[data[:, idx] == val]

    print(f"Step {idx}: P(column_{idx}={val}) = {value_count}/{total_events} = {prob:.4f}")

    # probability of observing `query` given a dataset
    return prob * bayes_query(next_subset, query, idx + 1)


if __name__ == "__main__":
    # Sample dataset 
    # [Fever, Cough, Has Disease]
    data = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 0]]
        )

    likelihood = bayes_query(data = data, query = [1, 1])
    print(f"P(Disease | Fever = 1, Cough = 1) = {likelihood:.4f}")

