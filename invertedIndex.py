from porterStemmer import PorterStemmer
import re
from collections import defaultdict

'''
1) Concatenate the title and the text of the page.
2) Lowercase all words.
3) Get all tokens, where a token is a string of alphanumeric characters terminated by a non-alphanumeric character. 
    The alphanumeric characters are defined to be [a-z0-9]. So, the tokens for the word ‘apple+orange’ would be ‘apple’ 
    and ‘orange’.
4) Filter out all the tokens that are in the stop words list, such as ‘a’, ‘an’, ‘the’.
5) Stem each token using Porter Stemmer to finally obtain the stream of terms. 
    Porter Stemmer removes common endings from words.
'''


porter = PorterStemmer()

def getStopwords():
    '''O: list of common words in English language.'''

    with open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\stopwords.txt', 'r') as f:
        sWord = [line.rstrip() for line in f]

    stopwords = dict.fromkeys(sWord)
    return stopwords

def getTerms(line, termsOnly=True):
    '''I: line of text in page. 
    
    O: characteristic words in this line.'''
    line = line.lower()
    #put spaces instead of non-alphanumeric characters
    line = re.sub(r'[^a-z0-9 ]',' ',line)
    words = line.split()

    if termsOnly:
        stopwords = getStopwords()

        #if term isn't stopword (stopword = common word) pop it out, else add it to list of tokens
        tokens = [term for term in words if term not in stopwords.keys()]

        #transform term to it's core  [happened --> hapenn]
        tokens = [porter.stem(term, 0, len(term)-1) for term in tokens]
    else:
        #transform term to it's core  [happened --> hapenn]
        stemWord = [porter.stem(term, 0, len(term)-1) for term in words]
        #print(f'stemWord {stemWord}')
        return stemWord

    return tokens

def parseCollection(coll):
    '''I: collection in form of XML file. Containing tags: page, id, title and text
     
     O: dictionary with keys:
      {
      pageId eg. :'18987398723', 
      pageTitle eg. :'In the Middle of Nowhere.', 
      pageText eg. :'In early 80s Freud done something unexpectedly, obviously'
      }
    '''
    #dictionary with keys: id, title and text eg.
    #{'id': ' 1872628290 ', 'title': ' Cow in the middle of nowhere. ', 'text': ' language chinese poland '}
    parsedPage = {}

    parsedPage['id'] = list()
    parsedPage['title'] = list()
    parsedPage['text'] = list()

    article = re.search('<page> (.*?) </page>', coll, re.DOTALL).group()

    #current page
    doc = []

    #search for the end of the page and add it to doc
    for line in article:
        if line == '<\page>':
            break
        doc.append(line)

    currPage = ''.join(doc)

    #p stands for current page
    pid=re.search('<id>(.*?)</id>', currPage, re.DOTALL)
    ptitle=re.search('<title>(.*?)</title>', currPage, re.DOTALL)
    ptext=re.search('<text>(.*?)</text>', currPage, re.DOTALL)

    parsedPage['id'] = pid.group(1)
    parsedPage['title'] = ptitle.group(1)
    parsedPage['text'] = ptext.group(1)

    return parsedPage


def createIndex(coll, invertedIndex):
    '''I: collection in form of XML file. 

    O: invertedIndex eg. 
    Key = term: Value = [(id, [pos1, pos2, ...]), ... 

    where key is stem of characteristic word and a value is a list containing 
    IDs of articles in which it occures and a positions in every article.'''

    parsedPage = parseCollection(coll)
    pageId = parsedPage['id']
    pageTitle = parsedPage['title']
    pageText = parsedPage['text']
 
    concatenate = pageTitle.split() + pageText.split()
    print(f'concatenate {concatenate}\n')

    # characteristic words' core in title + text
    tokens = getTerms(' '.join(concatenate))
    print(f'tokens {tokens}\n')
    notCharTokens = getTerms(' '.join(concatenate), False)

    # current page ID
    articleId = {token:pageId for token in tokens}

    ## if a word is a token append it to tokensPos
    tokensPos = {token:[] for token in tokens}

    for pos, token in enumerate(notCharTokens):
        if token in tokens:
            tokensPos[token].append(pos)

    print(f'tokensPos {tokensPos}\n')

    # if token occurs more than once, delete all occurences in tokens list
    for token in tokens:
        tk = {}
        tk[token] = tokens.count(token)
        if tk[token] > 1:
            tokens = [i for i in tokens if i != token]
            tokens.append(token)
    
    print(f'tokens without occurences {tokens}\n')

    # if token is already in invertedIndex, add only its position,
    # else create for new token a list and append to it its articleId and its position in text
    for token in tokens:
        if token not in invertedIndex.keys():
            invertedIndex[token] = [(int(articleId[token]), tokensPos[token])]
        else:
            invertedIndex[token].append((int(articleId[token]), tokensPos[token]))

    print(f'invertedIndex {invertedIndex}\n')

    return invertedIndex

def writeIndexToFile(invertedIndex):
    # index saved as    term|docID1:pos1,pos2;docID2:pos3,pos4,pos5;…
    with open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\invertedIndex.txt', 'a+') as f:
        for term in invertedIndex.keys():
            f.writelines(f'{term}|')

            for ID, position in invertedIndex[term]:
                # for every articleId write postion of a term in it
                f.writelines(f'{ID}:')
                
                # if there isn't only one position put a comma after it 
                # or if it's the last position in the list of positions, do not
                for pos in position:
                    # if it's the last element in the list do not write a comma
                    if position.index(pos) == len(position)-1:
                        f.writelines(f'{pos}')
                    else:
                        f.writelines(f'{pos},')
                f.writelines(f';')
            f.writelines('\n')

invertedIndex = {}

pages = ["<page> <title> one in the middle of nowhere </title> <id> 98798733 </id> <text> brown brown</text> </page>", 
"<page> <id> 1233323 </id> <title> department </title> <text> brown computer young university </text> </page>"]

for page in pages:
    createIndex(page, invertedIndex)

writeIndexToFile(invertedIndex)
