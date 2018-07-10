#coding:utf-8

import requests
import re
from bs4 import BeautifulSoup

#all the following functions return 1000000, which is a integer

def get_search_results_Google(keyword):
	r = requests.get("https://www.google.com/search",params={'q':keyword})
	soup = BeautifulSoup(r.text)
	res = soup.find("div",{"id":"resultStats"})
	n_text = res.text.split(' ')[1].split(',')
	number = ""
	for n in n_text:
		number+=n
	return int(number)

def get_search_results_Baidu(keyword):
	r = requests.get("http://www.baidu.com/s",params={'wd':keyword})
	soup = BeautifulSoup(r.text)
	res = soup.find("div",{"class":"nums"})
	n_text=re.findall(r"\d+",res.text)
	number=""
	for n in n_text:
		number+=n
	return int(number)

def get_search_results_Bing(keyword):
	r = requests.get("https://www.bing.com/search",params={'q':keyword})
	soup = BeautifulSoup(r.text)
	res = soup.find("span",{"class":"sb_count"})
	n_text = res.text.split(' ')[0].split(',')
	number = ""
	for n in n_text:
		number+=n
	return int(number)

#print get_search_results_Google("test")
print(get_search_results_Baidu("huawei_p9 android"))
print(get_search_results_Baidu("huawei_p9 ios"))
print(get_search_results_Bing("huawei_p9 android"))
print(get_search_results_Bing("huawei_p9 ios"))


