import math
import pickle
import pickle
from pathlib import Path
from typing import List, Optional, Tuple


def make_fdist(path: str) -> None:
    """
    Create a frequency distribution of words from the Gutenberg corpus and save it to a file.

    Args:
        path (str): The path to save the frequency distribution file.
    """
    import nltk
    from nltk.probability import FreqDist
    from nltk.corpus import gutenberg

    print("Creating word frequency lookup table")
    # Download the Gutenberg corpus (if not already downloaded)
    nltk.download('gutenberg')

    # Load the text corpus
    corpus = gutenberg.words()

    # Create a frequency distribution
    fdist = FreqDist(word.lower() for word in corpus if len(word) == 5)

    # Get the most common words and their frequencies
    most_common = fdist.most_common()

    words = get_word_list()

    wdict = {}
    for w in words:
        wdict[w] = fdist.get(w,1)

    # Save wdict using pickle
    with open(path, 'wb') as file:
        pickle.dump(wdict, file)

def get_word_list(url: str = 'sgb-words.txt') -> List[str]:
    """
    Get the list of valid words from a file or download it from a URL.

    Args:
        url (str, optional): The URL or path to the word list file. Defaults to 'sgb-words.txt'.

    Returns:
        List[str]: The list of valid words.
    """
    path = str(url).split('/')[-1]
    path = Path(__file__).parent / path
    if not Path(path).exists():
        import requests

        url = "https://raw.githubusercontent.com/charlesreid1/five-letter-words/master/sgb-words.txt"
        response = requests.get(url)

        if response.status_code == 200:
            with open(path, "w") as file:
                file.write(response.text)
            print("Downloaded Word List.")
        else:
            raise("Failed to download Word List.")
    
    with open(path, 'r') as file:
        words = file.read().splitlines()
    words = sorted(words)
    return words


def load_word_frequencies(path: str) -> dict:
    """
    Load the word frequencies from a file or create a new frequency distribution if the file doesn't exist.

    Args:
        path (str, optional): The path to the word frequencies file. Defaults to 'word_frequencies.pkl'.

    Returns:
        dict: The word frequencies dictionary.
    """
    if not Path(path).exists():
        make_fdist(path)
    with open(path, 'rb') as file:
        frequencies = pickle.load(file)
    return frequencies

def get_highest_frequency_word(wdict: dict, word_list: List[str]) -> Optional[str]:
    """
    Get the word with the highest frequency from a list of words.

    Args:
        wdict (dict): The word frequencies dictionary.
        word_list (List[str]): The list of words to search.

    Returns:
        Optional[str]: The word with the highest frequency, or None if no words are found.
    """
    max_frequency = 0
    max_frequency_word = None

    for word in word_list:
        frequency = wdict.get(word, 0)
        if frequency > max_frequency:
            max_frequency = frequency
            max_frequency_word = word

    return max_frequency_word

def find_between_words(word1: str, word2: str, word_list: List[str], after_first: Optional[float] = None, before_second: Optional[float] = None) -> Tuple[List[str], int]:
    """
    Find the words between two given words in a word list and recommend a word based on distance and frequency.

    Args:
        word1 (str): The first word.
        word2 (str): The second word.
        word_list (List[str]): The list of valid words.
        after_first (Optional[float], optional): The estimated distance after the first word. Defaults to None.
        before_second (Optional[float], optional): The estimated distance before the second word. Defaults to None.

    Returns:
        Tuple[List[str], int]: A tuple containing the list of valid words between the two given words and the index of the recommended word.
    """
    start_index = word_list.index(word1) if word1 in word_list else 0
    end_index = word_list.index(word2) if word2 in word_list else len(word_list) - 1

    if word1 not in word_list:
        print(f"{word1} not found")
    if word2 not in word_list:
        print(f"{word2} not found")

    assert end_index > start_index, f"{word2} appears to come after {word1}! This breaks my logic. Terminating. Did you enter the words in the right order?"

    valid_words = word_list[start_index+1:end_index]

    if after_first is not None and before_second is not None:
        total_distance = len(valid_words)
        normalized_after_first = after_first / (after_first + before_second)

        quantile_index = int(total_distance * normalized_after_first)
        quantile_start = int(max(0, math.floor(quantile_index - (0.02 * len(valid_words)))))
        quantile_end = int(min(total_distance, math.ceil(1+quantile_index + (0.02 * len(valid_words)))))
        quantile_words = valid_words[quantile_start:quantile_end]
        _path = Path(__file__).parent / 'word_frequencies.pkl'
        word_freqs = load_word_frequencies(str(_path))
        print("Quantile Words:",','.join(quantile_words[:5]),f'[...] (total {len(quantile_words)})' if len(quantile_words)>5 else '')
        print("Loc-Greedy Word:",valid_words[quantile_index])
        freq_greedy=get_highest_frequency_word(word_freqs,quantile_words)
        print("Frequency-Greedy Word: ", freq_greedy )
        freq_idx = valid_words.index(freq_greedy)


        if len(quantile_words)<10:
            target_index = freq_idx
        else:
            if ((after_first > 5*before_second) or (before_second > 5* after_first)):
                print("Keys are far apart! Doing a quantile bounding")
                # Choose the one that eliminates more words (adds most information)
                if quantile_start > len(valid_words) - quantile_end:
                    print(f"[DEBUG] Quantile Start = {valid_words[quantile_start]} (expect suggested word to be upper)")
                    target_index = quantile_start
                else:
                    print(f"[DEBUG] Chose End = {valid_words[quantile_end]} (Expect suggested word to be lower)")
                    target_index = quantile_end
                # target_index = quantile_start if (after_first > before_second) else quantile_end
            else:
                print("Keys are close together! Greedy Policy")
                target_index = quantile_index
    else:
        target_index = len(valid_words) // 2
    return valid_words, target_index

def main() -> None:
    """
    The main function to run the Betweenle Solver.
    """

    print("Welcome to Betweenle Solver!")
    word1 = input("Enter the first word (leave blank if not selected yet): ").lower()
    word2 = input("Enter the second word (leave blank if not selected yet): ").lower()

    after_first = input("Enter the estimated distance after the first word (optional): ")
    before_second = input("Enter the estimated distance before the second word (optional): ")

    word_list = get_word_list()

    if after_first and before_second:
        after_first = float(after_first)
        before_second = float(before_second)
        between_words, target = find_between_words(word1, word2, word_list, after_first, before_second)
    else:
        between_words, target = find_between_words(word1, word2, word_list)

    if between_words:
        print(f"> Words between '{word1}' and '{word2}':")
        print(','.join(between_words[:10]),'...' if len(between_words)>10 else '\n')
        print(f"{len(between_words)} matches found!")
        print("="*10)
        if after_first and before_second:
            print(f"\n\nI Recommend: {between_words[target]}\n\n")
        else:
            print(f"Binary Search Recommended: '{between_words[len(between_words)//2]}'")
    else:
        print(f"No words found between '{word1}' and '{word2}'.")

if __name__ == "__main__":
    main()