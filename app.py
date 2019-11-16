from flask import Flask, render_template, request
import pickle
import math

app = Flask(__name__)

f = open('captionings.pickle', 'rb')
captions = pickle.load(f)
f.close()

f = open('filenames.pickle', 'rb')
files = pickle.load(f)
f.close()

fl = open('indexed.pckl', 'rb')
dictOFTF_IDF = pickle.load(fl)
fl.close()

filenames = []
for x in files:
    filenames = filenames + [x[13:]]


@app.route('/')
def my_form():
    return render_template('base.html')


@app.route('/', methods=['POST'])
def hello_world():
    query = request.form['text']
    # print(captions)
    # print(filenames)
    imageDictionary = {}
    '''
    for index, sentence in enumerate(captions):
        sentence = str(sentence)
        print(sentence)
        tokenizedWords = sentence.split(' ')
        imageDictionary[index] = [(word, tokenizedWords.count(word)) for word in tokenizedWords]
    '''
    '''
    print(imageDictionary)

    termFrequency = {}
    for i in range(0, len(captions)):
        listOfNoDuplicates = []
        for wordFreq in imageDictionary[i]:
            if wordFreq not in listOfNoDuplicates:
                listOfNoDuplicates.append(wordFreq)
            termFrequency[i] = listOfNoDuplicates
    print("\nWords that don't appear twice:")
    print(termFrequency)

    allDocuments = ''
    for sentence in captions:
        allDocuments += str(sentence) + ' '
    allDocumentsTokenized = allDocuments.split(' ')

    print("\nTokens:")
    print(allDocumentsTokenized)

    allDocumentsNoDuplicates = []
    for word in allDocumentsTokenized:
        if word not in allDocumentsNoDuplicates:
            allDocumentsNoDuplicates.append(word)
    print("\nAll Unique Words:")
    print(allDocumentsNoDuplicates)

    dictOfNumberOfDocumentsWithTermInside = {}
    for index, voc in enumerate(allDocumentsNoDuplicates):
        count = 0
        for sentence in captions:
            if voc in str(sentence):
                count += 1
        dictOfNumberOfDocumentsWithTermInside[index] = (voc, count)
    print("\nCount of Terms:")
    print(dictOfNumberOfDocumentsWithTermInside)

    dictOFIDFNoDuplicates = {}
    for i in range(0, len(termFrequency)):
        listOfIDFCalcs = []
        for word in termFrequency[i]:
            for x in range(0, len(dictOfNumberOfDocumentsWithTermInside)):
                if word[0] == dictOfNumberOfDocumentsWithTermInside[x][0]:
                    listOfIDFCalcs.append(
                        (word[0], math.log(len(captions) / dictOfNumberOfDocumentsWithTermInside[x][1])))
        dictOFIDFNoDuplicates[i] = listOfIDFCalcs
    print("\nIDF Number:")
    print(dictOFIDFNoDuplicates)

    dictOFTF_IDF = {}
    for i in range(0, len(termFrequency)):
        listOFTF_IDF = []
        TFsentence = termFrequency[i]
        IDFsentence = dictOFIDFNoDuplicates[i]
        for x in range(0, len(TFsentence)):
            listOFTF_IDF.append((TFsentence[x][0], TFsentence[x][1] * IDFsentence[x][1]))
        dictOFTF_IDF[i] = listOFTF_IDF
    print("\nTF-IDF Number:")
    print(dictOFTF_IDF)
    '''
    '''
    fl = open('indexed.pckl', 'wb')
    pickle.dump(dictOFTF_IDF, fl)
    fl.close()
    '''
    '''
    fl = open('indexed.pckl', 'rb')
    dictOFTF_IDF = pickle.load(fl)
    fl.close()
    '''
    # query = "Blue flying sphere"

    topDocIndex = search_term_index(query, dictOFTF_IDF)
    topDocScore = search_term_score(query, dictOFTF_IDF)
    for k in enumerate(topDocIndex):
        print(captions[k[1]])
        print(filenames[k[1]])
    j = 0
    while j != 20:
        print(topDocScore[j][1])
        j = j+1

    score1 = str(topDocScore[0][1])
    print(score1)

    # top doc score contains document scores
    # captions contains captions

    return render_template('output.html', query=query, captions=captions, topDocScore=topDocScore, topDocIndex=topDocIndex, filenames=filenames)


def search_term_index(term, dicOFTF_IDF):
    # Will take the term, break it up into tokens. Find the TF_IDF of each term and return index of the best doc

    # Tokenize term
    wordsList = term.split(" ")
    # print('\nWordslist:')
    # print(wordsList)

    scoresOfDocs = {}
    for index, words in enumerate(dicOFTF_IDF):
        scoresOfDocs[index] = 0;
        # i represents number of words in each doc.
        for i in range(0, len(dicOFTF_IDF[index])):
            # The below prints all words
            # print(dicOFTF_IDF[index][i][0])

            # The below prints all scores
            # print(dicOFTF_IDF[index][i][1])
            # print("\n")
            for x, terms in enumerate(wordsList):
                if wordsList[x] == (dicOFTF_IDF[index][i][0]):
                    scoresOfDocs[index] += (dicOFTF_IDF[index][i][1])
    # print(scoresOfDocs)
    indexArray = sorted(range(len(scoresOfDocs)), key=lambda k: scoresOfDocs[k])[-20:]
    indexArray.reverse()
    # print(indexArray)
    return indexArray


def search_term_score(term, dicOFTF_IDF):
    # Will take the term, break it up into tokens. Find the TF_IDF of each term and return the score of the best doc.

    # Tokenize term
    wordsList = term.split(" ")
    # print('\nWordslist:')
    # print(wordsList)

    scoresOfDocs = {}
    for index, words in enumerate(dicOFTF_IDF):
        scoresOfDocs[index] = 0;
        # i represents number of words in each doc.
        for i in range(0, len(dicOFTF_IDF[index])):
            # The below prints all words
            # print(dicOFTF_IDF[index][i][0])

            # The below prints all scores
            # print(dicOFTF_IDF[index][i][1])
            # print("\n")
            for x, terms in enumerate(wordsList):
                if wordsList[x] == (dicOFTF_IDF[index][i][0]):
                    scoresOfDocs[index] += (dicOFTF_IDF[index][i][1])
    topDocScores = sorted(scoresOfDocs.items(), key=lambda u: u[1], reverse=True)
    # print(topDocScores)
    indexArray = sorted(range(len(scoresOfDocs)), key=lambda k: scoresOfDocs[k])[-20:]
    indexArray.reverse()
    # print(indexArray)
    return topDocScores


if __name__ == '__main__':
    app.run()
