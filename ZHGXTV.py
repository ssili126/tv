import time
import datetime
import concurrent.futures
import requests
import re
import os
import threading
from queue import Queue
import eventlet
eventlet.monkey_patch()


urls = [
"http://1.183.139.1:9001",
"http://1.183.141.1:8001",
"http://1.191.154.1:9000",
"http://1.191.155.1:9000",
"http://1.193.112.1:808",
"http://1.193.179.1:808",
"http://1.196.106.1:888",
"http://1.196.152.1:888",
"http://1.196.249.1:808",
"http://1.196.57.1:808",
"http://1.197.168.1:9999",
"http://1.197.251.1:885",
"http://1.197.34.1:808",
"http://1.199.136.1:8878",
"http://1.24.190.1:10080",
"http://1.24.190.1:10089",
"http://1.59.160.1:9000",
"http://1.59.161.1:9000",
"http://1.59.163.1:9000",
"http://1.59.164.1:9000",
"http://1.59.165.1:9000",
"http://1.59.167.1:9000",
"http://1.70.10.1:808",
"http://1.70.11.1:808",
"http://1.70.14.1:808",
"http://1.70.8.1:808",
"http://1.80.12.1:10000",
"http://1.87.218.1:7878",
"http://101.17.32.1:8899",
"http://101.18.25.1:808",
"http://101.18.30.1:808",
"http://101.224.201.1:12345",
"http://101.229.56.1:12345",
"http://101.23.217.1:8090",
"http://101.74.233.1:9001",
"http://101.75.215.1:8008",
"http://106.42.108.1:888",
"http://106.42.34.1:888",
"http://106.42.35.1:888",
"http://106.46.33.1:808",
"http://106.46.37.1:808",
"http://106.46.38.1:808",
"http://110.181.109.1:8081",
"http://110.183.50.1:808",
"http://110.183.56.1:808",
"http://110.19.98.1:808",
"http://110.241.188.1:808",
"http://110.241.189.1:808",
"http://110.241.190.1:808",
"http://110.241.191.1:808",
"http://110.243.76.1:8899",
"http://110.243.78.1:8899",
"http://110.243.80.1:8899",
"http://110.250.214.1:8899",
"http://110.250.215.1:8899",
"http://110.251.158.1:8008",
"http://110.253.83.1:888",
"http://110.52.8.1:808",
"http://110.53.122.1:808",
"http://110.72.17.1:808",
"http://110.72.20.1:808",
"http://110.72.25.1:808",
"http://110.72.28.1:808",
"http://110.72.35.1:808",
"http://110.72.37.1:999",
"http://110.72.39.1:808",
"http://110.72.5.1:999",
"http://111.112.254.1:808",
"http://111.126.255.1:9999",
"http://111.126.255.1:808",
"http://111.22.215.1:808",
"http://111.61.236.1:9081",
"http://111.72.204.1:808",
"http://111.72.246.1:808",
"http://111.72.250.1:808",
"http://111.73.151.1:808",
"http://111.73.152.1:808",
"http://111.73.159.1:808",
"http://111.73.180.1:808",
"http://112.112.249.1:808",
"http://112.114.137.1:888",
"http://112.115.131.1:8005",
"http://112.115.132.1:8005",
"http://112.123.206.1:808",
"http://112.243.226.1:808",
"http://112.244.224.1:808",
"http://112.244.71.1:808",
"http://112.244.84.1:808",
"http://112.244.86.1:808",
"http://112.46.85.1:8001",
"http://112.46.85.1:8002",
"http://112.46.85.1:8008",
"http://112.54.220.1:9088",
"http://112.54.220.1:9099",
"http://113.101.119.1:808",
"http://113.101.119.1:8090",
"http://113.102.160.1:8089",
"http://113.102.162.1:8089",
"http://113.109.117.1:8081",
"http://113.109.119.1:8081",
"http://113.110.72.1:8090",
"http://113.110.72.1:808",
"http://113.116.181.1:8089",
"http://113.116.183.1:8089",
"http://113.118.13.1:808",
"http://113.119.160.1:8073",
"http://113.140.86.1:8009",
"http://113.195.172.1:808",
"http://113.200.75.1:1688",
"http://113.227.108.1:777",
"http://113.231.97.1:8818",
"http://113.231.98.1:8818",
"http://113.234.55.1:777",
"http://113.235.144.1:777",
"http://113.235.196.1:777",
"http://113.239.88.1:8818",
"http://113.239.91.1:8818",
"http://113.240.156.1:8082",
"http://113.240.177.1:8082",
"http://113.45.171.1:465",
"http://113.78.30.1:808",
"http://113.81.20.1:18081",
"http://113.81.21.1:18081",
"http://113.86.205.1:8090",
"http://113.86.205.1:808",
"http://114.223.32.1:12999",
"http://114.223.33.1:12999",
"http://114.225.153.1:12999",
"http://115.148.193.1:808",
"http://115.148.193.1:8088",
"http://115.152.245.1:808",
"http://115.56.156.1:808",
"http://116.112.42.1:808",
"http://116.128.226.1:808",
"http://116.131.150.1:8011",
"http://116.131.173.1:809",
"http://116.136.0.1:888",
"http://116.136.4.1:888",
"http://116.138.153.1:8888",
"http://116.138.153.1:88",
"http://116.138.154.1:88",
"http://116.138.154.1:8888",
"http://116.21.254.1:9901",
"http://116.52.172.1:808",
"http://117.43.20.1:808",
"http://117.43.216.1:20000",
"http://117.43.22.1:808",
"http://117.44.0.1:20000",
"http://117.44.1.1:20000",
"http://117.70.230.1:808",
"http://117.70.233.1:888",
"http://117.70.233.1:808",
"http://117.70.234.1:808",
"http://117.70.234.1:888",
"http://117.70.235.1:808",
"http://117.72.36.1:9099",
"http://117.80.41.1:8888",
"http://118.249.4.1:8082",
"http://118.81.213.1:8088",
"http://118.81.214.1:8088",
"http://118.81.220.1:8088",
"http://118.81.221.1:8088",
"http://118.81.222.1:8088",
"http://118.81.223.1:8088",
"http://119.123.79.1:9600",
"http://119.123.79.1:808",
"http://119.165.87.1:9901",
"http://119.179.7.1:808",
"http://119.251.162.1:8880",
"http://119.36.176.1:18080",
"http://119.54.188.1:5000",
"http://120.14.172.1:8885",
"http://120.192.226.1:8009",
"http://120.211.138.1:808",
"http://120.228.210.1:808",
"http://120.234.40.1:8088",
"http://120.34.136.1:8090",
"http://120.4.49.1:8899",
"http://120.4.50.1:8899",
"http://120.7.84.1:8008",
"http://120.79.17.1:808",
"http://120.79.26.1:808",
"http://121.18.158.1:808",
"http://121.19.134.1:808",
"http://121.21.213.1:8899",
"http://121.21.222.1:8899",
"http://121.224.161.1:8888",
"http://121.224.163.1:8888",
"http://121.236.157.1:8888",
"http://121.238.31.1:12999",
"http://121.24.98.1:8090",
"http://121.24.99.1:8090",
"http://121.29.191.1:8000",
"http://121.29.191.1:8800",
"http://121.56.37.1:808",
"http://121.56.39.1:808",
"http://122.142.169.1:5000",
"http://122.142.171.1:5000",
"http://122.142.172.1:5000",
"http://122.142.178.1:5000",
"http://122.142.181.1:5000",
"http://122.142.185.1:5000",
"http://122.142.92.1:5000",
"http://122.142.95.1:5000",
"http://122.4.199.1:9001",
"http://122.4.199.1:9101",
"http://122.4.199.1:9201",
"http://123.10.77.1:808",
"http://123.10.78.1:808",
"http://123.10.79.1:808",
"http://123.101.157.1:808",
"http://123.101.159.1:808",
"http://123.101.96.1:3333",
"http://123.11.144.1:22222",
"http://123.12.185.1:808",
"http://123.12.186.1:808",
"http://123.13.152.1:808",
"http://123.13.155.1:808",
"http://123.13.159.1:808",
"http://123.13.244.1:7000",
"http://123.13.245.1:7000",
"http://123.13.247.1:7000",
"http://123.130.175.1:808",
"http://123.130.65.1:808",
"http://123.130.70.1:808",
"http://123.161.117.1:9999",
"http://123.162.61.1:888",
"http://123.182.247.1:8092",
"http://123.182.60.1:9002",
"http://123.184.70.1:801",
"http://123.187.46.1:65000",
"http://123.187.59.1:65000",
"http://123.53.236.1:808",
"http://123.53.36.1:9999",
"http://123.53.37.1:9999",
"http://123.53.38.1:9999",
"http://123.53.39.1:9999",
"http://123.54.198.1:808",
"http://123.7.236.1:8081",
"http://123.7.97.1:8099",
"http://124.135.87.1:9901",
"http://124.238.110.1:8880",
"http://124.238.95.1:808",
"http://125.41.230.1:8888",
"http://125.42.173.1:808",
"http://125.42.228.1:9999",
"http://125.42.229.1:9999",
"http://125.42.249.1:9999",
"http://125.44.241.1:8008",
"http://125.44.245.1:90",
"http://125.44.247.1:8008",
"http://125.47.117.1:888",
"http://125.47.84.1:8888",
"http://14.19.142.1:8089",
"http://14.29.76.1:8800",
"http://140.224.183.1:8090",
"http://144.7.38.1:808",
"http://159.75.75.1:8888",
"http://171.116.70.1:8888",
"http://171.13.115.1:808",
"http://171.14.86.1:3333",
"http://171.14.94.1:808",
"http://171.15.151.1:9999",
"http://171.15.5.1:808",
"http://171.217.53.1:808",
"http://171.221.14.1:808",
"http://171.34.76.1:808",
"http://171.41.123.1:88",
"http://171.9.68.1:8099",
"http://171.9.69.1:8099",
"http://171.9.70.1:8099",
"http://171.9.71.1:8099",
"http://175.10.196.1:8082",
"http://175.13.225.1:808",
"http://175.147.19.1:88",
"http://175.147.19.1:8888",
"http://175.166.217.1:777",
"http://175.166.218.1:777",
"http://175.170.18.1:777",
"http://175.171.103.1:777",
"http://175.171.13.1:5111",
"http://175.171.13.1:777",
"http://175.171.17.1:777",
"http://175.171.2.1:777",
"http://175.171.24.1:5111",
"http://175.171.30.1:5111",
"http://175.171.8.1:777",
"http://180.114.60.1:12999",
"http://180.114.62.1:12999",
"http://180.117.28.1:8888",
"http://180.117.31.1:8888",
"http://180.213.169.1:9901",
"http://182.105.168.1:8088",
"http://182.109.59.1:8088",
"http://182.109.59.1:808",
"http://182.113.198.1:888",
"http://182.116.116.1:808",
"http://182.116.123.1:808",
"http://182.117.68.1:808",
"http://182.119.164.1:8081",
"http://182.122.72.1:8089",
"http://182.122.73.1:8089",
"http://182.123.72.1:8090",
"http://182.123.73.1:8090",
"http://182.123.76.1:8090",
"http://182.123.77.1:8090",
"http://182.123.78.1:8090",
"http://182.123.79.1:8090",
"http://182.150.23.1:808",
"http://182.45.186.1:808",
"http://182.45.241.1:808",
"http://182.46.8.1:8018",
"http://182.87.8.1:808",
"http://182.88.216.1:808",
"http://182.99.101.1:808",
"http://182.99.101.1:8088",
"http://183.0.214.1:2233",
"http://183.166.62.1:81",
"http://183.234.70.1:8088",
"http://183.242.1.1:10080",
"http://211.149.143.1:88",
"http://211.97.63.1:801",
"http://218.79.8.1:2001",
"http://218.87.145.1:20000",
"http://219.140.50.1:808",
"http://219.140.51.1:808",
"http://219.144.235.1:8090",
"http://219.155.13.1:8888",
"http://219.155.202.1:808",
"http://219.155.227.1:8008",
"http://219.156.193.1:808",
"http://219.156.197.1:808",
"http://219.157.193.1:888",
"http://220.165.241.1:808",
"http://220.176.50.1:20000",
"http://220.176.60.1:20000",
"http://220.202.92.1:888",
"http://220.202.93.1:888",
"http://220.202.95.1:888",
"http://221.0.78.1:1681",
"http://221.0.78.1:2082",
"http://221.0.78.1:2581",
"http://221.0.78.1:1181",
"http://221.0.78.1:881",
"http://221.201.131.1:771",
"http://221.201.131.1:777",
"http://221.205.239.1:8088",
"http://221.211.232.1:9000",
"http://221.211.233.1:9000",
"http://221.214.139.1:808",
"http://221.237.25.1:808",
"http://222.136.210.1:808",
"http://222.137.25.1:8081",
"http://222.137.85.1:8081",
"http://222.138.101.1:808",
"http://222.138.78.1:808",
"http://222.140.160.1:808",
"http://222.172.183.1:808",
"http://222.211.198.1:808",
"http://222.211.199.1:808",
"http://222.219.183.1:8089",
"http://222.223.158.1:50009",
"http://222.78.16.1:8090",
"http://222.88.210.1:808",
"http://223.166.92.1:12999",
"http://27.128.203.1:808",
"http://27.185.1.1:8092",
"http://27.192.122.1:808",
"http://27.223.246.1:9901",
"http://27.41.248.1:801",
"http://27.41.248.1:808",
"http://27.41.249.1:801",
"http://27.41.250.1:808",
"http://27.41.250.1:801",
"http://27.41.251.1:801",
"http://27.41.251.1:808",
"http://36.129.204.1:8083",
"http://36.129.204.1:50001",
"http://36.141.28.1:5004",
"http://36.141.28.1:8083",
"http://36.141.28.1:8085",
"http://36.99.128.1:808",
"http://36.99.134.1:808",
"http://39.150.50.1:808",
"http://42.176.182.1:8818",
"http://42.202.19.1:8818",
"http://42.224.8.1:808",
"http://42.224.91.1:808",
"http://42.224.93.1:808",
"http://42.225.144.1:8089",
"http://42.225.145.1:8089",
"http://42.225.147.1:8089",
"http://42.227.174.1:9999",
"http://42.229.219.1:8099",
"http://42.235.53.1:888",
"http://42.238.169.1:888",
"http://42.238.170.1:888",
"http://42.48.2.1:808",
"http://42.48.25.1:808",
"http://42.49.216.1:808",
"http://42.80.41.1:888",
"http://47.100.188.1:808",
"http://47.104.102.1:808",
"http://47.108.221.1:9089",
"http://47.108.221.1:9099",
"http://47.109.181.1:88",
"http://47.99.164.1:808",
"http://49.76.42.1:12999",
"http://58.16.141.1:8088",
"http://58.17.48.1:808",
"http://58.20.44.1:808",
"http://58.20.87.1:808",
"http://59.173.108.1:808",
"http://59.173.109.1:808",
"http://59.173.110.1:808",
"http://59.173.111.1:808",
"http://59.38.45.1:8090",
"http://59.38.46.1:8090",
"http://59.38.47.1:8090",
"http://59.39.200.1:808",
"http://59.42.60.1:808",
"http://59.44.192.1:65000",
"http://59.47.118.1:801",
"http://59.52.184.1:8888",
"http://59.52.185.1:8888",
"http://59.52.186.1:8888",
"http://59.52.187.1:8888",
"http://59.62.94.1:808",
"http://59.62.94.1:8088",
"http://59.62.95.1:808",
"http://60.10.139.1:8801",
"http://60.10.139.1:8800",
"http://60.16.18.1:4949",
"http://60.17.187.1:88",
"http://60.175.86.1:81",
"http://60.220.147.1:808",
"http://60.223.255.1:8800",
"http://60.29.124.1:6080",
"http://60.4.229.1:808",
"http://60.6.111.1:808",
"http://60.9.236.1:50003",
"http://61.140.233.1:9990",
"http://61.140.235.1:9990",
"http://61.146.224.1:8088",
"http://61.53.141.1:808",
"http://61.53.82.1:808",
"http://61.53.95.1:808",
"http://61.54.253.1:808",
"http://8.130.21.1:880",
"http://122.138.218.1:50085",
"http://60.22.88.1:8002",
"http://58.243.9.1:808",
"http://219.157.13.1:808",
"http://114.104.171.1:20080",
"http://120.238.53.1:2223",
"http://42.49.34.1:808",
"http://120.194.237.1:808",
"http://218.59.233.1:3456",
"http://118.122.2.1:9999",
"http://221.229.246.1:808",
"http://58.17.77.1:808",
"http://58.20.243.1:808",
"http://49.221.17.1:808",
"http://58.20.202.1:808",
"http://220.167.113.1:8033"
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
        response = requests.get(url, timeout=0.2)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


results = []

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
            print(result)

#for url in valid_urls:
#    print(url)

#now_today = datetime.date.today()
#with open("ip.txt", 'a', encoding='utf-8') as file:
#    file.write(f"{now_today}更新\n")
#    for url in valid_urls:
#        file.write(url + "\n")

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


channels = []

for result in results:
    line = result.strip()
    if result:
        channel_name, channel_url = result.split(',')
        channels.append((channel_name, channel_url))

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

error_channels = []


# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
            lines = requests.get(channel_url, timeout = 1).text.strip().split('\n')  # 获取m3u8文件内容
            ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
            ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接

            # 多获取的视频数据进行5秒钟限制
            with eventlet.Timeout(5, False):
                start_time = time.time()
                content = requests.get(ts_url, timeout = 1).content
                end_time = time.time()
                response_time = (end_time - start_time) * 1

            if content:
                with open(ts_lists_0, 'ab') as f:
                    f.write(content)  # 写入文件
                file_size = len(content)
                # print(f"文件大小：{file_size} 字节")
                download_speed = file_size / response_time / 1024
                # print(f"下载速度：{download_speed:.3f} kB/s")
                normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                #print(f"标准化后的速率：{normalized_speed:.3f} MB/s")

                # 删除下载的文件
                os.remove(ts_lists_0)
                result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                results.append(result)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            numberx = (len(results) + len(error_channels)) / len(channels) * 100
            print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 10
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)  # 将工作线程设置为守护线程
    t.start()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
results.sort(key=lambda x: channel_key(x[0]))


result_counter = 8  # 每个频道需要的个数

with open("itvlist.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('卫视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

with open("itvlist.m3u", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('#EXTM3U\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"央视频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"央视频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    #file.write('卫视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"卫视频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"卫视频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    #file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"其他频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"其他频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1