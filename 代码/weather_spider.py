#-*- coding: utf-8 -*-
import requests  # 模拟浏览器进行网络请求
from lxml import etree  # 进行数据预处理
import csv  # 写入csv文件

def getWeather(url):
    weather_info = []   # 新建一个列表,将爬取的每月数据放进去
    # 请求头信息:浏览器版本型号,接收数据的编码格式
    headers = {
        # 必填,不填拿不到数据
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'
    }
    # 请求 接收到了响应数据
    resp = requests.get(url, headers=headers)
    # 数据预处理
    resp_html = etree.HTML(resp.text)
    # xpath提取所有数据
    resp_list = resp_html.xpath("//ul[@class='thrui']/li")
    # for循环迭代遍历
    for li in resp_list:
        day_weather_info = {}
        # 日期
        day_weather_info['date_time'] = li.xpath("./div[1]/text()")[0].split(' ')[0]
        # 最高气温 (包含摄氏度符号)
        high = li.xpath("./div[2]/text()")[0]
        day_weather_info['high'] = high[:high.find('℃')]
        # 最低气温
        low = li.xpath("./div[3]/text()")[0]
        day_weather_info['low'] = low[:low.find('℃')]
        # 天气
        day_weather_info['weather'] = li.xpath("./div[4]/text()")[0]
        weather_info.append(day_weather_info)
    return weather_info


weathers = []

# for循环生成有顺序的1-12
for month in range(1, 13):
    # 获取某一月的天气信息
    # 三元表达式
    weather_time = '2024' + ('0' + str(month) if month < 10 else str(month))
    print(weather_time)
    url = f'https://lishi.tianqi.com/changsha/{weather_time}.html'
    # 爬虫获取这个月的天气信息
    weather = getWeather(url)
    # 存到列表中
    weathers.append(weather)
print(weathers)


# 数据写入(一次性写入)
with open("weather.csv", "w",newline='') as csvfile:
    writer = csv.writer(csvfile)
    # 先写入列名:columns_name 日期 最高气温 最低气温  天气
    writer.writerow(["日期", "最高气温", "最低气温", '天气'])
    # 一次写入多行用writerows(写入的数据类型是列表,一个列表对应一行)
    writer.writerows([list(day_weather_dict.values()) for month_weather in weathers for day_weather_dict in month_weather])
