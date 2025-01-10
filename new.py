import asyncio
import logging
import time
from urllib.parse import urlparse
import aiofiles
import aiohttp
import re
import os
from typing import List, Tuple

# 网段最小范围
min_network_segment = 1
# 网段最大范围
max_network_segment = 256
# 每个频道需要的个数
result_counter = 8
# 控制异步并发的信号量
semaphore = asyncio.Semaphore(200)
# 请求等待时间, 并发量越高时间要越长
time_out = 3
# 源URL
src_urls = [
    "http://1.196.55.1:9901",
    "http://1.197.249.1:9901",
    "http://101.65.32.1:9901",
    "http://101.66.198.1:9901",
    "http://101.66.199.1:9901",
    "http://101.72.127.1:808",
    "http://106.46.147.1:10443",
    "http://106.55.164.1:9901",
    "http://111.225.112.1:808",
    "http://111.225.114.1:808",
    "http://111.33.89.1:9901",
    "http://111.78.22.1:9901",
    "http://111.8.224.1:8085",
    "http://112.132.160.1:9901",
    "http://112.234.23.1:9901",
    "http://112.26.18.1:9901",
    "http://112.5.89.1:9900",
    "http://112.5.89.1:9901",
    "http://113.116.145.1:8883",
    "http://113.116.59.1:8883",
    "http://113.124.234.1:9901",
    "http://113.195.13.1:9901",
    "http://113.195.162.1:9901",
    "http://113.195.4.1:9901",
    "http://113.195.45.1:9901",
    "http://113.200.214.1:9902",
    "http://113.201.61.1:9901",
    "http://113.205.195.1:9901",
    "http://113.205.196.1:9901",
    "http://113.206.102.1:9901",
    "http://113.218.204.1:8081",
    "http://113.220.234.1:9999",
    "http://113.220.235.1:9999",
    "http://113.57.20.1:9901",
    "http://113.57.93.1:9900",
    "http://113.92.198.1:8883",
    "http://114.254.92.1:88",
    "http://115.149.139.1:10001",
    "http://115.236.83.1:1111",
    "http://115.48.22.1:9901",
    "http://115.48.63.1:9901",
    "http://116.128.224.1:9901",
    "http://116.128.242.1:9901",
    "http://116.167.111.1:9901",
    "http://116.167.76.1:9901",
    "http://116.167.79.1:9901",
    "http://116.227.232.1:7777",
    "http://116.233.34.1:7777",
    "http://116.30.121.1:8883",
    "http://116.31.165.1:280",
    "http://116.31.165.1:3079",
    "http://116.31.165.1:6666",
    "http://117.27.190.1:9998",
    "http://117.90.196.1:6000",
    "http://118.248.168.1:8088",
    "http://118.248.169.1:8088",
    "http://118.248.216.1:8088",
    "http://118.81.106.1:9999",
    "http://118.81.107.1:9999",
    "http://119.125.134.1:7788",
    "http://119.163.228.1:9901",
    "http://120.0.52.1:8086",
    "http://120.0.8.1:8086",
    "http://121.19.134.1:808",
    "http://121.232.178.1:5000",
    "http://121.232.187.1:6000",
    "http://121.33.239.1:9901",
    "http://122.188.62.1:8800",
    "http://123.129.70.1:9901",
    "http://123.130.84.1:8154",
    "http://123.138.216.1:9902",
    "http://123.138.22.1:9901",
    "http://123.139.57.1:9901",
    "http://123.154.154.1:9901",
    "http://123.182.247.1:4433",
    "http://124.126.4.1:9901",
    "http://124.128.73.1:9901",
    "http://124.231.213.1:9999",
    "http://125.106.86.1:9901",
    "http://125.107.177.1:9901",
    "http://125.125.234.1:9901",
    "http://14.106.236.1:9901",
    "http://14.106.239.1:9901",
    "http://171.8.75.1:8011",
    "http://180.113.102.1:5000",
    "http://180.117.149.1:9901",
    "http://180.124.146.1:60000",
    "http://180.175.163.1:7777",
    "http://180.213.174.1:9901",
    "http://182.113.206.1:9901",
    "http://182.117.136.1:9901",
    "http://202.100.46.1:9901",
    "http://210.22.75.1:9901",
    "http://218.74.169.1:9901",
    "http://218.76.32.1:9901",
    "http://218.87.237.1:9901",
    "http://220.161.206.1:9901",
    "http://220.179.68.1:9901",
    "http://220.180.112.1:9901",
    "http://220.249.114.1:9901",
    "http://221.2.148.1:8154",
    "http://221.205.128.1:9999",
    "http://221.205.129.1:9999",
    "http://221.205.130.1:9999",
    "http://221.205.131.1:9999",
    "http://221.233.192.1:1111",
    "http://222.134.245.1:9901",
    "http://222.243.221.1:9901",
    "http://223.166.234.1:7777",
    "http://223.241.247.1:9901",
    "http://223.68.201.1:9901",
    "http://27.14.163.1:9901",
    "http://27.14.84.1:9901",
    "http://27.8.192.1:9901",
    "http://27.8.233.1:9901",
    "http://27.8.243.1:9901",
    "http://36.249.150.1:9901",
    "http://36.249.151.1:9901",
    "http://36.40.236.1:9999",
    "http://36.44.157.1:9901",
    "http://36.99.206.1:9901",
    "http://47.104.163.1:9901",
    "http://47.116.70.1:9901",
    "http://49.232.48.1:9901",
    "http://49.234.31.1:7004",
    "http://58.17.116.1:9908",
    "http://58.19.244.1:1111",
    "http://58.209.101.1:9901",
    "http://58.216.229.1:9901",
    "http://58.220.219.1:9901",
    "http://58.23.27.1:9901",
    "http://58.243.224.1:9901",
    "http://58.243.93.1:9901",
    "http://58.48.37.1:1111",
    "http://58.48.5.1:1111",
    "http://59.173.183.1:9901",
    "http://59.63.22.1:8888",
    "http://60.169.254.1:9901",
    "http://60.172.59.1:9901",
    "http://60.174.86.1:9901",
    "http://61.136.172.1:9901",
    "http://61.136.67.1:50085",
    "http://61.156.228.1:8154",
    "http://61.173.144.1:9901"
]

