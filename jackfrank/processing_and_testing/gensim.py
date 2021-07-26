# coding=utf-8
import codecs
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary

fr = open('./后翼弃兵.txt', 'r', encoding='utf-8')
train = []
for line in fr.readlines():
    line = line.split(' ')
    train.append(line)

print(len(train))
# print (' '.join(train[2]))

dictionary = corpora.Dictionary(train)
corpus = [dictionary.doc2bow(text) for text in train]
lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=100)

topic_list = lda.print_topics(20)
print(type(lda.print_topics(20)))
print(len(lda.print_topics(20)))

for topic in topic_list:
    print(topic)
print("第一主题")
print(lda.print_topic(1))

print('给定一个新文档，输出其主题分布')

# test_doc = list(new_doc) #新文档进行分词
test_doc = train[0]  # 查看训练集中第三个样本的主题分布
doc_bow = dictionary.doc2bow(test_doc)  # 文档转换成bow
doc_lda = lda[doc_bow]  # 得到新文档的主题分布
# 输出新文档的主题分布
print(doc_lda)
for topic in doc_lda:
    print("%s\t%f\n" % (lda.print_topic(topic[0]), topic[1]))