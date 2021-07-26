# -*-coding:UTF-8-*-
import json
import jieba

txt = open('../t/后翼弃兵.txt', 'rt', encoding='utf-8').read()
words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
counts = {}  # 通过键值对的形式存储词语及其出现的次数

for word in words:
    if len(word) == 1:  # 单个词语不计算在内
        continue
    else:
        counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

items = list(counts.items())  # 将键值对转换成列表
items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序
ite = json.dumps(items, ensure_ascii=False)
print(ite)
words = []

for i in range(20):
    word, count = items[i]
    words.append(items[i])
    print(word, count)

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
wordcloud_base().render('./词云图_后翼弃兵.html')

