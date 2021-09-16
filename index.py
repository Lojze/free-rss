import requests
from bs4 import BeautifulSoup
import pprint
import json
import hashlib
import random
import datetime
import time

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

def baiduAPI_translate(query_str):
    # 你的APP ID
    appID = ''
    # 你的密钥
    secretKey = ''
    # 百度翻译 API 的 HTTP 接口
    apiURL = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    to_lang = "zh"

    # 生成随机的 salt 值
    salt = str(random.randint(32768, 65536))
    # 准备计算 sign 值需要的字符串
    pre_sign = appID + query_str + salt + secretKey
    # 计算 md5 生成 sign
    sign = hashlib.md5(pre_sign.encode()).hexdigest()
    # 请求 apiURL 所有需要的参数
    params = {
        'q': query_str,
        'from': 'auto',
        'to': to_lang,
        'appid': appID,
        'salt':salt,
        'sign': sign
    }

    try:
        # 直接将 params 和 apiURL 一起传入 requests.get() 函数
        response = requests.get(apiURL, params=params)
        # 获取返回的 json 数据
        result_dict = response.json()
        # 得到的结果正常则 return
        if 'trans_result' in result_dict:
            dst = result_dict['trans_result'][0]['dst']
            # print(dst)
            return dst
    except Exception as e:
        print('Some errors occured: ', e)

response = requests.get("https://")
soup = BeautifulSoup(response.content, 'html.parser')

list = soup.select('h2,div.table')

dataList = []
data = []

temp = None
for tag in list:
    if tag.name == 'h2':
        time.sleep(1)
        temp = {
            "title": baiduAPI_translate(tag.get_text().strip()),
            # "title":tag.get_text().strip(),
            "items": []
        }
        data.append(temp)
    else:
        for card in tag:
            time.sleep(1)
            temp["items"].append({
                "text": baiduAPI_translate(card.find(class_="idea").get_text().strip()),
                # "text": card.find(class_="idea").get_text().strip(),
                "votes": card.find(class_="votes").get("data-votes"),
                "action": card.find(class_="action-upvote").get("data-id")
            })


# pprint.pprint(data)

def dict2json(file_name, the_dict):
    '''
    将字典文件写如到json文件中
    :param file_name: 要写入的json文件名(需要有.json后缀),str类型
    :param the_dict: 要写入的数据，dict类型
    :return: 1代表写入成功,0代表写入失败
    '''
    try:
        json_str = json.dumps(the_dict, ensure_ascii=False,indent=4)
        # with open(file_name, 'a', encoding="utf-8") as json_file:
        #     json_file.write(json_str + ',')
        with open(file_name, 'r+', encoding="utf-8") as json_file:
            old = json_file.read()
            json_file.seek(0)
            json_file.write(json_str)
            json_file.write(old)
        return 1
    except:
        return 0

# print(data)

dict2json("idea.json", {"now_time":now_time,"data":data})
