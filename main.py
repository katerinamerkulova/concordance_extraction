"""
Lab 1
A concordance extraction
"""


import os


def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    return ''.join([char for char in text.lower()
        if char.isalnum() or char.isspace()]).split()


def remove_stop_words(tokens: list, stop_words: list) -> list:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    stop_words = ['the', 'is']
    --> ['weather', 'sunny', 'man', 'happy']
    """
    return [word for word in tokens if word not in stop_words]


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    freqs = {i: tokens.count(i) for i in set(tokens)}
    return dict(sorted(freqs.items(), key=lambda x: x[1], reverse=True))


def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words to return
    :return: a list of the most common words
    e.g. tokens = ['weather', 'sunny', 'man', 'happy', 'and', 'dog', 'happy']
    top_n = 1
    --> ['happy']
    """
    return sorted(freq_dict, key=freq_dict.get,
            reverse=True)[:top_n]


def get_concordance(tokens: list,
                    word: str,
                    left_context_size: int,
                    right_context_size: int) -> list:
    """
    Gets a concordance of a word
    A concordance is a listing of each occurrence of a word in a text,
    presented with the words surrounding it
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    --> [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]
    """
    lcs = left_context_size
    rcs = right_context_size

    idx = [i for i, x in enumerate(tokens) if x == word]

    if lcs > 0 and rcs > 0:
        return [tokens[i-lcs:i+rcs+1] for i in idx]

    if not lcs > 0 and rcs > 0:
        return [tokens[i:i+rcs+1] for i in idx]

    if lcs > 0 and not rcs > 0:
        return [tokens[i-lcs:i+1] for i in idx]
    return []


def get_adjacent_words(tokens: list,
                       word: str,
                       left_n: int,
                       right_n: int) -> list:
    """
    Gets adjacent words from the left and right context
    :param tokens: a list of tokens
    :param word: a word-base for the search
    :param left_n: the distance between a word and an adjacent one in the left context
    :param right_n: the distance between a word and an adjacent one in the right context
    :return: a list of adjacent words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_n = 2
    right_n = 3
    --> [['man', 'is'], ['dog, 'cat']]
    """
    conc = get_concordance(tokens, word, left_n, right_n)
    if not left_n:
        return [[elem[-1]] for elem in conc]
    if not right_n:
        return [[elem[0]] for elem in conc]
    return [[elem[0], elem[-1]] for elem in conc]


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as file:
        data = file.read()
    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    with open(os.path.join(path_to_file, 'report.txt'),
              'w', encoding='utf-8') as file:
        file.write('\n'.join([' '.join(k) for k in content]))


def sort_concordance(tokens: list,
                     word: str,
                     left_context_size: int,
                     right_context_size: int,
                     left_sort: bool) -> list:
    """
    Gets a concordance of a word and sorts it by either left or right context
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :param left_sort: if True, sort by the left context, False – by the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    left_sort = True
    --> [['dog', 'is', 'happy', 'but', 'the', 'cat'], ['man', 'is', 'happy', 'the', 'dog', 'is']]
    """
    lcs = left_context_size
    rcs = right_context_size

    conc = get_concordance(tokens, word, lcs, rcs)
    if left_sort and lcs > 0:
        return sorted(conc)
    if not left_sort and rcs > 0:
        return sorted(conc, key=lambda x: x[conc[0].index(word) + 1:])
    return []
