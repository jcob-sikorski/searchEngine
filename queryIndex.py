import pickle

def intersect(l):
    '''
    I: list of lists of elements
    O: list of sequences which is in every list
    '''
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


def oneWordQuery(invertedIndex, query):
    '''I: query from terminal
    O: list of articles' IDs where term occurs
    '''
    # stem searched term
    from invertedIndex import getTerms
    terms = getTerms(query)

    # if query in invertedIndex return articles IDs in which query occurs
    # else return []
    for term in terms:
        IDs = []
        if term in invertedIndex.keys():
            for ID, pos in invertedIndex[term]:
                IDs.append(ID)
        else:
            return []
    print(f'IDs {IDs}')
    return IDs


def freeTextQuery(invertedIndex, query):
    '''I: Free Text Query from terminal
    O: list of articles' IDs in which some searched terms occur
    '''   
    from invertedIndex import getTerms
    terms = getTerms(query)
    IDs = []

    for term in terms:
        if term in invertedIndex.keys():
            for ID, pos in invertedIndex[term]:
                IDs.append(ID)

    IDs = list(set(IDs))   
    print(f'IDs {IDs}')
    return IDs


def phraseQueries(invertedIndex, query):
    '''I: phraseQuery from terminal with quotes
    O: list of articles' IDs in which some searched terms occur
    '''   
    from invertedIndex import getTerms
    #from collections import defaultdict

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
            return None

    # IDs of articles in which query occurs
    inter = list(set(intersect(IDs)))
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

    legit = []

    for ID in inter:
        #holder is temporary storage for entire sequence of words
        holder = list(positions[ID])
        #h is a for a test if query is in particular order
        h = []

        for ei, elem in enumerate(holder):
            h.append(elem-ei)
        #if length of terms is equal to number of same numbers in h, query is in the article
        for elem in h:
            if h.count(elem) == len(terms):
                legit.append(ID)

    print(f'legit {list(set(legit))}')
    return list(set(legit))
