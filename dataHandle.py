import os
import nltk
from nltk.stem import WordNetLemmatizer
from enchant.checker import SpellChecker
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import chardet
import codecs

#遍历数据文件夹得到所有文件的路径存到list中
def getFilePath(dataPath):
    filePath=[]
    for root,dirs,files in os.walk(dataPath):
        for file in files:
            tmpFilePath = os.path.join(root, file)
            filePath.append(tmpFilePath)
    #print(len(filePath))
    return filePath

#文本预处理
def datePreHandle(filePath):
    for tfp in filePath:
        print(tfp)
        #with open(tfp,'r') as fo:
        with codecs.open(tfp,'rb') as co:
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
            word_stopped = [w.lower() for w in words if (w.lower() not in cachedStopWords)]
            print(word_stopped)

            #数据处理后保存
            filePathHandeled=tfp.replace("20news-18828","20news-18828_handeled")
            fileName=filePathHandeled[filePathHandeled.rfind('/')+1:]
            dirPathHandeled=filePathHandeled[:filePathHandeled.rfind('/')]
            print(filePathHandeled,fileName,dirPathHandeled)

            #数据写入文件
            if os.path.exists(dirPathHandeled)==False:
                os.makedirs(dirPathHandeled)
            with open(filePathHandeled,"w+") as tmpfo:
                tmpfo.write(str(word_stopped))
    print("handled {} files".format(len(filePath)))
    return len(filePath)




#http://www.cnblogs.com/pinard/p/6756534.html
#https://blog.csdn.net/Galoa/article/details/79859215?utm_source=blogxgwz3

#nltk.download('wordnet')
#nltk.download('stopwords')
#nltk.download('punkt')

dataPath='/home/wangrui/data/20news-18828/'

#dirs=os.listdir(path)
#print(dirs)
#filePath=getFilePath(dataPath)
#print(filePath)
#print(datePreHandle(filePath))


'''
#拼写检查
checker=SpellChecker("en_US")
checker.set_text("like")
for err in checker:
    print("err:",err.word)

#词干提取（不做）、词形还原
wnl=WordNetLemmatizer()
print(wnl.lemmatize("countries"))

#转化为小写
str="fdsFSDfs"
print(str.lower())


#分词结果去掉停用词
cachedStopWords=stopwords.words("english")
print(cachedStopWords)
wordStoped=[]
words=["i"],["am"],["at"],["school"]
for word in words:
    filtered = [w for w in word if (w not in cachedStopWords)]
    if filtered!= []:
        wordStoped.append(filtered)
print(wordStoped)

'''
