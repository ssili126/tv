import asyncio
import re
from typing import List, Tuple
import aiohttp


urls = [
"http://112.123.217.1:9901",
"http://112.123.218.1:9901",
"http://112.123.219.1:9901",
"http://112.132.160.1:9901",
"http://112.193.114.1:9901",
"http://112.193.42.1:9901",
"http://112.194.128.1:9901",
"http://112.194.140.1:9901",
"http://112.194.206.1:9901",
"http://112.234.21.1:9901",
"http://112.234.23.1:9901",
"http://112.235.200.1:9901",
"http://112.235.201.1:9901",
"http://112.235.202.1:9901",
"http://112.26.18.1:9901",
"http://112.27.145.1:9901",
"http://112.5.146.1:9900",
"http://112.5.89.1:9900",
"http://112.5.89.1:9901",
"http://112.6.117.1:9901",
"http://112.6.126.1:9901",
"http://112.6.165.1:9901",
"http://112.6.178.1:9901",
"http://112.91.103.1:9919",
"http://112.99.193.1:9901",
"http://112.99.195.1:9901",
"http://112.99.200.1:9901",
"http://113.100.72.1:9901",
"http://113.111.104.1:9901",
"http://113.116.145.1:8883",
"http://113.116.56.1:8883",
"http://113.116.58.1:8883",
"http://113.116.59.1:8883",
"http://113.124.234.1:9901",
"http://113.124.72.1:9901",
"http://113.15.186.1:8181",
"http://113.195.13.1:9901",
"http://113.195.162.1:9901",
"http://113.195.4.1:9901",
"http://113.195.45.1:9901",
"http://113.195.7.1:9901",
"http://113.195.8.1:9901",
"http://113.200.214.1:9902",
"http://113.201.61.1:9901",
"http://113.205.195.1:9901",
"http://113.205.196.1:9901",
"http://113.206.102.1:9901",
"http://113.218.188.1:9901",
"http://113.218.189.1:8081",
"http://113.218.190.1:8081",
"http://113.218.204.1:8081",
"http://113.220.232.1:9999",
"http://113.220.233.1:9999",
"http://113.220.234.1:9999",
"http://113.220.235.1:9999",
"http://113.223.12.1:9998",
"http://113.236.30.1:9901",
"http://113.245.217.1:9901",
"http://113.245.218.1:9901",
"http://113.245.219.1:9901",
"http://113.57.20.1:9901",
"http://113.57.93.1:9900",
"http://113.64.94.1:9901",
"http://113.70.161.1:9901",
"http://113.81.21.1:9901",
"http://113.92.198.1:8883",
"http://114.254.92.1:88",
"http://115.149.139.1:10001",
"http://115.207.18.1:9901",
"http://115.207.211.1:9901",
"http://115.207.24.1:9901",
"http://115.215.143.1:9901",
"http://115.220.17.1:9901",
]


def modify_urls(url: str) -> list[str]:
    """遍历网段内所有IP，拼出 JSON 地址列表"""
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    for i in range(1, 256):
        modified_ip = f"{ip_address.rsplit('.',1)[0]}.{i}"
        modified_url = f"{base_url}{modified_ip}{port}{IPTV_PATH}"
        modified_urls.append(modified_url)
    return modified_urls


async def is_url_accessible(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore) -> str | None:
    """用 HEAD 请求快速探测 200 状态"""
    async with sem:
        try:
            async with session.head(url) as resp:
                if resp.status == 200:
                    print(url)
                    return url
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return None


async def check_urls(base_urls: list[str]) -> list[str]:
    """并发扫描所有 modify_urls 生成的候选地址，返回可用列表"""
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        # 扁平化所有任务
        tasks = [
            is_url_accessible(session, candidate, sem)
            for raw in set(base_urls)
            for candidate in modify_urls(raw.strip())
        ]
        valid = []
        # as_completed 实时收集
        for coro in asyncio.as_completed(tasks):
            url = await coro
            if url:
                valid.append(url)
        return valid

async def fetch_json(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore) -> List[Tuple[str, str]]:
    """
    拉取 IPTV JSON，解析出每个频道的 (name, m3u8_url)。
    """
    async with sem:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                payload = await resp.json()
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            print(f"[fetch_json] 从 {url} 获取 JSON 失败: {e}")
            return []

    data = payload.get("data", [])
    results: List[Tuple[str, str]] = []
    for item in data:
        name = item.get("name")
        rel = item.get("url")
        if not name or not rel:
            continue
        # 自动拼接相对路径到完整 URL
        full_url = url + rel
        results.append((name, full_url))
    return results


