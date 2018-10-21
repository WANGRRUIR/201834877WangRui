import os
from dataHandle import getFilePath
import codecs
import chardet
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy

dataHandledPath='/home/wangrui/data/20news-18828_handeled/'
tfidfPath='/home/wangrui/data/20news-18828-tfidf'

def tfidf(dataHandledPath):
    filePath=getFilePath(dataHandledPath)
    print(filePath)

    allText=[]

    for tfp in filePath:
        #print(tfp)
        #with open(tfp,'r') as fo:
        with codecs.open(tfp,'rb') as co:
            text=co.read()
            encodeInfo = chardet.detect(text)
            text=text.decode(encodeInfo["encoding"])
            #text = ast.literal_eval(text)
            #读取处理过保存的数据文件
            tmpText=" "
            tmpText=tmpText.join(ast.literal_eval(text))
            #print(tmpText)
            #获取所有内容
            allText.append(tmpText)
    print(len(allText))
    #生成tfidf
    tfidf=TfidfVectorizer()
    tfidfModel=tfidf.fit(allText)
    #tfidf的矩阵形式表示
    tfidfResult=tfidfModel.transform(allText)
    #print(tfidfResult)
    #matrixResult=tfidfResult.todense()
    #print(type(matrixResult))
    #矩阵对应的列的权重
    #print(tfidfModel.vocabulary_)
    return tfidf,tfidfModel,tfidfResult,filePath,allText

def tfidfWrite(tfidf,tfidfResult,dataHandledPath,filePath):
    #每个文件写入tfidf值
    #filePath=getFilePath(dataHandledPath)
    words=tfidf.get_feature_names()
    TFIDF=dict()

    for i in range(len(filePath)):
        tfidfFilePath=filePath[i].replace("20news-18828_handeled","20news-18828-tfidf")
        fileName=tfidfFilePath[tfidfFilePath.rfind('/')+1:]
        dirPathHandeled=tfidfFilePath[:tfidfFilePath.rfind('/')]
        print(tfidfFilePath)
        if os.path.exists(dirPathHandeled)==False:
            os.makedirs(dirPathHandeled)
        with codecs.open(tfidfFilePath,'w+') as co:
            for j in range(len(words)):
                if tfidfResult[i,j]>1e-5:
                    co.write(words[j]+':'+str(tfidfResult[i,j]))
                    co.write('\n')
                    TFIDF[str(words[j])]=tfidfResult[i,j]

    print(TFIDF)

def tfidfModelGenerate(tfidf,tfidfResult):
    words=tfidf.get_feature_names()
    matrixResult=tfidfResult.todense()
    #numpy.savetxt('tfidfModel.csv', matrixResult, delimiter = ',')
    #matrixResult = numpy.loadtxt(open("tfidfModel.csv","rb"),delimiter=",",skiprows=0)
    #print(type(matrixResult))
    with codecs.open('tfidfModel.txt','w+') as co:
        co.write(str(tfidf.get_feature_names()))
        co.write('\n')
        co.write(str(matrixResult))
    return



#tfidf,tfidfModel,tfidfResult,filePath,allText=tfidf(dataHandledPath)
#tfidfWrite(tfidf,tfidfResult,dataHandledPath,filePath)
#tfidfModelGenerate(tfidf,tfidfResult)
