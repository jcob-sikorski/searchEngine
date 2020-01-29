def queryIndex():
    '''O: inverted index from txt file InvertedIndex.txt'''
    # invertedIndex from txt file
    recInvertedIndex = {}

    # open invertedIndex txt file
    with open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\invertedIndex.txt', 'r') as f:
        for line in f:
            line = line.replace(' ', '').replace('\n', '').split('|')

            # Key = term: Value = id:pos1,pos2,...;
            recInvertedIndex[line[0]] = line[1]

        # for every term |Key = term: Value = id:pos1,pos2,...;| --> |Key = term: Value = [(id, [pos1, pos2, ...]), ...]
        for key in recInvertedIndex.keys():

            # delete all occurences of whitespace in list of strings
            recInvertedIndex[key] = [i for i in recInvertedIndex[key].split(';') if i != '']

            # split id: pos1, pos2, ... by :
            for string in recInvertedIndex[key]:
                recInvertedIndex[key][recInvertedIndex[key].index(string)] = tuple(string.split(':'))
            
            # spit positions by , and change each position to int type
            for coordinates in recInvertedIndex[key]:
                index, pos = coordinates

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

        # inverted index of all articles
        invertedIndex = queryIndex()
        
        # stemmed searched term
        sQuery = stemmer(query)
        
        # articles IDs
        IDs = []

        for term in sQuery:
            for ID, pos in invertedIndex[term]:
                IDs.append(ID)
    except:
        IDs = []

    return IDs


def freeTextQuery():
    '''I: Free Text Query from terminal
    O: list of articles' IDs where terms occur
    '''   
    from invertedIndex import getTerms

    query = input('Search: ')
    terms = getTerms(query)

    IDs = []

    invertedIndex = queryIndex()

    for term in terms:
        try:
            for ID, pos in invertedIndex[term]:
                IDs.append(ID)
        except:
            pass
        
    return IDs


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


def phraseQueries():
    from invertedIndex import getTerms

    query = 'departure from brown computer science university'
    terms = getTerms(query)
    

    invertedIndex = queryIndex()

    holder = []
    IDs = []

    for term in terms:
        if term in invertedIndex.keys():
            for coordinates in invertedIndex[term]:

                holder.append(coordinates[0])

            IDs.append(holder)
            holder = []
        else:
            # for tests pass, in reality change pass to break
            pass

    inter = list(set(intersect(IDs)))
    positions = []
    
    print(f'inter {inter}')

    for i in inter:
        holder = []
        for term in terms:
            if term in invertedIndex.keys():
                for ID, pos in invertedIndex[term]:
                    print(ID)
                    if ID in inter:
                        print(f'------------------ {inter}')
                        holder.append(pos)

        positions.append(holder)
        holder = []

    print(f'positions {positions}')
    for i, x in enumerate(positions):
        for ind, l in enumerate(x):
            for y in l:
                positions[i][ind] = l[0] - ind

    print(f'positions {positions}')   

    c = []

    for i, x in enumerate(positions):
        for ind, pos in enumerate(x):
            try:
                if positions[i][ind+1] == pos + 1:
                    print('ja ja')
                    c.append(inter[i])

            except:
                pass
    
    print(c)
            

    return IDs


#test = 'brown computer science dog in universe'
phraseQueries()
