"""
    File: writer-bot-ht.py
    Author: Kiel McDonald
    Purpose: Generate a randomized line of text given a seed and a file to work from using the Markov
             Chain Algorithm and a hash table.
        
"""
import random
SEED = 8
NONWORD = "@"

def main():
    # Input
    sfile = input()# name of file containing words to randomize
    hash_size = int(input())
    n = int(input())# length to prefix
    if n < 1:
        print("ERROR: specified prefix size is less than one")
        exit(1)
    text_size = int(input())# words to be generated
    if text_size < 1:
        print("ERROR: specified size of the generated text is less than one")
        exit(1)
    # Processing
    word_list = build_word_list(sfile, n)
    markov_table = build_markov_table(hash_size, word_list, n)
    tlist = random_text_generation(markov_table, text_size, word_list, n)

    # Output
    print_text(tlist, text_size, n)

def build_word_list(sfile, n):
    """
    This function reads an input file and builds a list with each seperate word as an element.
    
    Parameters: sfile is the name of the file to be opened. n is the size of the prefix pair.

    Returns: word_list is a list of all the words from the source document.
    
    Pre-condition: sfile must be readable, n must be greater than 0.

    Post-condition: all words from the source doc will be added to the list to build the hash table.
    """  
    # Add all words in source doc to a list
    word_list = []

    for i in range(n):
        word_list.extend(NONWORD)
    lines = open(sfile).readlines()
    for line in range(len(lines)):
        text_line = lines[line].split()
        word_list.extend(text_line)
    return word_list

def build_markov_table(hash_size, word_list, n):
    """
    This function builds a hash table given a size and the word list to use as keys. It uses
    the HashTable methods to check for duplicates and add to the list of siuffixes if a key is a duplicate.
    
    Parameters: hash_size is the size of the table to be created, word_list is the list of all words from
    the source document, n is the number of words to be used to create a prefix.

    Returns: a table with all of the words placed within with their corresponding suffixes.
    
    Pre-condition: hash_size must be greater than the size of the word_list.

    Post-condition: the table will co ntain all of the individual unique keys from word_list.
    """ 
    markov_table = HashTable(hash_size)
    for word in range(len(word_list)):
        if word_list[word] != NONWORD:
            if n > 1:
                key = ""
                for x in range(n):
                    if word + x < len(word_list):
                        key += str(word_list[word + x]) + " "
                key = key.strip() # remove any extra space        
                if (word + x + 1) < len(word_list):
                    if key in markov_table:
                        markov_table.get(key).append(word_list[word + x + 1]) # add word to suffix list
                    else:
                        values = [word_list[word + x + 1]]
                        markov_table.put(key, values)
            else: # if n == 1
                key = word_list[word]
                if (word + 1) < len(word_list):
                    if key in markov_table:
                        markov_table.get(key).append(word_list[word + 1])
                    else:
                        values = [word_list[word + 1]]
                        markov_table.put(key, values)
    return markov_table

def random_text_generation(markov_table, text_size, word_list, n):
    """
    This function generates random text using the Markov algorithm.
    
    Parameters: markov_table is the HashTable with all prefix suffix pairs, text size is the number of
    words to be generated, word_list is the list of all words from the source doc, n is the number of words
    in the prefix.

    Returns: tlist is a list of words that make up the generated block of text.
    
    Pre-condition: text_size should not be greater than word_list

    Post-condition: a list will be used to store all of the words to be printed.
    """  
    random.seed(SEED)
    tlist = [] # will contain randomized text as a list
    key = ' '.join(word_list[n: n+n])
    word_list = word_list[n+n:]
    tlist.extend(key.split())
    for i in range(text_size - 1):
        if markov_table.get(key) != None: 
            suffix_list = markov_table.get(key)
            if len(suffix_list) > 1:
                rand = random.randint(0, len(suffix_list) - 1)
                word = suffix_list[rand]
            else:
                word = suffix_list[0]
            tlist.append(word)
            if n > 1:
                key = key.split()[1] + " " + word
            else:
                key = word
    return tlist

