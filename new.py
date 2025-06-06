import asyncio
import aiohttp
import re
import datetime
import requests
import eventlet
import os
import time
import threading
from queue import Queue
eventlet.monkey_patch()


urls = [
"http://1.192.12.1:9901",
"http://1.192.248.1:9901",
"http://1.194.52.1:10086",
"http://1.195.111.1:11190",
"http://1.195.130.1:9901",
"http://1.195.131.1:9901",
"http://1.195.62.1:9901",
"http://1.196.192.1:9901",
"http://1.196.252.1:9901",
"http://1.196.55.1:9901",
"http://1.197.153.1:9901",
"http://1.197.203.1:9901",
"http://1.197.249.1:9901",
"http://1.197.250.1:9901",
"http://1.197.251.1:9901",
"http://1.197.82.1:9901",
"http://1.197.83.1:9901",
"http://1.197.84.1:9901",
"http://1.198.30.1:9901",
"http://1.198.67.1:9901",
"http://1.199.234.1:9901",
"http://1.199.235.1:9901",
"http://101.65.32.1:9901",
"http://101.65.34.1:9901",
"http://101.66.194.1:9901",
"http://101.66.195.1:9901",
"http://101.66.198.1:9901",
"http://101.66.199.1:9901",
"http://101.71.213.1:9901",
"http://101.72.127.1:808",
"http://101.74.28.1:9901",
"http://103.39.222.1:9999",
"http://106.115.121.1:9901",
"http://106.118.70.1:9901",
"http://106.124.91.1:9901",
"http://106.46.114.1:8011",
"http://106.46.147.1:10443",
"http://106.46.34.1:9901",
"http://106.55.164.1:9901",
"http://110.189.180.1:9901",
"http://110.52.99.1:9901",
"http://110.53.218.1:9902",
"http://110.7.128.1:8096",
"http://110.7.129.1:8096",
"http://110.7.130.1:8096",
"http://110.72.53.1:8181",
"http://110.81.206.1:50080",
"http://111.15.174.1:8969",
"http://111.225.112.1:808",
"http://111.225.114.1:808",
"http://111.225.115.1:9901",
"http://111.33.89.1:9901",
"http://111.59.63.1:9901",
"http://111.74.155.1:9901",
"http://111.78.22.1:9901",
"http://111.78.34.1:9901",
"http://111.8.224.1:8085",
"http://111.8.242.1:8085",
"http://111.8.242.1:9901",
"http://111.8.242.1:9999",
"http://111.9.163.1:9901",
"http://112.101.78.1:9901",
"http://112.116.14.1:9901",
"http://112.116.15.1:9901",
"http://112.123.130.1:9901",
"http://112.123.138.1:9901",
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
"http://115.224.206.1:9901",
"http://115.225.233.1:9901",
"http://115.236.171.1:9901",
"http://115.236.83.1:1111",
"http://115.48.160.1:9901",
"http://115.48.161.1:9901",
"http://115.48.22.1:9901",
"http://115.48.60.1:9901",
"http://115.48.62.1:9901",
"http://115.48.63.1:9901",
"http://115.50.120.1:9901",
"http://115.55.132.1:9901",
"http://115.55.59.1:9901",
"http://115.59.9.1:9901",
"http://116.117.104.1:8096",
"http://116.117.105.1:8096",
"http://116.117.106.1:8096",
"http://116.117.107.1:8096",
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
"http://116.55.141.1:9901",
"http://116.55.176.1:9901",
"http://116.55.180.1:9901",
"http://117.174.99.1:9901",
"http://117.27.190.1:9901",
"http://117.27.190.1:9998",
"http://117.90.196.1:6000",
"http://118.122.189.1:9901",
"http://118.248.167.1:8088",
"http://118.248.168.1:8088",
"http://118.248.169.1:8088",
"http://118.248.170.1:8088",
"http://118.248.216.1:8088",
"http://118.253.0.1:2023",
"http://118.72.48.1:888",
"http://118.72.49.1:888",
"http://118.72.50.1:888",
"http://118.72.51.1:888",
"http://118.72.68.1:888",
"http://118.72.69.1:888",
"http://118.81.106.1:9999",
"http://118.81.107.1:9999",
"http://119.119.77.1:9901",
"http://119.120.196.1:9999",
"http://119.125.104.1:9901",
"http://119.125.128.1:9901",
"http://119.125.129.1:9901",
"http://119.125.130.1:9901",
"http://119.125.131.1:9901",
"http://119.125.134.1:7788",
"http://119.125.134.1:9901",
"http://119.129.173.1:9999",
"http://119.142.76.1:9901",
"http://119.142.77.1:9901",
"http://119.163.199.1:9901",
"http://119.163.228.1:9901",
"http://119.163.56.1:9901",
"http://119.163.57.1:9901",
"http://119.163.60.1:9901",
"http://119.163.61.1:9901",
"http://119.163.63.1:9901",
"http://119.164.81.1:9901",
"http://119.177.21.1:9901",
"http://119.177.23.1:9901",
"http://119.179.182.1:9901",
"http://119.183.200.1:9901",
"http://119.39.192.1:9898",
"http://119.51.52.1:9901",
"http://119.51.62.1:9901",
"http://119.51.63.1:9901",
"http://119.51.64.1:9901",
"http://119.62.28.1:9901",
"http://119.62.36.1:9901",
"http://119.62.80.1:9901",
"http://120.0.52.1:8086",
"http://120.0.8.1:8086",
"http://120.197.43.1:9901",
"http://120.198.96.1:9901",
"http://120.198.99.1:9901",
"http://120.211.129.1:9901",
"http://120.224.178.1:9901",
"http://120.224.23.1:9901",
"http://120.238.150.1:9901",
"http://120.238.85.1:9901",
"http://121.19.134.1:808",
"http://121.232.178.1:5000",
"http://121.232.187.1:6000",
"http://121.238.176.1:9901",
"http://121.24.98.1:9901",
"http://121.33.239.1:9901",
"http://121.43.180.1:9901",
"http://121.62.63.1:9901",
"http://122.114.171.1:9901",
"http://122.114.192.1:9901",
"http://122.138.32.1:9999",
"http://122.139.47.1:9901",
"http://122.188.62.1:8800",
"http://122.227.100.1:9901",
"http://122.230.62.1:9901",
"http://122.246.75.1:9901",
"http://122.4.92.1:9991",
"http://123.10.69.1:9901",
"http://123.10.70.1:9901",
"http://123.10.71.1:9901",
"http://123.101.144.1:9901",
"http://123.101.98.1:9898",
"http://123.12.148.1:9901",
"http://123.129.70.1:9901",
"http://123.13.28.1:9901",
"http://123.13.29.1:9901",
"http://123.13.57.1:9901",
"http://123.13.60.1:9901",
"http://123.13.80.1:9901",
"http://123.13.83.1:9901",
"http://123.130.84.1:8154",
"http://123.131.200.1:9901",
"http://123.132.234.1:8154",
"http://123.138.216.1:9902",
"http://123.138.22.1:9901",
"http://123.139.57.1:9901",
"http://123.149.160.1:9901",
"http://123.149.163.1:9901",
"http://123.154.154.1:9901",
"http://123.154.155.1:9901",
"http://123.154.157.1:9901",
"http://123.154.252.1:9901",
"http://123.154.253.1:9901",
"http://123.159.128.1:9901",
"http://123.159.135.1:9901",
"http://123.161.132.1:9901",
"http://123.161.37.1:9901",
"http://123.163.114.1:85",
"http://123.163.114.1:9901",
"http://123.163.21.1:9901",
"http://123.163.55.1:9901",
"http://123.163.94.1:9901",
"http://123.182.209.1:8088",
"http://123.182.211.1:8088",
"http://123.182.212.1:9901",
"http://123.182.247.1:4433",
"http://123.183.24.1:6666",
"http://123.183.25.1:6666",
"http://123.183.27.1:6666",
"http://123.189.36.1:9901",
"http://123.235.8.1:9901",
"http://123.4.125.1:9901",
"http://123.52.12.1:9901",
"http://123.54.171.1:9901",
"http://123.54.220.1:9901",
"http://123.55.3.1:9901",
"http://123.7.110.1:9901",
"http://123.9.47.1:9901",
"http://124.126.4.1:9901",
"http://124.128.73.1:9901",
"http://124.129.235.1:9901",
"http://124.152.247.1:2001",
"http://124.228.160.1:9901",
"http://124.229.231.1:9901",
"http://124.231.212.1:9999",
"http://124.231.213.1:9999",
"http://124.231.214.1:9999",
"http://124.234.179.1:9901",
"http://124.234.199.1:9901",
"http://124.238.110.1:9999",
"http://124.66.82.1:9901",
"http://124.90.211.1:9901",
"http://124.94.193.1:9902",
"http://125.106.86.1:9901",
"http://125.107.177.1:9901",
"http://125.107.97.1:9901",
"http://125.114.210.1:9901",
"http://125.114.241.1:9901",
"http://125.115.210.1:9901",
"http://125.119.48.1:9901",
"http://125.125.129.1:9901",
"http://125.125.133.1:9901",
"http://125.125.134.1:9901",
"http://125.125.225.1:9901",
"http://125.125.233.1:9901",
"http://125.125.234.1:9901",
"http://125.125.236.1:9901",
"http://125.32.120.1:9901",
"http://125.42.148.1:9901",
"http://125.42.150.1:9901",
"http://125.42.151.1:9901",
"http://125.43.240.1:9901",
"http://125.43.244.1:9901",
"http://125.43.247.1:9901",
"http://125.43.249.1:9901",
"http://125.71.73.1:9901",
"http://125.93.74.1:9002",
"http://139.209.36.1:9901",
"http://139.209.39.1:9901",
"http://14.106.236.1:9901",
"http://14.106.239.1:9901",
"http://14.204.108.1:9901",
"http://14.204.109.1:9901",
"http://14.204.29.1:9901",
"http://14.204.46.1:9901",
"http://14.204.53.1:9901",
"http://14.212.185.1:9901",
"http://14.216.204.1:8883",
"http://14.216.215.1:8883",
"http://14.216.218.1:8883",
"http://14.216.220.1:8883",
"http://14.216.221.1:8883",
"http://14.216.227.1:8883",
"http://14.29.76.1:9901",
"http://144.52.160.1:9901",
"http://144.52.162.1:9901",
"http://150.255.145.1:9901",
"http://150.255.149.1:9901",
"http://150.255.150.1:9901",
"http://150.255.157.1:9901",
"http://150.255.216.1:9901",
"http://153.0.204.1:9901",
"http://163.177.122.1:9901",
"http://171.104.198.1:8181",
"http://171.106.217.1:8181",
"http://171.108.239.1:8181",
"http://171.109.208.1:8099",
"http://171.109.6.1:8181",
"http://171.12.164.1:9901",
"http://171.12.189.1:9901",
"http://171.14.89.1:9901",
"http://171.35.124.1:10011",
"http://171.38.194.1:8082",
"http://171.8.75.1:8011",
"http://175.0.32.1:8081",
"http://175.0.35.1:8081",
"http://175.16.149.1:9901",
"http://175.16.151.1:9901",
"http://175.16.153.1:9901",
"http://175.16.155.1:9901",
"http://175.16.184.1:9901",
"http://175.16.198.1:9901",
"http://175.16.250.1:9901",
"http://175.18.189.1:9902",
"http://175.8.87.1:9998",
"http://180.113.102.1:5000",
"http://180.117.149.1:9901",
"http://180.124.146.1:60000",
"http://180.175.163.1:7777",
"http://180.213.174.1:9901",
"http://182.112.188.1:9901",
"http://182.112.28.1:9901",
"http://182.113.201.1:9901",
"http://182.113.206.1:9901",
"http://182.113.6.1:9901",
"http://182.114.185.1:9901",
"http://182.114.212.1:9901",
"http://182.114.214.1:9901",
"http://182.114.215.1:9901",
"http://182.114.48.1:9901",
"http://182.114.49.1:9901",
"http://182.114.50.1:9901",
"http://182.117.136.1:9901",
"http://182.117.90.1:9901",
"http://182.120.229.1:9901",
"http://182.122.122.1:9901",
"http://182.122.73.1:10086",
"http://182.125.172.1:9901",
"http://182.126.114.1:9901",
"http://182.126.115.1:9901",
"http://182.126.119.1:9901",
"http://182.150.25.1:9901",
"http://182.241.192.1:9901",
"http://182.241.193.1:9901",
"http://182.241.194.1:9901",
"http://182.34.67.1:9901",
"http://182.46.196.1:9901",
"http://183.0.186.1:8888",
"http://183.0.186.1:9900",
"http://183.10.180.1:9901",
"http://183.10.181.1:9901",
"http://183.131.246.1:9901",
"http://183.136.148.1:9901",
"http://183.203.147.1:9901",
"http://183.203.151.1:9901",
"http://183.238.113.1:8883",
"http://183.239.226.1:9901",
"http://183.24.48.1:9901",
"http://183.255.41.1:9901",
"http://183.63.15.1:9901",
"http://183.94.146.1:2222",
"http://202.100.46.1:9901",
"http://202.168.187.1:2024",
"http://202.168.187.1:9999",
"http://210.22.75.1:9901",
"http://211.142.224.1:2023",
"http://218.13.170.1:9901",
"http://218.29.147.1:9901",
"http://218.71.245.1:9901",
"http://218.74.169.1:9901",
"http://218.74.171.1:9901",
"http://218.75.241.1:9901",
"http://218.76.32.1:9901",
"http://218.77.81.1:9901",
"http://218.87.237.1:9901",
"http://219.137.202.1:9999",
"http://219.146.83.1:9902",
"http://219.146.90.1:9901",
"http://219.154.240.1:9901",
"http://219.154.241.1:9901",
"http://219.154.242.1:9901",
"http://219.154.243.1:9901",
"http://219.156.143.1:9901",
"http://219.159.194.1:8181",
"http://220.161.206.1:9901",
"http://220.163.178.1:8888",
"http://220.164.192.1:50085",
"http://220.179.68.1:9901",
"http://220.180.109.1:9901",
"http://220.180.109.1:9902",
"http://220.180.112.1:9901",
"http://220.180.229.1:9901",
"http://220.202.98.1:14901",
"http://220.248.173.1:9901",
"http://220.248.188.1:8991",
"http://220.249.114.1:9901",
"http://221.13.235.1:9901",
"http://221.14.152.1:9901",
"http://221.14.153.1:9901",
"http://221.14.155.1:9901",
"http://221.14.156.1:9901",
"http://221.14.158.1:9901",
"http://221.14.159.1:9901",
"http://221.193.168.1:9901",
"http://221.2.148.1:8154",
"http://221.205.128.1:9999",
"http://221.205.129.1:9999",
"http://221.205.130.1:9999",
"http://221.205.131.1:9999",
"http://221.206.104.1:9901",
"http://221.213.69.1:9901",
"http://221.213.94.1:9901",
"http://221.224.4.1:1111",
"http://221.224.72.1:9901",
"http://221.225.236.1:9901",
"http://221.226.4.1:9901",
"http://221.226.8.1:9527",
"http://221.233.192.1:1111",
"http://221.7.239.1:8181",
"http://221.9.97.1:9901",
"http://222.134.245.1:9901",
"http://222.136.68.1:9901",
"http://222.138.109.1:9901",
"http://222.140.9.1:9901",
"http://222.142.198.1:9901",
"http://222.142.72.1:9901",
"http://222.142.73.1:9901",
"http://222.142.93.1:9901",
"http://222.169.70.1:9901",
"http://222.173.134.1:8888",
"http://222.174.140.1:9901",
"http://222.175.199.1:9901",
"http://222.185.245.1:9901",
"http://222.190.173.1:9901",
"http://222.218.158.1:8181",
"http://222.240.60.1:9901",
"http://222.241.154.1:9901",
"http://222.243.221.1:9901",
"http://222.243.24.1:9901",
"http://222.84.192.1:8181",
"http://222.84.193.1:8181",
"http://222.89.19.1:9901",
"http://222.89.210.1:9901",
"http://222.92.7.1:3333",
"http://222.92.7.1:3334",
"http://223.151.51.1:9901",
"http://223.159.11.1:8099",
"http://223.159.8.1:8099",
"http://223.159.9.1:8099",
"http://223.166.234.1:7777",
"http://223.199.83.1:9901",
"http://223.241.247.1:9901",
"http://223.243.10.1:9008",
"http://223.243.2.1:9008",
"http://223.68.201.1:9901",
"http://223.75.123.1:9901",
"http://223.75.148.1:9901",
"http://27.14.163.1:9901",
"http://27.14.84.1:9901",
"http://27.188.213.1:9901",
"http://27.188.9.1:9901",
"http://27.192.126.1:9901",
"http://27.203.143.1:9901",
"http://27.223.98.1:9901",
"http://27.36.116.1:9901",
"http://27.8.192.1:9901",
"http://27.8.233.1:9901",
"http://27.8.243.1:9901",
"http://36.134.209.1:9901",
"http://36.136.77.1:9901",
"http://36.249.150.1:9901",
"http://36.249.151.1:9901",
"http://36.34.58.1:9901",
"http://36.35.220.1:9901",
"http://36.35.223.1:9901",
"http://36.40.236.1:9999",
"http://36.44.157.1:9901",
"http://36.44.159.1:9901",
"http://36.49.56.1:9901",
"http://36.99.134.1:9901",
"http://36.99.206.1:9901",
"http://39.152.171.1:9901",
"http://39.164.202.1:8899",
"http://39.164.222.1:888",
"http://39.165.44.1:9901",
"http://39.74.142.1:9999",
"http://42.225.203.1:9901",
"http://42.225.222.1:9901",
"http://42.235.4.1:9901",
"http://42.237.248.1:9901",
"http://42.237.26.1:9901",
"http://42.238.233.1:9901",
"http://42.238.237.1:9901",
"http://42.48.50.1:9002",
"http://42.49.148.1:9901",
"http://42.49.189.1:9008",
"http://42.5.185.1:9901",
"http://42.5.86.1:9901",
"http://47.104.163.1:9901",
"http://47.116.70.1:9901",
"http://47.122.26.1:9901",
"http://49.232.48.1:9901",
"http://49.234.31.1:7004",
"http://58.17.116.1:9908",
"http://58.19.133.1:9901",
"http://58.19.244.1:1111",
"http://58.20.77.1:9002",
"http://58.209.101.1:9901",
"http://58.210.23.1:9901",
"http://58.210.60.1:9901",
"http://58.216.229.1:9901",
"http://58.218.184.1:9901",
"http://58.220.219.1:1099",
"http://58.220.219.1:9901",
"http://58.23.26.1:9901",
"http://58.23.27.1:9901",
"http://58.242.103.1:9901",
"http://58.243.224.1:9901",
"http://58.243.234.1:9901",
"http://58.243.33.1:9901",
"http://58.243.93.1:9901",
"http://58.245.97.1:9901",
"http://58.245.99.1:9901",
"http://58.48.37.1:1111",
"http://58.48.5.1:1111",
"http://58.51.111.1:1111",
"http://58.51.111.1:9901",
"http://58.53.152.1:9901",
"http://58.53.153.1:9901",
"http://58.53.154.1:9901",
"http://58.53.155.1:9901",
"http://58.57.155.1:9901",
"http://58.57.21.1:9901",
"http://58.57.40.1:9901",
"http://59.173.183.1:9901",
"http://59.173.243.1:9901",
"http://59.32.97.1:9901",
"http://59.44.10.1:9901",
"http://59.44.203.1:9901",
"http://59.49.186.1:9901",
"http://59.49.187.1:9901",
"http://59.49.191.1:9901",
"http://59.50.106.1:9901",
"http://59.62.8.1:9901",
"http://59.63.22.1:8888",
"http://60.12.183.1:9901",
"http://60.167.15.1:9901",
"http://60.169.254.1:9901",
"http://60.172.59.1:9901",
"http://60.174.40.1:9901",
"http://60.174.86.1:9901",
"http://60.185.9.1:9",
"http://60.187.74.1:9901",
"http://60.190.18.1:9901",
"http://60.209.232.1:9901",
"http://60.213.92.1:9901",
"http://60.217.73.1:83",
"http://60.255.137.1:9901",
"http://60.255.47.1:8801",
"http://60.255.47.1:9901",
"http://60.4.9.1:9901",
"http://61.130.72.1:8888",
"http://61.136.172.1:9901",
"http://61.136.67.1:50085",
"http://61.138.128.1:19901",
"http://61.141.114.1:8883",
"http://61.143.43.1:3333",
"http://61.153.215.1:9901",
"http://61.156.228.1:8154",
"http://61.163.181.1:9901",
"http://61.173.144.1:9901",
"http://61.175.237.1:1111",
"http://61.175.237.1:9901",
"http://61.184.128.1:1111",
"http://61.184.128.1:9901",
"http://61.53.90.1:9901",
"http://61.54.14.1:9901"
]


