import re
# 读取iptv.txt文件，提取频道信息
channels = []
with open('IPTV.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            channel, address = line.split(',')
            channels.append((channel, address))
# 对频道进行排序
channels.sort()
# 自定义排序函数，提取频道名称中的数字并按数字排序
def channel_key(channel):
    match = re.search(r'\d+', channel)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

# 对频道进行排序
channels.sort(key=lambda x: channel_key(x[0]))

# 生成iptv_list.txt文件
with open('iptv_sort.txt', 'w', encoding='utf-8') as file:
    file.write('央视频道,#genre#\n')
    for channel, address in channels:
        if 'cctv' in channel.lower():
            file.write(f'{channel},{address}\n')
    file.write('卫视频道,#genre#\n')
    for channel, address in channels:
        if '卫视' in channel:
            file.write(f'{channel},{address}\n')
    file.write('其他频道,#genre#\n')
    for channel, address in channels:
        if 'cctv' not in channel.lower() and '卫视' not in channel:
            file.write(f'{channel},{address}\n')
