from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import csv
import time

headurl = 'https://www.usnews.com'

user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",

                    ] 

def openweb(url):
	# 找到一个可用的user_agent
	ok = 0
	for agent in user_agents:
		try:
			req = Request(url, headers={'User-Agent':agent})
			webpage = urlopen(req)
			ok = 1
			bsObj = BeautifulSoup(webpage, features="html.parser")
			break
		except HTTPError:
			pass
	if not ok:
		sleep(.5) 	# 等待0.5秒再试
		bsObj = openweb(url)
	return bsObj

def rankscrape(starturl):
	with open("rank.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerow(['排名', '学校', '国家', 'Global score'])

		def pagerank(bsObj):
			# 搜集该页的排名数据
			for child in bsObj.find(id='resultsMain').find_all(name='div', attrs={"class":"sep"}):
				no = child.find('span', {"class","rankscore-bronze"}).get_text().strip().split(" ")[0].strip()
				name = child.a.get_text()
				nation = child.find('div',{"class":"t-taut"}).span.get_text()
				score = child.find("div",{"class":"t-large t-strong t-constricted"}).get_text().strip()
				# link = child.a.attrs['href']
				item = [no,name,nation,score]
				print(item)
				writer.writerow(item)
				# print(link)

		bsObj = openweb(starturl)
		while True:
			pagerank(bsObj)
			if bsObj.find('div', {"class":"pagination"}).find(text=re.compile('Next')):
				nextpage = bsObj.find('div', {"class":"pagination"}).find_all("a")[-1].attrs['href']
			else:
				return

			bsObj = openweb(headurl + nextpage)
			

rankscrape('https://www.usnews.com/education/best-global-universities/rankings')

