"""Generate Markov chains from text files."""

from random import choice
import sys

def open_and_read_file(file_path):
    """Take file path as string; return text as string.
    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as file:
        text = file.read()

    return text

def process_files(*args):

    text = ""
    for file in args:
        text += open_and_read_file(file)

    return text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.
    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.
    For example:
        >>> chains = make_chains("hi there mary hi there juanita")
    Each bigram (except the last) will be a key in chains:
        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]
    Each item in chains is a list of all possible following words:
        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """
    words = text_string.split()
    chains = {}

    chain_length = int(input("Input the number of words to use in your key: "))

    for i in range(len(words)-1):
        if i < (len(words) - chain_length):
            new_key = tuple(words[i:(i+chain_length)])
            chains[new_key] = chains.get(new_key, []) + [words[i+chain_length]]

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []
    key_list = list(chains)
    key = choice(key_list)
    puctuation = ['!', '?', '.']

    file_length = int(input("Enter the number of sentences to generate: "))

    for n in range(file_length):

        while key[0].istitle() is False:
            key = choice(key_list)

        while key in chains and key[-1][-1] not in puctuation:
            value = choice(chains[key])
            link = " ".join(key) + " " + value
            words.append(link)
            key = key[1:] + (value,)


    return " ".join(words)
