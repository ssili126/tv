import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
eventlet.monkey_patch()

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []

with open("itv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line:
            channel_name, channel_url = line.split(',')
            channels.append((channel_name, channel_url))

# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            response = requests.get(channel_url, timeout=1)
            if response.status_code == 200:
                channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
                lines = requests.get(channel_url,timeout=1).text.strip().split('\n')  # 获取m3u8文件内容
                ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀

                file_size = 0
                start_time = time.time()
                # 多获取的视频数据进行12秒钟限制
                with eventlet.Timeout(12, False):
                    for i in range(len(ts_lists)):
                        ts_url = channel_url_t + ts_lists[i]  # 拼接单个视频片段下载链接
                        response = requests.get(ts_url, stream=True, timeout=1)
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file_size += len(chunk)
                        response.close()
                end_time = time.time()
                response_time = end_time - start_time
                if response_time >=12:
                    file_size = 0
                download_speed = file_size / response_time / 1024
                normalized_speed =download_speed / 1024  # 将速率从kB/s转换为MB/s
                ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接
                if normalized_speed >= 1:
                    if file_size >= 12000000:
                        result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                        results.append(result)
                        numberx = (len(results) + len(error_channels)) / len(channels) * 100
                        print(f"可用频道：{len(results)} , 网速：{normalized_speed:.3f} MB/s , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
                    else:
                        error_channel = channel_name, channel_url
                        error_channels.append(error_channel)
                        numberx = (len(results) + len(error_channels)) / len(channels) * 100
                        print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} , 网速：{normalized_speed:.3f} MB/s , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
                else:
                    error_channel = channel_name, channel_url
                    error_channels.append(error_channel)
                    numberx = (len(results) + len(error_channels)) / len(channels) * 100
                    print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} , 网速：{normalized_speed:.3f} MB/s , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
            else:
                error_channel = channel_name, channel_url
                error_channels.append(error_channel)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(
                    f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
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
    t = threading.Thread(target=worker, daemon=True) 
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
now_today = datetime.date.today()
# 将结果写入文件
with open("itv_results.txt", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url, speed = result
        file.write(f"{channel_name},{channel_url},{speed}\n")

with open("itv_speed.txt", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url, speed = result
        file.write(f"{channel_name},{channel_url}\n")


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
                
    file.write(f"{now_today}更新,#genre#\n")

