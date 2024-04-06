# Betweenle Solver

The Betweenle Solver is a Python-based tool that helps you solve the Betweenle word game by finding words between two given words and recommending the best word to guess based on distance and frequency.

I've tested it on 20 games thus far and it consistently gets a perfect score.

## Installation

1. You can pip install the git repo as shown below:

```
> pip install git+https://github.com/llucid-97/betweenle_solver
```

## Usage

This then adds the following command to your python environment:

```
> betweenle_solver
```

The solver will prompt you to enter the following information:

1. The first word
2. The second word
3. (Optional) The estimated distance after the first word
4. (Optional) The estimated distance before the second word

After providing the required information, the solver will display the words between the two given words and recommend the best word to guess based on distance and frequency.

## How the Search Works

The Betweenle Solver uses a combination of binary search, quantile-based selection, and word frequency to find and recommend words between two given words.

1. Binary Search:
   - The solver first performs a binary search on the sorted list of valid words to find the index range between the two given words.
   - If no distance estimates are provided, the solver recommends the middle word within the index range.

2. Quantile-Based Selection:
   - If distance estimates are provided (estimated distance after the first word and before the second word), the solver uses quantile-based selection.
   - The solver normalizes the distance estimates and calculates a target index within the valid words range.
   - It then selects a subset of words around the target index using a quantile range.

3. Word Frequency:
   - The solver uses a pre-computed word frequency distribution based on the Gutenberg corpus.
   - It selects the word with the highest frequency from the quantile-based subset of words.
   - If the quantile-based subset is small, the solver directly recommends the word with the highest frequency.
   - If the quantile-based subset is large and the distance estimates are far apart, the solver performs a quantile bounding to eliminate more words and recommends the word at the appropriate index.
   - If the distance estimates are close together, the solver uses a greedy policy and recommends the word at the target index.

## Theoretical Algorithm Complexity

The theoretical algorithm complexity of the Betweenle Solver can be analyzed as follows:

- Binary Search: The binary search on the sorted list of valid words has a time complexity of O(log n), where n is the number of valid words.

- Quantile-Based Selection: The quantile-based selection involves calculating indices and selecting a subset of words, which has a time complexity of O(1).

- Word Frequency: The word frequency lookup for each word in the quantile-based subset has a time complexity of O(1) on average, assuming the word frequency dictionary has constant-time access.

Therefore, the overall time complexity of the Betweenle Solver is O(log n) for the binary search, plus O(1) for the quantile-based selection and word frequency lookup, resulting in a total time complexity of O(log n).

The space complexity is O(n) to store the list of valid words and the word frequency dictionary.

Note: The actual performance may vary depending on the size of the word list and the efficiency of the dictionary lookup.