src_urls_test = src_urls[31:36]


# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def modify_urls(src_url):
    # 正则替换IP第四位
    modified_urls = []
    pattern = r'\.(\d+)\:'
    request_param = "/iptv/live/1000.json?key=txiptv"
    for i in range(min_network_segment, max_network_segment):
        base_url = re.sub(pattern, f".{i}:", src_url)
        modified_url = f"{base_url}{request_param}"
        modified_urls.append(modified_url)
    return set(modified_urls)


async def check_url_code(url):
    # 校验url是否可用
    async with semaphore:  # 限制并发数
        try:
            async with aiohttp.ClientSession() as session:
                logging.info(f"开始校验: {url}")
                async with session.get(url, timeout=time_out) as resp:
                    if resp.status == 200:
                        return url
                    else:
                        return None
        except Exception:
            return None


async def get_valid_urls() -> list:
    # 获取所有有效的url

    tasks = []  # 用来存储所有异步任务

    for src_url in src_urls:
        urls = modify_urls(src_url)
        for url in urls:
            # 启动每个校验任务
            tasks.append(check_url_code(url))

    # 等待所有校验任务完成，并获取结果
    results = await asyncio.gather(*tasks)

    # 筛选出有效的url
    valid_urls = [url for url in results if url is not None]

    logging.info(f"共找到 {len(valid_urls)} 个有效的URL")
    return valid_urls


def replace_name(name: str) -> str:
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
    return name


