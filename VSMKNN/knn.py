import os
import nltk
from nltk.stem import WordNetLemmatizer
from enchant.checker import SpellChecker
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import chardet
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer

def knn(tfidfResult,allText,filePath,k):
    matrixResult=tfidfResult.todense()

    with codecs.open('49960','rb') as co:
        text=co.read()
    encodeInfo = chardet.detect(text)
    text=text.decode(encodeInfo["encoding"])

    #print(text)
    #词干提取（不做）、词形还原
    wnl=WordNetLemmatizer()
    text=wnl.lemmatize(text)

    #去掉所有带字符的词 剩下的存到list 分词
    words = [word for word in word_tokenize(text) if (str.isalpha(word) is not False)]
    #去掉停用词并转化为小写
    cachedStopWords=stopwords.words("english")
    text = [w.lower() for w in words if (w.lower() not in cachedStopWords)]
    tmpText=" "
    tmpText=tmpText.join(text)
    tallText=allText
    tallText.append(tmpText)

    #print(tmpText)

    ttfidf=TfidfVectorizer()
    ttfidfModel=ttfidf.fit(tallText)
    #tfidf的矩阵形式表示
    ttfidfResult=ttfidfModel.transform(tallText)
    tmatrixResult=ttfidfResult.todense()
    tmatrixResult=tmatrixResult[-1].tolist()
    print(tmatrixResult)
    print(matrixResult.shape)
    #比较得到cos距离
    dis=[]
    for i in range(len(filePath)):
        dis.append(cos(matrixResult[0].tolist()[0],tmatrixResult[0]))
    result=dict(zip(filePath,dis))
    result=list(sortedDict(result).items())
    for i in range(k):
        print(result[i][1])
    return



def cos(vector1,vector2):
    dot_product = 0.0;
    normA = 0.0;
    normB = 0.0;
    #print(len(vector1),len(vector2))
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB==0.0:
        return None
    else:
        return dot_product / ((normA*normB)**0.5)

def sortedDict(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)




