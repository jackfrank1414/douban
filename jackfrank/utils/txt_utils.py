def read_name():
    print("正在读取电影名称...")
    n = 'None\n'
    url_list = []
    with open('../move.txt','r',encoding='utf-8') as fp:
        data = fp.readlines()
        for line in data:
            if (line == n):
                continue
            for i in range(0,len(eval(line)),1):
                # print(eval(line)[i].get("url"))
                url_list.append(eval(line)[i].get("title"))
    fp.close()
    return url_list

def read_rate():
    print("正在读取电影评分...")
    n = 'None\n'
    url_list = []
    with open('../move.txt', 'r', encoding='utf-8') as fp:
        data = fp.readlines()
        for line in data:
            if (line == n):
                continue
            for i in range(0, len(eval(line)), 1):
                # print(eval(line)[i].get("url"))
                url_list.append(eval(line)[i].get("rate"))
    fp.close()
    return url_list

def is_chinese(uchar):
    if uchar >= '\u4e00' and uchar <= '\u9fa5' or uchar == '\n':
        return True
    else:
        return False

def reserve_chinese(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str += i
    return content_str