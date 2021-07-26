import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

#获取代理ip列表
def get_ip():
    print("开始爬取代理ip_list...")
    url = 'https://ip.jiangxianli.com/?page='
    headers = {
        'User-Agent': UserAgent().random
    }

    ip_list = []
    for i in range(0,2,1):
        url_list = url + str(i+1)
        html = requests.get(url_list,headers=headers,verify=False)
        soup = BeautifulSoup(html.text,"html.parser")
        tr = soup.select('.layui-table tbody tr')
        for j in range(0,len(tr)):
            soup1 = BeautifulSoup(str(tr[j]),"html.parser")
            td = soup1.find_all('td')
            if ((td[2].text) == '高匿'):
                ip_list.append(soup1.select('td button')[0]["data-url"])
    return ip_list

#测试代理ip可用性
def ip_test(proxies):
    url = 'http://icanhazip.com'
    headers = {
        'User-Agent': UserAgent().random
    }
    try:
        response = requests.get(url,headers=headers,proxies=proxies,allow_redirects=False,timeout=5)  # 使用代理
        #print(response.status_code)
        if response.status_code == 200:
            return response.status_code
    except requests.ConnectionError as e:
        return -1
    except requests.exceptions.ReadTimeout as e:
        return -1

#选择可用的代理ip
def choose_ip(ip_list):
    print(ip_list)
    print("开始测试代理ip可行性...")
    for i in range(0,len(ip_list),1):
        proxies = {'http': ip_list[i]}
        print("第" + str(i+1) + "次测试:" + str(proxies))
        status_code = ip_test(proxies)
        if (status_code == 200):
            print("测试通过，该代理ip暂时可用！")
            return ip_list[i]
            break