async def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)
    return modified_urls

async def is_url_accessible(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=0.5) as response:
                if response.status == 200:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{current_time} {url}")
                    return url
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass
    return None

async def check_urls(session, urls, semaphore):
    tasks = []
    for url in urls:
        url = url.strip()
        modified_urls = await modify_urls(url)
        for modified_url in modified_urls:
            task = asyncio.create_task(is_url_accessible(session, modified_url, semaphore))
            tasks.append(task)
    results = await asyncio.gather(*tasks)
    valid_urls = [result for result in results if result]
    return valid_urls

async def fetch_json(session, url, semaphore):
    async with semaphore:
        try:
            ip_start_index = url.find("//") + 2
            ip_dot_start = url.find(".") + 1
            ip_index_second = url.find("/", ip_dot_start)
            base_url = url[:ip_start_index]
            ip_address = url[ip_start_index:ip_index_second]
            url_x = f"{base_url}{ip_address}"

            json_url = f"{url}"
            async with session.get(json_url, timeout=0.5) as response:
                json_data = await response.json()
                results = []
                try:
                    for item in json_data['data']:
                        if isinstance(item, dict):
                            name = item.get('name')
                            urlx = item.get('url')
                            if ',' in urlx:
                                urlx = "aaaaaaaa"
                            if 'http' in urlx:
                                urld = f"{urlx}"
                            else:
                                urld = f"{url_x}{urlx}"

                            if name and urlx:
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
                except Exception:
                    pass
                return results
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
            return []

