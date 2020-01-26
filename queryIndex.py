def queryIndex():
    '''O: inverted index from txt file InvertedIndex.txt'''
    # index from txt file
    recInvertedIndex = {}

    # dictionary in a format of inverted index in final form
    lines = {}

    # open invertedIndex txt file
    with open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\invertedIndex.txt', 'r') as f:
        for line in f:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.split('|')
            # Key = term: Value = id:pos1,pos2,...;
            lines[line[0]] = line[1]

        keys = lines.keys()
        # for every term |Key = term: Value = id:pos1,pos2,...;| --> |Key = term: Value = [(id, [pos1, pos2, ...]), ...]
        for key in keys:

            # split coordinates by ;
            lines[key] = lines[key].split(';')

            # delete all occurences of whitespace in list of strings
            lines[key] = [i for i in lines[key] if i != '']

            # split id: pos1, pos2, ... by :
            for string in lines[key]:
                lines[key][lines[key].index(string)] = tuple(string.split(':'))
            
            # spit positions by , and change each position to int type
            for coordinates in lines[key]:
                index, pos = coordinates
                pos = pos.split(',')
                for i in pos:
                    pos[pos.index(i)] = int(i)
                lines[key][lines[key].index(coordinates)] = (index, pos)

    return lines


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
