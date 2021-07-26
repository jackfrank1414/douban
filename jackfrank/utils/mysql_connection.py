import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random
import pymysql

def test_sql():
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='test')
    cur = conn.cursor()
    cur.execute("INSERT INTO url_list (url, name) VALUES ('www.baidu.com', 'This is content.')")
    cur.close()
    conn.commit()
    conn.close()

def get_info_sql(ip,url_list):
    print("开始爬取电影相关信息...")
    headers = {
        'User-Agent': UserAgent().random
    }
    proxies = {'http': ip}

    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='test')

    for id in range(0, 5, 1):
        url = url_list[id]
        print(url + " " + str(id + 1))
        html = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(html.text, "html.parser")
        soup1 = BeautifulSoup(str(soup.select('#info')), "html.parser")

        # 获取电影名称、日期、评分信息
        title = soup.select('#wrapper #content h1 span')[0].text
        year = soup.select('#wrapper #content h1 span')[1].text
        rate = soup.select('#interest_sectl .rating_wrap.clearbox .rating_self.clearfix strong')[0].text

        # 获取导演信息
        daoyan = soup1.find_all('a', rel="v:directedBy")
        director = ''
        for i in range(0, len(daoyan)):
            if (i != (len(daoyan) - 1)):
                director = director + soup1.find_all('a', rel="v:directedBy")[i].text + " / "
            else:
                director = director + soup1.find_all('a', rel="v:directedBy")[i].text

        # 获取编剧信息，如没有则为空
        playwright = ''
        if ((soup.select('#info .pl')[1].text) == '编剧'):
            playwright = soup.select('#info .attrs')[1].text
        else:
            playwright = ''

        # 获取演员信息
        yanyuan = soup1.find_all('a', rel="v:starring")
        actors = ''
        for i in range(0, len(yanyuan)):
            if (i != (len(yanyuan) - 1)):
                actors = actors + soup1.find_all('a', rel="v:starring")[i].text + " / "
            else:
                actors = actors + soup1.find_all('a', rel="v:starring")[i].text

        # 获取电影类型信息
        types = soup1.find_all('span', property='v:genre')
        classification = ''
        for i in range(0, len(types)):
            if (i != (len(types) - 1)):
                classification = classification + soup1.find_all('span', property='v:genre')[i].text + " / "
            else:
                classification = classification + soup1.find_all('span', property='v:genre')[i].text

        # 获取电影上映时间信息
        times = soup1.find_all('span', property="v:initialReleaseDate")
        showtime = ''
        for j in range(0, len(times)):
            if (j != (len(times) - 1)):
                showtime = showtime + soup1.find_all('span', property='v:initialReleaseDate')[j].text + " / "
            else:
                showtime = showtime + soup1.find_all('span', property='v:initialReleaseDate')[j].text

        # 获取电影时长，如为连续剧则为空
        duration = ''
        try:
            duration = soup1.find_all('span', property="v:runtime")[0].text
        except IndexError as e:
            duration = ''

        print(title)
        cur = conn.cursor()
        query = "INSERT INTO movie_info (title, year, rate, director, playwright, actors, classification, showtime, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (title, year, rate, director, playwright, actors, classification, showtime, duration)
        cur.execute(query,values)
        cur.close()

        time.sleep(random.uniform(1.5, 2.5))
        if ((id + 1) % 20 == 0):
            time.sleep(random.uniform(10.5, 15.5))
    conn.commit()
    conn.close()