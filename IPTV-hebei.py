import time
from selenium import webdriver
import requests
import json
import re

url = "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22%E6%B2%B3%E5%8C%97%22"
#url = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iSGViZWki"

# 使用webdriver_manager自动下载和管理chromedriver
driver = webdriver.Chrome()

# 使用WebDriver访问网页
driver.get(url)  # 将网址替换为你要访问的网页地址
time.sleep(10)
# 获取网页内容
page_content = driver.page_source

# 关闭WebDriver
driver.quit()

# 查找所有符合指定格式的网址
pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
urls = re.findall(pattern, page_content)
#print(urls)
# 遍历网址列表，获取JSON文件并解析
results = []
for url in urls:
    try:
        # 发送GET请求获取JSON文件，设置超时时间为5秒
        json_url = f"{url}/iptv/live/1000.json?key=txiptv"
        response = requests.get(json_url, timeout=5)
        json_data = response.json()

        # 解析JSON文件，获取name和url字段
        for item in json_data['data']:
            if isinstance(item, dict):
                name = item.get('name')
                urlx = item.get('url')
                urld = f"{url}{urlx}"

                if name and urlx:
                    # 删除特定文字
                    name = name.replace("中央", "CCTV")
                    name = name.replace("高清", "")
                    name = name.replace("标清", "")
                    name = name.replace("频道", "")
                    name = name.replace("-", "")
                    name = name.replace(" ", "")
                    name = name.replace("PLUS", "+")
                    name = name.replace("(", "")
                    name = name.replace(")", "")

                    name = name.replace("CCTV1综合", "CCTV1")
                    name = name.replace("CCTV2财经", "CCTV2")
                    name = name.replace("CCTV3综艺", "CCTV3")
                    name = name.replace("CCTV4国际", "CCTV4")
                    name = name.replace("CCTV5体育", "CCTV5")
                    name = name.replace("CCTV6电影", "CCTV6")
                    name = name.replace("CCTV7军事", "CCTV7")
                    name = name.replace("CCTV7军农", "CCTV7")
                    name = name.replace("CCTV8电视剧", "CCTV8")
                    name = name.replace("CCTV9记录", "CCTV9")
                    name = name.replace("CCTV9纪录", "CCTV9")
                    name = name.replace("CCTV10科教", "CCTV10")
                    name = name.replace("CCTV11戏曲", "CCTV11")
                    name = name.replace("CCTV12社会与法", "CCTV12")
                    name = name.replace("CCTV13新闻", "CCTV13")
                    name = name.replace("CCTV14少儿", "CCTV14")
                    name = name.replace("CCTV15音乐", "CCTV15")
                    name = name.replace("CCTV16奥林匹克", "CCTV16")
                    name = name.replace("CCTV17农业农村", "CCTV17")
                    name = name.replace("CCTV5+体育赛视", "CCTV5+")
                    name = name.replace("CCTV5+体育赛事", "CCTV5+")
                    results.append(f"{name},{urld}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to process JSON for URL {json_url}. Error: {str(e)}")
        continue
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON for URL {url}. Error: {str(e)}")
        continue

# 将结果保存到文本文件
with open("iptv_hebei.txt", "w", encoding="utf-8") as file:
    for result in results:
        file.write(result + "\n")

# 打印结果
#for result in results:
    #print(result)
