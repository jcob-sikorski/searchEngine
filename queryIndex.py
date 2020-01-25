def queryIndex():
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

    print(f'lines {lines}')

queryIndex()