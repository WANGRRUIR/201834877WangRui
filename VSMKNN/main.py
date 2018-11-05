from vsm import tfidf
from knn import knn

dataHandledPath='/home/wangrui/data/20news-18828_handeled/'

tfidf,tfidfModel,tfidfResult,filePath,allText=tfidf(dataHandledPath)
tmatrixResult=knn(tfidfResult,allText,filePath,5)