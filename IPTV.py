import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import re

hebei = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iSGViZWki" #河北
beijing = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iYmVpamluZyI%3D" #北京
guangdong = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iZ3Vhbmdkb25nIg%3D%3D" #广东
shanghai = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ic2hhbmdoYWki" #上海
tianjin = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0idGlhbmppbiI%3D" #天津
chongqing = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iY2hvbmdxaW5nIg%3D%3D" #重庆
shanxi = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ic2hhbnhpIg%3D%3D" #山西
shaanxi = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhYW54aSI%3D" #陕西
liaoning = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ibGlhb25pbmci" #辽宁
jiangsu = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iamlhbmdzdSI%3D" #江苏
zhejiang = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iemhlamlhbmci" #浙江
anhui = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5a6J5b69Ig%3D%3D" #安徽
fujian = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iRnVqaWFuIg%3D%3D" #福建
jiangxi = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rGf6KW%2FIg%3D%3D" #江西
shandong = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5bGx5LicIg%3D%3D" #山东
henan = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rKz5Y2XIg%3D%3D" #河南
hubei = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5YyXIg%3D%3D" #湖北
hunan = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5Y2XIg%3D%3D" #湖南

def process_url(url):
# 创建一个Chrome WebDriver实例
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
# 使用WebDriver访问网页
driver.get(url) # 将网址替换为你要访问的网页地址
time.sleep(10)
# 获取网页内容
page_content = driver.page_source

# 关闭WebDriver
driver.quit()

# 查找所有符合指定格式的网址
pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+" # 设置匹配的格式，如http://8.8.8.8:8888
urls_all = re.findall(pattern, page_content)
urls = list(set(urls_all)) # 去重得到唯一的URL列表
for url in urls:
print(url)
# 遍历网址列表，获取JSON文件并解析
results = []
for url in urls:
try:
# 发送GET请求获取JSON文件，设置超时时间为5秒
json_url = f"{url}/iptv/live/1000.json?key=txiptv"
response = requests.get(json_url, timeout=3)
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
name = name.replace("HD", "")
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
name = name.replace("CCTV4中文国际", "CCTV4")
name = name.replace("CCTV5体育", "CCTV5")
name = name.replace("CCTV6电影", "CCTV6")
name = name.replace("CCTV7军事", "CCTV7")
name = name.replace("CCTV7军农", "CCTV7")
name = name.replace("CCTV7国防军事", "CCTV7")
name = name.replace("CCTV8电视剧", "CCTV8")
name = name.replace("CCTV9记录", "CCTV9")
name = name.replace("CCTV9纪录", "CCTV9")
name = name.replace("CCTV10科教", "CCTV10")
name = name.replace("CCTV11戏曲", "CCTV11")
name = name.replace("CCTV12社会与法", "CCTV12")
name = name.replace("CCTV13新闻", "CCTV13")
name = name.replace("CCTV新闻", "CCTV13")
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

return results
def save_results(results, filename):
# 将结果保存到文本文件
with open(filename, "w", encoding="utf-8") as file:
for result in results:
file.write(result + "\n")
print(result)

# 处理第1个URL
results_hebei = process_url(hebei)
save_results(results_hebei, "hebei.txt")

# 处理第2个URL
results_beijing = process_url(beijing)
save_results(results_beijing, "beijing.txt")

# 处理第3个URL
results_guangdong = process_url(guangdong)
save_results(results_guangdong, "guangdong.txt")

# 处理第4个URL
results_shanghai = process_url(shanghai)
save_results(results_shanghai, "shanghai.txt")

# 处理第5个URL
results_tianjin = process_url(tianjin)
save_results(results_tianjin, "tianjin.txt")

# 处理第6个URL
results_chongqing = process_url(chongqing)
save_results(results_chongqing, "chongqing.txt")

# 处理第7个URL
results_shanxi = process_url(shanxi)
save_results(results_shanxi, "shanxi.txt")

# 处理第8个URL
results_shaanxi = process_url(shaanxi)
save_results(results_shaanxi, "shaanxi.txt")

# 处理第9个URL
results_liaoning = process_url(liaoning)
save_results(results_liaoning, "liaoning.txt")

# 处理第10个URL
results_jiangsu = process_url(jiangsu)
save_results(results_jiangsu, "jiangsu.txt")

# 处理第11个URL
results_zhejiang = process_url(zhejiang)
save_results(results_zhejiang, "zhejiang.txt")

# 处理第12个URL
results_anhui = process_url(anhui)
save_results(results_anhui, "anhui.txt")

# 处理第13个URL
results_fujian = process_url(fujian)
save_results(results_fujian, "fujian.txt")

# 处理第14个URL
results_jiangxi = process_url(jiangxi)
save_results(results_jiangxi, "jiangxi.txt")

# 处理第15个URL
results_shandong = process_url(shandong)
save_results(results_shandong, "shandong.txt")

# 处理第16个URL
results_henan = process_url(henan)
save_results(results_henan, "henan.txt")

# 处理第17个URL
results_hubei = process_url(hubei)
save_results(results_hubei, "hubei.txt")

# 处理第18个URL
results_hunan = process_url(hunan)
save_results(results_hunan, "hunan.txt")

# 合并文件内容
file_contents = []
file_paths = ["hebei.txt", "beijing.txt", "guangdong.txt", "shanghai.txt", "tianjin.txt", "chongqing.txt", "shanxi.txt", "shaanxi.txt", "liaoning.txt", "jiangsu.txt", "zhejiang.txt", "anhui.txt", "fujian.txt", "jiangxi.txt", "shandong.txt", "henan.txt", "hubei.txt", "hunan.txt"] # 替换为实际的文件路径列表
for file_path in file_paths:
with open(file_path, 'r', encoding="utf-8") as file:
content = file.read()
file_contents.append(content)

# 写入合并后的文件
with open("IPTV.txt", "w", encoding="utf-8") as output:
output.write('\n'.join(file_contents))