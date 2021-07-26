# -*-coding:UTF-8-*-
import json
import jieba

# for i in range(20):
#     word, count = items[i]
#     words.append(items[i])
#     print(word, count)
#

words=[]
words.append(["断崖式衰退", 100])
words.append(["九七回归", 81])
words.append(["经典", 76])
words.append(["演技差", 56])
words.append(["流量明星", 47])
words.append(["张国荣", 60])
words.append( ["周星驰", 54])
words.append( ["大跌", 69])
words.append( ["回忆", 46])
words.append(  ["电影中心", 50])
words.append(  ["古天乐", 27])
words.append(  ["好莱坞", 34])
words.append(  ["无间道", 29])
words.append(  ["内忧外患", 31])
words.append(  ["日渐式微", 18])
words.append(  ["特效", 20])
words.append(  ["价值观", 29])
words.append(  ["审美", 18])
words.append(  ["美国", 36])
words.append(  ["港片", 48])






# coding=utf-8
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

# 渲染图
def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100], shape='diamond')  # SymbolType.ROUND_RECT
        .set_global_opts(title_opts=opts.TitleOpts(title='WordCloud词云'))
    )
    return c

# 生成图
wordcloud_base().render('./词云图.html')

