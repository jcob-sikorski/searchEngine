def queryIndex():
    '''O: inverted index from txt file InvertedIndex.txt'''
    # invertedIndex from txt file
    recInvertedIndex = {}

    # open invertedIndex txt file
    with open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\invertedIndex.txt', 'r') as f:
        for line in f:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.split('|')
            # Key = term: Value = id:pos1,pos2,...;
            recInvertedIndex[line[0]] = line[1]

        keys = recInvertedIndex.keys()
        # for every term |Key = term: Value = id:pos1,pos2,...;| --> |Key = term: Value = [(id, [pos1, pos2, ...]), ...]
        for key in keys:

            # split coordinates by ;
            recInvertedIndex[key] = recInvertedIndex[key].split(';')

            # delete all occurences of whitespace in list of strings
            recInvertedIndex[key] = [i for i in recInvertedIndex[key] if i != '']

            # split id: pos1, pos2, ... by :
            for string in recInvertedIndex[key]:
                recInvertedIndex[key][recInvertedIndex[key].index(string)] = tuple(string.split(':'))
            
            # spit positions by , and change each position to int type
            for coordinates in recInvertedIndex[key]:
                index, pos = coordinates
                print(f'coordinates {index}')
                pos = pos.split(',')
                for i in pos:
                    pos[pos.index(i)] = int(i)
                recInvertedIndex[key][recInvertedIndex[key].index(coordinates)] = (int(coordinates[0]), pos)
    print(f'recInvertedIndex {recInvertedIndex}')
    return recInvertedIndex


def oneWordQuery():
    '''I: query from terminal
    O: list of articles' IDs where term occurs
    '''
    # stem searched term
    from invertedIndex import stemmer

    try:
        query = input('Search: ')
        print(f'query {query}')

        # inverted index of all articles
        invertedIndex = queryIndex()
        
        # stemmed searched term
        sQuery = stemmer(query)
        print(f'sTerm {sQuery}')

        IDs = []

        for term in sQuery:
            for ID, pos in invertedIndex[term]:
                IDs.append(ID)

    except:
        IDs = []
    
    print('IDs ', IDs)

    return IDs

def freeTextQuery():
    '''I: Free Text Query from terminal
    O: list of articles' IDs where terms occur
    '''   
    from invertedIndex import getTerms

    query = input('Search: ')
    terms = getTerms(query)
    print(f'terms {terms}')

    IDs = []

    invertedIndex = queryIndex()

    for term in terms:
        try:
            for ID, pos in invertedIndex[term]:
                IDs.append(ID)
        except:
            pass

    print(f'IDs {IDs}')
    return IDs

def phraseQueries():
    query = input('Search: ')