# 获取所有可用的电视名字和链接
async def get_iptv_name_m3u8s() -> List[Tuple[str, str, str]]:
    """
    遍历url，获取JSON并解析

    返回一个列表元组:
        1是tv名字,
        2是m3u8的url
    """
    m3u8_list = []
    urls = await get_valid_urls()

    for url in urls:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=2) as resp:
                    json_data = await resp.json()
            try:
                # 解析JSON文件，获取name和url字段
                for item in json_data['data']:
                    if isinstance(item, dict):
                        name = item.get('name')
                        url_param = item.get('url')
                        if ',' in url_param:
                            url_param = f"aaaaaaaa"
                        # if 'http' in urlx or 'udp' in urlx or 'rtp' in urlx:
                        if 'http' in url_param:
                            parsed_url = urlparse(url)
                            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                            m3u9_url = f"{url_param}"
                        else:
                            parsed_url = urlparse(url)
                            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                            m3u9_url = f"{base_url}{url_param}"
                        if name and url_param:
                            # 修改特定文字
                            m3u8_list.append((replace_name(name), m3u9_url, base_url))
            except:
                continue
        except:
            continue
    return m3u8_list


async def download_ts(m3u8_list: List[Tuple[str, str, str]]) -> Tuple[
    List[Tuple[str, str, str]], List[Tuple[str, str]]]:
    """
    下载ts测试url是否可用

    返回两个列表:
        第一个是结果
        第二个是错误
    """
    results = []
    error_channels = []

    async with aiohttp.ClientSession() as session:
        async def download_channel(name: str, url: str, base_url: str):
            try:
                async with session.get(url, timeout=2) as resp:
                    lines = (await resp.text()).strip().split('\n')
                    ts_lists = [line.split('/')[-1] for line in lines if not line.startswith('#')]  # 获取m3u8文件下视频流后缀
                    if not ts_lists:
                        raise ValueError(f"No video segments found for {name}")

                    ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
                    ts_url = f"{base_url}/{ts_lists[0]}"  # 拼接单个视频片段下载链接

                    # 获取TS文件内容并测量下载时间
                    start_time = time.time()
                    async with session.get(ts_url, timeout=1) as ts_response:
                        content = await ts_response.read()
                    end_time = time.time()
                    response_time = (end_time - start_time)

                    if content:
                        # 使用aiofiles异步写入文件
                        async with aiofiles.open(ts_lists_0, 'ab') as f:
                            await f.write(content)

                        file_size = len(content)
                        download_speed = file_size / response_time / 1024  # kB/s
                        normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 转换为MB/s并限制在1~100之间

                        os.remove(ts_lists_0)  # 删除下载的文件

                        result = (name, url, f"{normalized_speed:.3f} MB/s")
                        results.append(result)
                        numberx = (len(results) + len(error_channels)) / len(m3u8_list) * 100
                        logging.info(
                            f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(m3u8_list)} 个 , 总进度：{numberx:.2f} %。")
            except Exception as e:
                error_channel = (name, url)
                error_channels.append(error_channel)
                numberx = (len(results) + len(error_channels)) / len(m3u8_list) * 100
                logging.info(
                    f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(m3u8_list)} 个 , 总进度：{numberx:.2f} %。")

        # 使用 asyncio.gather 执行所有下载任务
        if m3u8_list != None:
            tasks = [download_channel(name, url, base_url) for name, url, base_url in m3u8_list]
            await asyncio.gather(*tasks)
        else:
            pass

    return results, error_channels


def results_sort(results) -> list:
    # 频道进行排序
    def channel_key(channel_name):
        match = re.search(r'\d+', channel_name)
        if match:
            return int(match.group())
        else:
            return float('inf')  # 返回一个无穷大的数字作为关键字

    results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
    results.sort(key=lambda x: channel_key(x[0]))
    return results


def write_itv_txt(results):
    # 写出txt类型
    results_sort(results)
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


def write_itv_m3u(results):
    # 写出m3u类型
    results_sort(results)
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
        # file.write('卫视频道,#genre#\n')
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
        # file.write('其他频道,#genre#\n')
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


async def start():
    start_time = time.time()
    m3u8_list = await get_iptv_name_m3u8s()
    results, error_channels = await download_ts(m3u8_list)
    write_itv_txt(results)
    write_itv_m3u(results)
    logging.info(f"成功频道: {len(results)}个.", )
    logging.info(f"错误频道: {len(error_channels)}个.")
    end_time = time.time()
    logging.info(f"耗时: {end_time - start_time}s.")


if __name__ == '__main__':
    asyncio.run(start())