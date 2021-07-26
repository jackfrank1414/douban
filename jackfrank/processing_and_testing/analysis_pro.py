from jackfrank.utils.Emotional_analysis import sentiment_score
from jackfrank.utils.txt_utils import read_name
from jackfrank.utils.txt_utils import read_rate
import xlrd
from xlutils.copy import copy

if __name__ == '__main__':
    # 生成stopword表，需要去除一些否定词和程度词汇
    stopwords = set()
    fr = open(r'G:\NLP二阶段\数据集\chinese_stop.txt', 'r', encoding='unicode_escape')
    for word in fr:
        stopwords.add(word.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
    # 读取否定词文件
    not_word_file = open(r'G:\NLP二阶段\工具包\情感极性词典\否定词.txt', 'r+', encoding='utf-8')
    not_word_list = not_word_file.readlines()
    not_word_list = [w.strip() for w in not_word_list]
    # 读取程度副词文件
    degree_file = open(r'G:\NLP二阶段\工具包\sentiment\程度级别词语（中文）.txt', 'r+')
    degree_list = degree_file.readlines()
    degree_list = [item.split(',')[0] for item in degree_list]
    # 生成新的停用词表
    with open('stopwords.txt', 'w', encoding='utf-8') as f:
        for word in stopwords:
            if (word not in not_word_list) and (word not in degree_list):
                f.write(word + '\n')

    name_list = read_name()
    rating_list = read_rate()
    for i in range(1,10):
        path = '../t/' + str(name_list[i]) + '.txt'
        f = open(path, "r", encoding='utf-8')
        lines = f.readlines()
        sum = 0
        point = 0
        n = 0
        for line in lines:
            if line != '\n':
                print(line, sentiment_score(line))
                sum = sum + sentiment_score(line)
                n += 1
        print(sum / n)
        excel = xlrd.open_workbook('./s.xls', formatting_info=True)
        excel1 = copy(excel)
        # 调用对象的add_sheet方法
        sheet = excel1.get_sheet(0)
        sheet.write(i+1,0,name_list[i])
        sheet.write(i+1, 1, sum/n)
        sheet.write(i+1,2,rating_list[i])
        # 最后将文件save保存
        excel1.save('./s.xls')
        f.close()



