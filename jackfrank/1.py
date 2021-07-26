import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from jackfrank.utils.ip_getter import get_ip
from jackfrank.utils.ip_getter import choose_ip
import xlrd
from xlutils.copy import copy
import time
import random

url = "https://movie.douban.com/top250"

for i in range(0, 250, 25):
    ip_list = get_ip()  # 获取代理ip_list
    ip = choose_ip(ip_list)  # 选择可用的高匿代理ip
    headers = {
        'User-Agent': UserAgent().random
    }
    proxies = {'http': ip}
    params = {
        'start': i,
        'filter': ''
    }
    html = requests.get(url, headers=headers, proxies=proxies, params=params)
    soup = BeautifulSoup(html.text, "html.parser")

    excel = xlrd.open_workbook('./top250.xls', formatting_info=True)
    excel1 = copy(excel)

    # 调用对象的add_sheet方法
    sheet = excel1.get_sheet(0)

    for j in range(0, 25, 1):
        href = soup.select('.info .hd a')[j]['href']
        html0 = requests.get(href, headers=headers, proxies=proxies)
        soup0 = BeautifulSoup(html0.text, "html.parser")
        soup1 = BeautifulSoup(str(soup0.select('#info')), "html.parser")

        # 获取电影名称、日期、评分信息
        title = soup0.select('#wrapper #content h1 span')[0].text
        year = soup0.select('#wrapper #content h1 span')[1].text
        rate = soup0.select('#interest_sectl .rating_wrap.clearbox .rating_self.clearfix strong')[0].text

        # 获取导演信息
        daoyan = soup1.find_all('a', rel="v:directedBy")
        director = ''
        for k in range(0, len(daoyan)):
            if k != (len(daoyan) - 1):
                director = director + soup1.find_all('a', rel="v:directedBy")[k].text + " / "
            else:
                director = director + soup1.find_all('a', rel="v:directedBy")[k].text

        # 获取编剧信息，如没有则为空
        playwright = ''
        if soup0.select('#info .pl')[1].text == '编剧':
            playwright = soup0.select('#info .attrs')[1].text
        else:
            playwright = ''

        # 获取演员信息
        yanyuan = soup1.find_all('a', rel="v:starring")
        actors = ''
        for k in range(0, len(yanyuan)):
            if k != (len(yanyuan) - 1):
                actors = actors + soup1.find_all('a', rel="v:starring")[k].text + " / "
            else:
                actors = actors + soup1.find_all('a', rel="v:starring")[k].text

        # 获取电影类型信息
        types = soup1.find_all('span', property='v:genre')
        classification = ''
        for k in range(0, len(types)):
            if k != (len(types) - 1):
                classification = classification + soup1.find_all('span', property='v:genre')[k].text + " / "
            else:
                classification = classification + soup1.find_all('span', property='v:genre')[k].text

        # 获取电影上映时间信息
        times = soup1.find_all('span', property="v:initialReleaseDate")
        showtime = ''
        for k in range(0, len(times)):
            if k != (len(times) - 1):
                showtime = showtime + soup1.find_all('span', property='v:initialReleaseDate')[k].text + " / "
            else:
                showtime = showtime + soup1.find_all('span', property='v:initialReleaseDate')[k].text

        # 获取电影时长，如为连续剧则为空
        duration = ''
        try:
            duration = soup1.find_all('span', property="v:runtime")[0].text
        except IndexError as e:
            duration = ''

        watched = ''
        wanted = ''
        watched = soup0.select('.subject-others-interests-ft a')[0].text
        wanted = soup0.select('.subject-others-interests-ft a')[1].text

        # 打印电影相关信息
        info = soup1.getText().replace('[\n', '')
        info = info.replace(']', '')

        # 将电影基本信息写入movie.txt文件
        # with open('./movie.txt','a',encoding='utf-8') as fp:
        #     fp.write(title + ' ' + year + '\n')
        #     fp.write("评分: " + rate + '\n')
        #     fp.write(info + '\n')

        # 将电影信息写入到Excel表中
        # 创建我们需要的第一行的标头数据
        heads = ['movie_id', 'title', 'year', 'rate', 'director', 'playwright', 'actors', 'classification', 'showtime',
                 'duration', 'watched', 'wanted']
        if j == 0:
            ls = 0
            # 将标头循环写入表中
            for head in heads:
                sheet.write(0, ls, head)
                ls += 1

        data = [j + 1 + i, title, year, rate, director, playwright, actors, classification, showtime, duration, watched,
                wanted]

        # 将数据分两次循环写入表中 外围循环行
        for l in range(0, len(heads), 1):
            sheet.write(j + 1 + i, l, data[l])
            # 最后将文件save保存
            excel1.save('./top250.xls')
    # time.sleep(random.uniform(13.5, 35.5))
