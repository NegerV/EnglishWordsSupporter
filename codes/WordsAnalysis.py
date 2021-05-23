import os
import gensim
rootPath = os.path.abspath(os.path.join(os.getcwd(), "..")) + "\\"
sourcePath = rootPath + "source\\"
Words = []  # 全词典

with open(sourcePath + "words.txt", "r", encoding="utf-8") as source:
    for w in source:
        wordline = w.split("\t")
        wordline = list(map(str.strip, wordline))
        Words.append(wordline[:-1])

print(Words)
print(len(Words))

import logging
import gensim
from gensim.models import word2vec
# 设置输出日志
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# 直接用gensim提供的API去读取txt文件，读取文件的API有LineSentence 和 Text8Corpus, PathLineSentences等。
sentences = Words
# 训练模型，词向量的长度设置为200， 迭代次数为8，采用skip-gram模型，模型保存为bin格式
model = gensim.models.Word2Vec(sentences, size=200, sg=1, iter=8)
model.wv.save_word2vec_format("./word2Vec" + ".bin", binary=True)
# 加载bin格式的模型
wordVec = gensim.models.KeyedVectors.load_word2vec_format("word2Vec.bin", binary=True)


print(type(wordVec))
