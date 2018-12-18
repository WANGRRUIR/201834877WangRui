from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift
from sklearn.cluster import SpectralClustering
from sklearn.cluster import ward_tree
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn import mixture

import numpy as np
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer

data=[]
label=[]
with codecs.open("./Tweets.txt",'r') as co:
    col=co.readlines()
    for l in col:
        #print(l.replace('\n',''))
        tmp=eval(l.replace('\n',''))
        data.append(tmp["text"])
        label.append(tmp["cluster"])

print(data,label)

tfidf=TfidfVectorizer()
tfidfModel=tfidf.fit(data)
tfidfResult=tfidfModel.transform(data)
matrixResult=tfidfResult.todense()
print(matrixResult)

n=set(label)
#print(len(n))

#K-Means
km_cluster=KMeans(n_clusters=len(n))
result=km_cluster.fit_predict(matrixResult)
print(result)

#Affinity propagation
af=AffinityPropagation().fit_predict(matrixResult)
print(af)

#Mean-shift
ms=MeanShift().fit(matrixResult)
print(ms.labels_)

#Spectral clustering
sc=SpectralClustering(n_clusters=len(n)).fit(matrixResult)
print(sc.labels_)

#Ward hierarchical
ward = AgglomerativeClustering(n_clusters=len(n), linkage='ward').fit(matrixResult)
print(ward.labels_)

#Agglomerative clustering
ac=AgglomerativeClustering().fit(matrixResult)
print(ac.labels_)

#DBSCAN
dbscan=DBSCAN().fit(matrixResult)
print(dbscan.labels_)

#Gaussian mixtures
gm=mixture.GaussianMixture()
gm=gm.fit(matrixResult)
print(gm.predict(matrixResult[0]))