from jackfrank.utils.ip_getter import get_ip
from jackfrank.utils.ip_getter import ip_test
from jackfrank.utils.ip_getter import choose_ip
from jackfrank.utils.mysql_connection import get_info_sql
from jackfrank.utils.mysql_connection import test_sql
from jackfrank.functions.spider import read_url
from jackfrank.functions.spider import get_movie_list
from jackfrank.functions.spider import get_info_txt
from jackfrank.functions.spider import get_coms
from jackfrank.functions.spider import get_com


if __name__ == '__main__':
    ip_list = get_ip()  # 获取代理ip_list
    ip = choose_ip(ip_list)  # 选择可用的高匿代理ip
    url_list = read_url()  # 读取网页url_list
    # get_info_txt(ip,url_list)  #读取电影基本信息并写入movie.txt文件
    # get_com(ip,url_list[0])   #获取指定电影的200条评论
    # get_info_sql(ip,url_list)

    movie_info = get_movie_list()
    get_coms(ip, url_list, movie_info)  #获取电影评论

    print("success!")