def rename(name: str) -> str | None:
    """替换频道名"""
    if not name:
        return None
    name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
    # 替换频道名对应表
    alias_map = {
        "cctv": "CCTV",
        "中央": "CCTV",
        "央视": "CCTV",
        "＋": "+",
        "plus": "+",
        "cctv1综合": "CCTV1",
        "cctv2财经": "CCTV2",
        "cctv3综艺": "CCTV3",
        "cctv4国际": "CCTV4",
        "cctv4中文国际": "CCTV4",
        "cctv4欧洲": "CCTV4",
        "cctv5体育": "CCTV5",
        "cctv5+体育赛事": "CCTV5+",
        "cctv5+体育赛视": "CCTV5+",
        "cctv5+体育": "CCTV5+",
        "cctv6电影": "CCTV6",
        "cctv7军事": "CCTV7",
        "cctv7军农": "CCTV7",
        "cctv7农业": "CCTV7",
        "cctv7国防军事": "CCTV7",
        "cctv8电视剧": "CCTV8",
        "cctv9记录": "CCTV9",
        "cctv9纪录": "CCTV9",
        "cctv10科教": "CCTV10",
        "cctv11戏曲": "CCTV11",
        "cctv12社会与法": "CCTV12",
        "cctv13新闻": "CCTV13",
        "cctv新闻": "CCTV13",
        "cctv14少儿": "CCTV14",
        "cctv15音乐": "CCTV15",
        "cctv16奥林匹克": "CCTV16",
        "cctv17农业农村": "CCTV17",
        "cctv17农业": "CCTV17",
    }

    # 优先处理别名
    for key, value in alias_map.items():
        if key in name:
            return value
    # 其他保留清理格式后的结果（首字母大写）
    return name.upper()


async def measure_speed(session: aiohttp.ClientSession, name_url: Tuple[str, str], sem: asyncio.Semaphore) -> Tuple[str, str, float] | None:
    """
    对单个频道测速，返回 (频道名称, m3u8地址, 下载速率 MB/s)，测速失败则返回 None。
    """
    name, m3u8_url = name_url
    async with sem:
        try:
            asyncio.get_event_loop().time()
            async with session.get(m3u8_url, timeout=1) as resp:
                if resp.status != 200:
                    return None
                content = await resp.text()
            lines = [line for line in content.splitlines() if line and not line.startswith("#")]
            if not lines:
                return None
            ts_url = lines[0]
            if not ts_url.startswith("http"):
                # 相对路径拼接
                prefix = m3u8_url.rsplit("/", 1)[0]
                ts_url = f"{prefix}/{ts_url}"

            ts_start = asyncio.get_event_loop().time()
            async with session.get(ts_url, timeout=2) as ts_resp:
                ts_data = await ts_resp.read()
            ts_end = asyncio.get_event_loop().time()
            duration = ts_end - ts_start
            if not ts_data or duration == 0:
                return None
            speed_kbps = len(ts_data) / duration / 1024  # kB/s
            return rename(name), m3u8_url, round(speed_kbps / 1024, 3)  # MB/s
        except Exception:
            return None


async def measure_all_speeds(channels: List[Tuple[str, str]], sem: asyncio.Semaphore) -> List[Tuple[str, str, float]]:
    """
    并发测速所有频道，返回测速成功的频道列表，格式为 [(频道名称, 播放地址, 下载速率MB/s), ...]
    """
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        tasks = [measure_speed(session, ch, sem) for ch in channels]
        results = []
        for coro in asyncio.as_completed(tasks):
            result = await coro
            if result:
                results.append(result)
        return results


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')

def write_file(results: List[Tuple[str, str, float]]) -> None:
    with open("itvlist.txt", 'w', encoding='utf-8') as file:
        channel_counters = {}
        file.write('央视频道,#genre#\n')
        for result in results:
            channel_name, channel_url, speed = result
            if 'CCTV' in channel_name:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= IPTV_SAVE_NUM:
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
                    if channel_counters[channel_name] >= IPTV_SAVE_NUM:
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
                    if channel_counters[channel_name] >= IPTV_SAVE_NUM:
                        continue
                    else:
                        file.write(f"{channel_name},{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] = 1


async def main() -> None:
    # 1. 探测 JSON 接口
    result = await check_urls(urls)
    print(result)
    # 2. 拉取频道列表
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        fetch_tasks = [fetch_json(session, u, sem) for u in result]
        lists = await asyncio.gather(*fetch_tasks)
    channels = [item for sub in lists for item in sub]
    # 3. 并发测速
    measured = await measure_all_speeds(channels, sem)
    measured.sort(key=lambda x: channel_key(x[0]))
    for name, url, speed in measured:
        print(f"{name}: {url} -> {speed:.2f} MB/s")
    write_file(measured)


if __name__ == "__main__":
    # 并发量上限
    MAX_CONCURRENCY = 300
    # 请求超时
    TIMEOUT = aiohttp.ClientTimeout(total=0.5)
    # IPTV路径
    IPTV_PATH = "/iptv/live/1000.json?key=txiptv"
    # 每个频道保存个数
    IPTV_SAVE_NUM = 8
    # 开始运行
    asyncio.run(main())
