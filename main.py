'''
Main program.
Start searching and find what you want.
'''

from queryIndex import *
import pickle

# invertedIndex in bits
invertedIndexInBits = open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\idx.txt', 'rb')
invertedIndex = pickle.load(invertedIndexInBits)

query = input('Search: ')

if query.startswith("'") and query.endswith("'") or query.startswith('''"''') and query.endswith('''"'''):
    phraseQueries(invertedIndex, query)

elif len(query.split()) > 1:
    freeTextQuery(invertedIndex, query)

else:
    oneWordQuery(invertedIndex, query)