def print_text(tlist, text_size, n):
    """
    This function prints the elements of tlist, 10 words per line.
    
    Parameters: tlist is a list of words that make up the generated block of text, text size is the
    number of words to be generated, n is the number of words in the prefix. 

    Returns: None.
    
    Pre-condition: text size must be greater than 0.

    Post-condition: words will be printed in order 10 per line.
    """ 
    if n > 1:
        x = n - 1
        tlist = tlist[:-x]
    if len(tlist) > 9:
        print(' '.join(tlist[:10]))
        tlist = tlist[10:]
        while len(tlist) > 0:
            if len(tlist) > 9:
                line = ' '.join(tlist[:10])
                print(line)
                tlist = tlist[10:]
            else:
                print(' '.join(tlist))
                tlist = []
    else:
        print(' '.join(tlist))
        

class HashTable:
    """
    This class builds a HashTable ADT which uses a list to store keys and their associated and their associated
    values (in a list).
    
    Parameters: size is the size of the hashTable to be created.

    Returns: None. (Constructor)
    
    Pre-condition: size should be greater than that of the amount of keys to be stored.

    Post-condition: a HashTable object will be created.
    """ 
    def __init__(self, size):
        self._pairs = [None] * size
        self._size = size

    def put(self, key, value): # deal with new keys
        """
        This method puts new keys into the hash table by indexing through the table by the increment
        generated by the hash function. It continues to loop until an empty spot is found.
        
        Parameters: key is what is being added to the hashtable while value is what is being stored
        in association with the key.

        Returns: None.
        
        Pre-condition: the hash table must have an empty space.

        Post-condition: the key and its associated value will be added to the table.
        """ 
        hash_incr = int(self._hash(key))
        put = False
        curr_pos = hash_incr - 1
        while put == False:
            if self._pairs[curr_pos] == None:
                self._pairs[curr_pos] = [key]
                self._pairs[curr_pos].extend([value])
                put = True
            else:
                if (curr_pos + hash_incr) > (len(self._pairs) - 1): # loop back to start
                    curr_pos = abs(len(self._pairs) - (curr_pos + hash_incr))
                else:
                    curr_pos += hash_incr

    def get(self, key):
        """
        This method returns the list of values associated with the given key if it exists in the table.
        
        Parameters: key is what is being looked for in the table.

        Returns: a list of values associated with the key if it exists in the table, None if it doesn't.
        
        Pre-condition: key must exist in the table for a list to be returned.

        Post-condition: a list, or None, will be returned.
        """ 
        if key in self:
            hash_incr = int(self._hash(key))
            curr_pos = hash_incr - 1
            while self._pairs[curr_pos][0] != key:
                if (curr_pos + hash_incr) > (len(self._pairs) - 1): # loop back to start
                    curr_pos = abs(len(self._pairs) - (curr_pos + hash_incr))
                else:
                    curr_pos += hash_incr
            return self._pairs[curr_pos][1]

        else:
            return None    

    def __contains__(self, key):
        """
        This method checks to see if the given key exists in the table.
        
        Parameters: key is what we are looking for in the table. 

        Returns: True if the key is in the table false if not.
        
        Pre-condition: the table should not be empty.

        Post-condition: This function will be used to determine wether or not a new key needs
        to be added to the table.
        """ 
        hash_incr = int(self._hash(key))
        initial_check = hash_incr - 1
        curr_pos = hash_incr - 1
        iteration = 0
        while curr_pos != initial_check or iteration == 0: # poor man's do-while loop
            iteration += 1
            if self._pairs[curr_pos] != None and self._pairs[curr_pos][0] == key:
                return True
            else:
                if (curr_pos + hash_incr) > (len(self._pairs) - 1):
                    curr_pos = abs(len(self._pairs) - (curr_pos + hash_incr))
                else:
                    curr_pos += hash_incr
        return False
                    
    def _hash(self, key):
        """
        This method hashes the key into an int that will be used to step through the table.
        
        Parameters: key is what is being hashed to an int.

        Returns: an int that represents the increment to be used when looping through the table.
        
        Pre-condition: key should not be empty.

        Post-condition: each unique key will always have the same hash value.
        """ 
        p = 0
        for c in key:
            p = 31*p + ord(c)
        return p % self._size

    def __str__(self):
        return str(self._pairs)
main()
