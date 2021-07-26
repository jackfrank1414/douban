import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random
import xlrd
from xlutils.copy import copy
from jackfrank.utils.send_message import send_msg

def read_url():
    print("正在读取电影链接...")
    n = 'None\n'
    url_list = []
    with open('./move.txt','r',encoding='utf-8') as fp:
        data = fp.readlines()
        for line in data:
            if (line == n):
                continue
            for i in range(0,len(eval(line)),1):
                # print(eval(line)[i].get("url"))
                url_list.append(eval(line)[i].get("url"))
    fp.close()
    return url_list

def get_movie_list():
    print("正在读取电影名称...")
    n = 'None\n'
    name_list = []
    count = 1
    with open('./move.txt', 'r', encoding='utf-8') as fp:
        data = fp.readlines()
        for line in data:
            if (line == n):
                continue
            for i in range(0, len(eval(line)), 1):
                # print(eval(line)[i].get("url"))
                data = {'id': 0,'title':''}
                data['id'] = count*(i+1)
                data['title'] = eval(line)[i].get("title")
                name_list.append(data)
            count += 1
    fp.close()
    return name_list

def get_info_txt(ip,url_list):
    print("开始爬取电影相关信息...")
    headers = {
        'User-Agent': UserAgent().random
    }
    proxies = {'http' : ip}

    excel = xlrd.open_workbook('../案.xls',formatting_info=True)
    excel1 = copy(excel)

    # 调用对象的add_sheet方法
    sheet = excel1.get_sheet(0)

    for id in range(1,100):
        if ((id + 1) % 15 == 0):
            time.sleep(random.uniform(10.5, 15.5))
            send_msg(str(id+1))
        if ((id + 1) % 100 == 0):

            time.sleep(random.uniform(30.5, 45.5))
        url = url_list[id]
        print(url + " " + str(id+1))
        html = requests.get(url,headers=headers,proxies=proxies)
        soup = BeautifulSoup(html.text,"html.parser")
        soup1 = BeautifulSoup(str(soup.select('#info')), "html.parser")

        #获取电影名称、日期、评分信息
        title = soup.select('#wrapper #content h1 span')[0].text
        year = soup.select('#wrapper #content h1 span')[1].text
        rate = soup.select('#interest_sectl .rating_wrap.clearbox .rating_self.clearfix strong')[0].text

        #获取导演信息
        daoyan = soup1.find_all('a',rel="v:directedBy")
        director = ''
        for i in range(0,len(daoyan)):
            if (i != (len(daoyan) - 1)):
                director = director + soup1.find_all('a',rel="v:directedBy")[i].text + " / "
            else:
                director = director + soup1.find_all('a',rel="v:directedBy")[i].text

        #获取编剧信息，如没有则为空
        playwright = ''
        if ((soup.select('#info .pl')[1].text) == '编剧'):
            playwright = soup.select('#info .attrs')[1].text
        else:
            playwright = ''

        #获取演员信息
        yanyuan = soup1.find_all('a',rel="v:starring")
        actors = ''
        for i in range(0,len(yanyuan)):
            if (i != (len(yanyuan) - 1)):
                actors = actors + soup1.find_all('a',rel="v:starring")[i].text + " / "
            else:
                actors = actors + soup1.find_all('a',rel="v:starring")[i].text

        #获取电影类型信息
        types = soup1.find_all('span',property='v:genre')
        classification = ''
        for i in range(0,len(types)):
            if (i != (len(types) - 1)):
                classification = classification + soup1.find_all('span',property='v:genre')[i].text + " / "
            else:
                classification = classification + soup1.find_all('span',property='v:genre')[i].text

        #获取电影上映时间信息
        times = soup1.find_all('span',property="v:initialReleaseDate")
        showtime = ''
        for j in range(0,len(times)):
            if (j != (len(times) - 1)):
                showtime = showtime + soup1.find_all('span',property='v:initialReleaseDate')[j].text + " / "
            else:
                showtime = showtime + soup1.find_all('span',property='v:initialReleaseDate')[j].text

        #获取电影时长，如为连续剧则为空
        duration = ''
        try:
            duration = soup1.find_all('span',property="v:runtime")[0].text
        except IndexError as e:
            duration = ''

        watched = ''
        wanted = ''
        watched = soup.select('.subject-others-interests-ft a')[0].text
        wanted = soup.select('.subject-others-interests-ft a')[1].text

        #打印电影相关信息
        info = soup1.getText().replace('[\n','')
        info = info.replace(']','')

        #将电影基本信息写入movie.txt文件
        # with open('./movie.txt','a',encoding='utf-8') as fp:
        #     fp.write(title + ' ' + year + '\n')
        #     fp.write("评分: " + rate + '\n')
        #     fp.write(info + '\n')

        #将电影信息写入到Excel表中
        # 创建我们需要的第一行的标头数据
        heads = ['movie_id', 'title', 'year', 'rate', 'director', 'playwright', 'actors', 'classification', 'showtime',
                 'duration','watched','wanted']
        if (id == 0):
            ls = 0
            # 将标头循环写入表中
            for head in heads:
                sheet.write(0, ls, head)
                ls += 1

        data = [id+1, title, year, rate, director, playwright, actors, classification, showtime, duration, watched, wanted]

        # 将数据分两次循环写入表中 外围循环行
        for j in range(0,len(heads),1):
            sheet.write(id+1,j,data[j])
            # 最后将文件save保存
            excel1.save('./案例.xls')

        time.sleep(random.uniform(3.5,5.5))

def get_com(ip,url,name):
    print("开始爬取评论review_list...")
    headers = {
        'User-Agent': UserAgent().random
    }
    proxies = {'http': ip}
    url_new = url + 'reviews'
    path = './coms/' + name + '.txt'

    #读取指定电影的200条评论：review_list
    review_list = []
    for i in range(0,200,20):
        params = {
            'start' : i
        }
        html = requests.get(url_new,params=params,headers=headers,proxies=proxies)
        soup = BeautifulSoup(html.text,"html.parser")
        review_list_sign = soup.select('.review-list div .main.review-item')
        for j in range(0,len(review_list_sign),1):
            review_list.append(review_list_sign[j]['id'])
            print(review_list_sign[j]['id'])
        time.sleep(random.uniform(3.5, 5.5))
        if i % 50 == 0:
            time.sleep(random.uniform(10, 15.5))

    time.sleep(65)
    #获得这200个用户对该作品的评论
    print("开始爬取该电影评论...")
    s1 = 'https://movie.douban.com/review/'
    for k in range(0,len(review_list),1):
        print(str(k)+":"+name)
        url_new2 = s1 + str(review_list[k]) +'/'
        html1 = requests.get(url_new2,headers=headers,proxies=proxies)
        soup_pl = BeautifulSoup(html1.text,"html.parser")
        txt = soup_pl.select('#link-report .review-content.clearfix p')
        txts = ''
        for t in range(0,len(txt),1):
            txts = txts + txt[t].text
        with open(path, 'a', encoding='utf-8') as fp:
            fp.write(txts + '\n')
        time.sleep(random.uniform(3.0, 4.5))
        if k % 50 == 0:
            time.sleep(random.uniform(10, 15.5))


def get_coms(ip,url_list,movie_info):
    for i in range(14,100):
        # send_msg('开始爬取电影：'+movie_info[i].get('title')+'的评论...')
        get_com(ip,url_list[i],movie_info[i].get('title'))