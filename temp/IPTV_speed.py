import re
import requests
import concurrent.futures

def test_speed(channel_name, channel_url):
    try:
        response = requests.get(channel_url, timeout=2)
        if response.status_code == 200:
            speed = response.elapsed.total_seconds()
            return channel_name, channel_url, f"{speed:.3f} seconds"
        else:
            return channel_name, channel_url, "Failed"
    except:
        return channel_name, channel_url, "Failed"

def channel_key(channel):
    match = re.search(r'\d+', channel)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

channels = []

with open("IPTV.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line:
            if 'rtp' in line or 'udp' in line:
                pass
            else:
                channel_name, channel_url = line.split(',')
                channels.append((channel_name, channel_url))

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []

    for channel in channels:
        channel_name, channel_url = channel
        futures.append(executor.submit(test_speed, channel_name, channel_url))

    results = []
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        results.append(result)

results.sort(key=lambda x: (x[0], x[2]))

with open("speed_results.txt", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url, speed = result
        file.write(f"{channel_name},{channel_url},{speed}\n")


channels = []
with open("speed_results.txt", 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            channel_name, channel_url, speed = line.split(',')
            if speed != "Failed":
                channels.append((channel_name,channel_url))


# 对频道进行排序
channels.sort(key=lambda x: channel_key(x[0]))

with open("IPTV_speed.txt", 'w', encoding='utf-8') as file:
    for channel_name,channel_url in channels:
        file.write(f'{channel_name},{channel_url}\n')
