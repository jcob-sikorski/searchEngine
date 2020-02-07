import pickle

def queryIndex():
    '''O: inverted index from txt file InvertedIndex.txt'''
    # invertedIndex from txt file
    invertedIndex = {}

    # open invertedIndex txt file
    with open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\invertedIndex.txt', 'r') as f:
        for line in f:
            line = line.replace(' ', '').replace('\n', '').split('|')

            # Key = term: Value = id:pos1,pos2,...;
            invertedIndex[line[0]] = line[1]

        # for every term |Key = term: Value = id:pos1,pos2,...;| --> |Key = term: Value = [(id, [pos1, pos2, ...]), ...]
        for term in invertedIndex.keys():
            # delete all occurences of whitespace in list of strings
            invertedIndex[term] = [i for i in invertedIndex[term].split(';') if i != '']

            # split id: pos1, pos2, ... by :
            for string in invertedIndex[term]:
                invertedIndex[term][invertedIndex[term].index(string)] = tuple(string.split(':'))
            
            # spit positions by ,
            for coordinates in invertedIndex[term]:
                index, pos = coordinates
                pos = pos.split(',')
                # change each position to int type
                for i in pos:
                    pos[pos.index(i)] = int(i)

                invertedIndex[term][invertedIndex[term].index(coordinates)] = (int(coordinates[0]), pos)
    return invertedIndex


def intersect(l):
    l = sorted(l, key=len)

    all_ids = []
    intersection = []

    for elem in l:
        for subElem in elem:
            all_ids.append(subElem)
    
    for elem in all_ids:
        if all_ids.count(elem) == len(l):
            intersection.append(elem)
        else:
            pass

    return intersection


def oneWordQuery(invertedIndex):
    '''I: query from terminal
    O: list of articles' IDs where term occurs
    '''
    # stem searched term
    from invertedIndex import getTerms

    stemQuery = getTerms(input('Search: '))
    # if query in invertedIndex return articles IDs in which query occurs
    # else return []
    for term in stemQuery:
        IDs = []
        if term in invertedIndex.keys():
            for ID, pos in invertedIndex[term]:
                IDs.append(ID)
        else:
            return []
    return IDs


def freeTextQuery(invertedIndex):
    '''I: Free Text Query from terminal
    O: list of articles' IDs in which some searched terms occur
    '''   
    from invertedIndex import getTerms

    terms = getTerms(input('Search: '))

    IDs = []

    for term in terms:
        if term in invertedIndex.keys():
            for ID, pos in invertedIndex[term]:
                IDs.append(ID)

    IDs = list(set(IDs))   

    print(f'IDs {IDs}')
    return IDs


def phraseQueries(invertedIndex):
    '''I: phraseQuery from terminal with quotes
    O: list of articles' IDs in which some searched terms occur
    '''   
    from invertedIndex import getTerms
    #from collections import defaultdict

    query = input('Search: ')
    terms = getTerms(query, False)
    print(f'terms {terms}')
    # IDs of articles in which term occured
    IDs = []

    for term in terms:
        holder = []

        if term in invertedIndex.keys():
            for coordinates in invertedIndex[term]:
                # add all IDs of articles in which the term occurs
                if coordinates[0] not in holder:
                    holder.append(coordinates[0])
            # add all IDs provided the previous condition
            IDs.append(holder)
        else:
            print('None!')
            return None
    #print(f'IDs {IDs}')
    # IDs of articles in which query occurs
    inter = list(set(intersect(IDs)))
    #print(f'inter {inter}')
    positions = {}

    # add positions of terms to positions
    for term in terms:
        if term in invertedIndex.keys():
            for ID, pos in invertedIndex[term]:
                if ID in inter:
                    if ID not in positions.keys():
                        positions[ID] = []
                    positions[ID].append(pos)

    # check if queried words are in the right order
    for ID in inter:
        holder = []
        for termPos in positions[ID]:
            for i in termPos:
                holder.append(i)
        positions[ID] = sorted(list(set(holder)))

    #print(f'positions {positions}')

    legit = []

    for ID in inter:
        #holder is temporary storage for entire sequence of words
        holder = list(positions[ID])
        #h is a for a test if query is in particular order
        h = []
        #print(f'holder {holder}')
        for ei, elem in enumerate(holder):
            h.append(elem-ei)
        #print(f'h {h}')
        #if length of terms is equal to number of same numbers in h, query is in the article
        for elem in h:
            if h.count(elem) == len(terms):
                legit.append(ID)

    print(f'legit {list(set(legit))}')
    return list(set(legit))


file2 = open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\idx.txt', 'rb')
new_d = pickle.load(file2)

phraseQueries(new_d)
