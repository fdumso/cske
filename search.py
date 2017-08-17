import requests
from bs4 import BeautifulSoup

#return "About 1,000,000 results"
def get_search_results_text(keyword):
	r = requests.get("https://www.google.com/search",params={'q':keyword})
	soup = BeautifulSoup(r.text,"lxml")
	res = soup.find("div",{"id":"resultStats"})
	return res.text

#return 1000000, that is a integer
def get_search_results_number(keyword):
	r = requests.get("https://www.google.com/search",params={'q':keyword})
	soup = BeautifulSoup(r.text,"lxml")
	res = soup.find("div",{"id":"resultStats"})
	n_text = res.split(' ')[1].split(',')
	number = ""
	for n in n_text:
		number+=n
	return int(number)

print get_search_results_number("android device")