import time
import os
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
###urls城市根据自己所处地理位置修改
urls = [
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hhbmdzaGEi",  # changsha 长沙
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemh1emhvdSI%3D",  # zhuzhou 株洲
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGVuZ3lhbmci",  # hengyang 衡阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieXVleWFuZyI%3D",  # yueyang 岳阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieWl5YW5nIg%3D%3D",  # yiyang 益阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemh1emhvdSI%3D",  # zhuzhou 株洲
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaHVhaWh1YSI%3D",  # huaihua 怀化
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibG91ZGki",  # loudi 娄底
]

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/ZHGXTV/Public/json/live_interface.txt"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls


def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=1)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


results = []

for url in urls:
    try:
        # 创建一个Chrome WebDriver实例
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    
        driver = webdriver.Chrome(options=chrome_options)
        # 使用WebDriver访问网页
        driver.get(url)  # 将网址替换为你要访问的网页地址
        time.sleep(10)
        # 获取网页内容
        page_content = driver.page_source
    
        # 关闭WebDriver
        driver.quit()
    
        # 查找所有符合指定格式的网址
        pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
        urls_all = re.findall(pattern, page_content)
        # urls = list(set(urls_all))  # 去重得到唯一的URL列表
        urls = set(urls_all)  # 去重得到唯一的URL列表
        x_urls = []
        for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
            url = url.strip()
            ip_start_index = url.find("//") + 2
            ip_end_index = url.find(":", ip_start_index)
            ip_dot_start = url.find(".") + 1
            ip_dot_second = url.find(".", ip_dot_start) + 1
            ip_dot_three = url.find(".", ip_dot_second) + 1
            base_url = url[:ip_start_index]  # http:// or https://
            ip_address = url[ip_start_index:ip_dot_three]
            port = url[ip_end_index:]
            ip_end = "1"
            modified_ip = f"{ip_address}{ip_end}"
            x_url = f"{base_url}{modified_ip}{port}"
            x_urls.append(x_url)
        urls = set(x_urls)  # 去重得到唯一的URL列表
    
        valid_urls = []
        #   多线程获取可用url
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = []
            for url in urls:
                url = url.strip()
                modified_urls = modify_urls(url)
                for modified_url in modified_urls:
                    futures.append(executor.submit(is_url_accessible, modified_url))
    
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    valid_urls.append(result)
    
        for url in valid_urls:
            print(url)
        # 遍历网址列表，获取JSON文件并解析
        for url in valid_urls:
            try:
                # 发送GET请求获取JSON文件，设置超时时间为0.5秒
                json_url = f"{url}"
                response = requests.get(json_url, timeout=1)
                json_data = response.content.decode('utf-8')
                try:
                    # 按行分割数据
                    lines = json_data.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line:
                            name, channel_url = line.split(',')
                            urls = channel_url.split('/', 3)
                            url_data = json_url.split('/', 3)
                            if len(urls) >= 4:
                                urld = (f"{urls[0]}//{url_data[2]}/{urls[3]}")
                            else:
                                urld = (f"{urls[0]}//{url_data[2]}")
                            print(f"{name},{urld}")
                            if name and urld:
                                # 删除特定文字
                                name = name.replace("cctv", "CCTV")
                                name = name.replace("中央", "CCTV")
                                name = name.replace("央视", "CCTV")
                                name = name.replace("高清", "")
                                name = name.replace("超高", "")
                                name = name.replace("HD", "")
                                name = name.replace("标清", "")
                                name = name.replace("频道", "")
                                name = name.replace("-", "")
                                name = name.replace(" ", "")
                                name = name.replace("PLUS", "+")
                                name = name.replace("＋", "+")
                                name = name.replace("(", "")
                                name = name.replace(")", "")
                                name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                                name = name.replace("CCTV1综合", "CCTV1")
                                name = name.replace("CCTV2财经", "CCTV2")
                                name = name.replace("CCTV3综艺", "CCTV3")
                                name = name.replace("CCTV4国际", "CCTV4")
                                name = name.replace("CCTV4中文国际", "CCTV4")
                                name = name.replace("CCTV4欧洲", "CCTV4")
                                name = name.replace("CCTV5体育", "CCTV5")
                                name = name.replace("CCTV6电影", "CCTV6")
                                name = name.replace("CCTV7军事", "CCTV7")
                                name = name.replace("CCTV7军农", "CCTV7")
                                name = name.replace("CCTV7农业", "CCTV7")
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
                                name = name.replace("CCTV17农业", "CCTV17")
                                name = name.replace("CCTV5+体育赛视", "CCTV5+")
                                name = name.replace("CCTV5+体育赛事", "CCTV5+")
                                name = name.replace("CCTV5+体育", "CCTV5+")
                                results.append(f"{name},{urld}")
                except:
                    continue
            except:
                continue
    except:
        continue

results = set(results)   # 去重得到唯一的URL列表
results = sorted(results)
with open("itv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")
        print(result)
