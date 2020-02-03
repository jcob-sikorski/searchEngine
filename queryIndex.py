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
    from invertedIndex import getTerms
    #from collections import defaultdict

    query = input('Search: ')
    terms = getTerms(query, False)
    # IDs of articles in which term occured
    IDs = []

    for term in terms:
        holder = []

        if term in invertedIndex.keys():
            for coordinates in invertedIndex[term]:
                # add all IDs of articles in which the term occurs
                holder.append(coordinates[0])
            # add all IDs to the IDs
            IDs.append(holder)
        else:
            print('None!')
            return None
    print(f'IDs {IDs}')

    # IDs of articles in which query occurs
    inter = list(set(intersect(IDs)))
    positions = {key:[] for key in inter}

    print(f'\ninter {inter}')
    #terms = list(set(terms))
    for term in terms:
        if term in invertedIndex.keys():
            for ID, pos in invertedIndex[term]:
                if ID in inter:
                    positions[ID].append(pos)
    
    print(f'positions {positions}')
    for ID in inter:
        holder = []
        for i, termPos in enumerate(positions[ID]):
            holder.append(termPos[0] - i)
        positions[ID] = holder

    legit = []
    print(f'positions {positions}')
    for ID in inter:
        if positions[ID][0] == positions[ID][1] or positions[ID][0] == positions[ID][1]+1:
            legit.append(ID)

    print(legit)

    return legit

invertedIndex = queryIndex()
freeTextQuery(invertedIndex)