async def main():
    x_urls = []
    for url in urls:
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
        ip_dot_second = url.find(".", ip_dot_start) + 1
        ip_dot_three = url.find(".", ip_dot_second) + 1
        base_url = url[:ip_start_index]
        ip_address = url[ip_start_index:ip_dot_three]
        port = url[ip_end_index:]
        ip_end = "1"
        modified_ip = f"{ip_address}{ip_end}"
        x_url = f"{base_url}{modified_ip}{port}"
        x_urls.append(x_url)
    unique_urls = set(x_urls)

    semaphore = asyncio.Semaphore(500)
    async with aiohttp.ClientSession() as session:
        valid_urls = await check_urls(session, unique_urls, semaphore)
        all_results = []
        tasks = []
        for url in valid_urls:
            task = asyncio.create_task(fetch_json(session, url, semaphore))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for sublist in results:
            all_results.extend(sublist)


    eventlet.monkey_patch()
    task_queue = eventlet.Queue()
    results = []
    error_channels = []

    def worker():
        while True:
            # 从队列中获取一个任务
            channel_name, channel_url = task_queue.get()
            try:
                channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
                lines = requests.get(channel_url, timeout=1).text.strip().split('\n')  # 获取m3u8文件内容
                ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
                ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
                ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接

                # 多获取的视频数据进行5秒钟限制
                with eventlet.Timeout(5, False):
                    start_time = datetime.datetime.now().timestamp()
                    content = requests.get(ts_url, timeout=1).content
                    end_time = datetime.datetime.now().timestamp()
                    response_time = (end_time - start_time) * 1

                if content:
                    with open(ts_lists_0, 'ab') as f:
                        f.write(content)  # 写入文件
                    file_size = len(content)
                    # print(f"文件大小：{file_size} 字节")
                    download_speed = file_size / response_time / 1024
                    # print(f"下载速度：{download_speed:.3f} kB/s")
                    normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                    # print(f"标准化后的速率：{normalized_speed:.3f} MB/s")

                    # 删除下载的文件
                    os.remove(ts_lists_0)
                    result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                    results.append(result)
                    numberx = (len(results) + len(error_channels)) / len(all_results) * 100
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{current_time}可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(all_results)} 个 ,总进度：{numberx:.2f} %。")
            except:
                error_channel = channel_name, channel_url
                error_channels.append(error_channel)
                numberx = (len(results) + len(error_channels)) / len(all_results) * 100
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{current_time}可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(all_results)} 个 ,总进度：{numberx:.2f} %。")

            # 标记任务完成
            task_queue.task_done()

    def channel_key(channel_name):
        match = re.search(r'\d+', channel_name)
        if match:
            return int(match.group())
        else:
            return float('inf')



    # 创建工作线程
    num_workers = 10
    #pool = eventlet.GreenPool(num_workers)
    for _ in range(num_workers):
        #pool.spawn(worker)
        t = threading.Thread(target=worker, daemon=True)  # 将工作线程设置为守护线程
        t.start()


    # 将all_results中的数据放入任务队列
    for result in all_results:
        channel_name, channel_url = result.split(',')
        task_queue.put((channel_name, channel_url))


    # 等待所有任务完成
    task_queue.join()

    # 对结果进行排序
    #results.sort(key=lambda x: channel_key(x[0]))
    results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
    results.sort(key=lambda x: channel_key(x[0]))

    # 保存结果到文件
    with open("speed_results.txt", 'w', encoding='utf-8') as file:
        for result in results:
            file.write(f"{result[0]},{result[1]},{result[2]}\n")

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


if __name__ == "__main__":
    asyncio.run(main())
