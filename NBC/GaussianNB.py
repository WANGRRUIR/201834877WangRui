import os
from sklearn.naive_bayes import GaussianNB
import numpy as np
from VSMKNN.dataHandle import getFilePath
import codecs
import chardet
from sklearn.feature_extraction.text import TfidfVectorizer
import ast

dataHandledPath='/home/wangrui/data/20news-18828_handeled/'
#所有类别-dict
all_class_name={}
#每个数据对应的类别-list
file_class=[]

def get_all_class(dataHandledPath):
    for root,dirs,files in os.walk(dataHandledPath):
        break
    for index,tmp_class in enumerate(dirs):
        all_class_name[tmp_class]=index
    print(all_class_name.values())

def get_class_name(dataHandledPath):
    filePath=getFilePath(dataHandledPath)
    #print(filePath)
    for tmp_class in filePath:
        file_class.append(all_class_name[tmp_class.split('/')[-2]])
    print(file_class)

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
    print(tfidfResult)
    matrixResult=tfidfResult.todense()

    model=GaussianNB()
    for tmp in zip(matrixResult,file_class):
        model.partial_fit(matrixResult,file_class,all_class_name.values())

    predicted=model.predict(matrixResult[0])
    print(predicted)





get_all_class(dataHandledPath)
get_class_name(dataHandledPath)