import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LotteryKiller.settings')
django.setup()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from killer.models import Result, Record


headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com/'
}
base_url = 'http://trend.caipiao.163.com/ssq/historyPeriod.html'


def get_html(payloads):
    try:
        response = requests.get(base_url, headers=headers, params=payloads)
        response.encoding = 'utf-8'
        response.raise_for_status()
    except requests.HTTPError:
        return "不成功的状态码" + response.status_code
    except requests.Timeout:
        return "请求超时"
    print("成功下载网页")
    return response.text


def parse_html(html, latest):
    bsObj = BeautifulSoup(html, 'lxml')
    data = bsObj.find_all(attrs={"data-period": re.compile(r"\d{7}")})  # list
    matrix = []  # 矩阵，每一行用于存储每一期的数据
    if not latest:
        for period in data:
            p_data = [int(number.string) for number in period if number.string not in [None, '\n']]
            matrix.append(p_data)
    else:
        p_data = [int(number.string) for number in data[-1] if number.string not in [None, '\n']]
        matrix.append(p_data)
    print("解析完成")
    return matrix


def store(lottery_matrix):
    result_names = ['period', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']
    for period in lottery_matrix:
        result_dict = dict(zip(result_names, period[0:8]))
        result = Result.objects.create(**result_dict)
    print("彩票开奖数据存储完成")
    time = datetime.now()
    begin_period = lottery_matrix[0][0]
    end_period = lottery_matrix[-1][0]
    begin = Result.objects.filter(period=begin_period)[0]
    end = Result.objects.filter(period=end_period)[0]
    Record.objects.create(time=time, begin_period=begin, end_period=end)
    print("该次爬取已记录")


def update_latest():
    latest_period = get_latest_period()
    latest_period += 1
    with open(r"./latest.txt", 'w') as f:
        f.write(str(latest_period))
    print("最新期已更新")


def get_latest_period():
    with open(r"./latest.txt", 'r') as f:
        latest_period = int(f.readline())
    return latest_period


def scrape():
    latest_period = get_latest_period()
    interval = {
        'beginPeriod': latest_period,
        'endPeriod': latest_period + 1
    }
    html = get_html(payloads=interval)
    data = parse_html(html, latest=True)
    store(data)
    update_latest()


def scrape_after_deploy():
    interval = {
        'beginPeriod': 2018058,
        'endPeriod': 2018090
    }
    html = get_html(payloads=interval)
    data = parse_html(html, latest=False)
    store(data)
