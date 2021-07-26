import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random

url = 'https://www.zhihu.com/api/v4/questions/19595489/answers'
headers = {
        'User-Agent': UserAgent().random
    }
params = {
 'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,'
            'collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,'
            'attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,'
            'relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,'
            'is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data['
            '*].author.follower_count,badge[*].topics;data[*].settings.table_of_content.enabled',
 'limit': '5',
 'offset': '5',
 'platform': 'desktop',
 'sort_by': 'default'
}
html = requests.get(url,headers=headers,params=params)
print(html.text)