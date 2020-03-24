'''
Main program.
Start searching and find what you want.
'''

import os

# try to install pickle module if not present
# if all went well, import required module again (for global access)

try:
  import pickle
except ImportError:
  print("Trying to Install required module: pickle\n")
  os.system('python -m pip install pickle')

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
