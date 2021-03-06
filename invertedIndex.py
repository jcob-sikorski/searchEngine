from porterStemmer import PorterStemmer
import re
from collections import defaultdict
import pickle

'''
1) Concatenates the title and the text of the page.
2) Lowercases all words.
3) Gets all tokens, where a token is a string of alphanumeric characters terminated by a non-alphanumeric character. 
    The alphanumeric characters are defined to be [a-z0-9]. So, the tokens for the word ‘apple+orange’ would be ‘apple’ 
    and ‘orange’.
4) Filters out all the tokens that are in the stop words list, such as ‘a’, ‘an’, ‘the’.
5) Stems each token using Porter Stemmer to finally obtain the stream of terms. 
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
    
    O: if termOnly=True: characteristic words in this line.
      else: all words stemmed.'''
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

    currPage = coll

    #p stands for current page
    pid=re.search('<id>(.*?)</id>', currPage, re.DOTALL)
    ptitle=re.search('<title>(.*?)</title>', currPage, re.DOTALL)
    ptext=re.search('<text>(.*?)</text>', currPage, re.DOTALL)

    parsedPage['id'] = pid.group(1)
    parsedPage['title'] = ptitle.group(1)
    parsedPage['text'] = ptext.group(1)

    return parsedPage


def createIndex(coll, invertedIndex, termsOnly=True):
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
 
    # characteristic words' core in title + text
    tokens = getTerms(' '.join(concatenate))
    notCharTokens = getTerms(' '.join(concatenate), False)

    # current page ID
    articleId = {token:pageId for token in tokens}

    tokensPos = {}
    # if word is a token append it to tokensPos
    if termsOnly:

        for pos, word in enumerate(notCharTokens):
            if word in tokens:
                if word in tokensPos:
                    tokensPos[word].append(pos)
                else:
                    tokensPos[word] = [pos]
         
    else:

        for pos, word in enumerate(notCharTokens):
            if word in tokensPos:
                tokensPos[word].append(pos)
            else:
                tokensPos[word] = [pos]

    tokens = list(set(tokens))
    notCharTokens = list(set(notCharTokens))

    # if token is already in invertedIndex, add only its position,
    # else create for new token a list and append to it its articleId and its position in text
    if termsOnly:
        for token in tokens:
            if token not in invertedIndex.keys():
                invertedIndex[token] = [(int(articleId[token]), tokensPos[token])]
            else:
                invertedIndex[token].append((int(articleId[token]), tokensPos[token]))
    else:
        for word in notCharTokens:
            if word not in invertedIndex.keys():
                invertedIndex[word] = [(int(articleId[tokens[0]]), tokensPos[word])]
            else:
                invertedIndex[word].append((int(articleId[tokens[0]]), tokensPos[word]))
    return invertedIndex

invertedIndex = {}

with open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\test.txt', 'r', encoding='utf8') as f:
    # collection of articles
    data = f.read().replace('\n', ' ')

    # list of every article in document
    articles = re.findall('<page> (.*?) </page>', data, re.DOTALL)

    for article in articles:
        createIndex(article, invertedIndex, False)

# bit container for invertedIndex
afile = open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\idx.txt', 'wb')

# transform invertedIndex to bits
pickle.dump(invertedIndex, afile)
afile.close()
