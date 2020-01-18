from porterStemmer import PorterStemmer
import re
from collections import defaultdict

porter = PorterStemmer()

def getStopwords():
    '''O: list of common words in English language.'''
    with open(r'C:\Users\jmsie\Dev\Projects\SearchEngine\search_engine\Include\stopwords.txt', 'r') as f:
        sWord = [line.rstrip() for line in f]

    stopwords = dict.fromkeys(sWord)
    return stopwords

def getTerms(line):
    '''I: line of text in page. 
    
    O: characteristic words in this line.'''
    line = line.lower()

    #put spaces instead of non-alphanumeric characters
    line=re.sub(r'[^a-z0-9 ]',' ',line)
    line = line.split()

    stopwords = getStopwords()

    #if term isn't stopword (stopword = common word) pop it out, else add it to list of tokens
    tokens = [term for term in line if term not in stopwords.keys()]

    #transform term to it's core  [happened --> hapenn]
    tokens = [porter.stem(term, 0, len(term)-1) for term in tokens]

    return tokens

def parseCollection(coll):
    '''I: collection in form of XML file. Containing tags: page, id, title and text
     
     O: dictionary with keys:

      pageId eg. ('18987398723'), 
      pageTitle eg. ('In the Middle of Nowhere.'), 
      pageText eg. ('In early 80s Freud done something unexpectedly, obviously')
    '''
    #current page
    doc = []

    #search for the end of the page and add it to doc
    for line in coll:
        if line == '<\page>':
            break
        doc.append(line)
    
    currPage = ''.join(doc)
    
    #p stands for current page

    pid=re.search('<id>(.*?)</id>', currPage, re.DOTALL)
    ptitle=re.search('<title>(.*?)</title>', currPage, re.DOTALL)
    ptext=re.search('<text>(.*?)</text>', currPage, re.DOTALL)

    #dictionary with keys: id, title and text eg.
    #{'id': ' 1872628290 ', 'title': ' Cow in the middle of nowhere. ', 'text': ' language chinese poland '}
    parsedPage = {}

    parsedPage['id'] = pid.group(1)
    parsedPage['title'] = ptitle.group(1)
    parsedPage['text'] = ptext.group(1)

    return parsedPage
    
#<page> <title> Freud. Neuroplascity and Alzheimer issues. </title> <id> 8773629817 </id> <text> In early 80s Freud done something unexpectedly, obviously he discovered new paradox. </text> </page>')

def createIndex(coll):
    '''I: collection in form of XML file. 

    O: invertedIndex eg. 
    {'languag': [' 1872628290 ', [3]], 'chines': [' 1872628290 ', [1]]} 

    where key is stem of characteristic word and a value is a list containing 
    IDs of articles in which it occures and a positions in every article.'''

    parsedPage = parseCollection(coll)
    print(f'parsedPage {parsedPage}')

    pageId = parsedPage['id']
    print(f'pageId {pageId}')
    pageTitle = parsedPage['title']
    print(f'pageTitle {pageTitle}')
    pageText = parsedPage['text']
    print(f'pageText {pageText}')

    tokens = getTerms(pageText)
    print(f'tokens {tokens}')

    concatenate = pageTitle.split() + pageText.split()
    print(f'concatenate {concatenate}')

    articleId = {}

    for token in tokens:
        articleId[token] = pageId

    print(f'tokensId {articleId}')
    
    tokensPos = {}

    for position, token in enumerate(tokens):
        tokensPos[token] = position

    print(f'tokensPos {tokensPos}')

    invertedIndex = {}

    for token in tokens:
        invertedIndex[token] = [articleId[token], [tokensPos[token]]]
    print(f'invertedIndex {invertedIndex}')

    return articleId, tokensPos
