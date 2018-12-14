# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')

proxies = {
	'http.proxy': 'socks5://127.0.0.1:1080',
	'https.proxy': 'socks5//127.0.0.1:1080'
}
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

url = 'https://dl.acm.org/tab_about.cfm?id=J204&type=periodical&sellOnline=0&parent_id=J204&parent_type=periodical&title=ACM%20Computing%20Surveys%20%28CSUR%29&toctitle=&tocissue_date=&notoc=0&usebody=tabbody&tocnext_id=&tocnext_str=&tocprev_id=&tocprev_str=&toctype=&_cf_containerId=cf_layoutareaprox&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=72DD577A40470AC670AB58F7F5E59F92&_cf_rc=1'
url2 = 'https://dl.acm.org/tab_about.cfm?type=issue&sellOnline=0&parent_id=J204&parent_type=periodical&title=ACM%20Computing%20Surveys%20%28CSUR%29&toctitle=ACM%20Computing%20Surveys%20%28CSUR%29&tocissue_date=Volume%2051%20Issue%205%2C%20December%202018&notoc=0&usebody=tabbody&tocnext_id=&tocnext_str=&tocprev_id=3236632&tocprev_str=Volume%2051%20Issue%204,%20September%202018&toctype=Issue&_cf_containerId=cf_layoutareaprox&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=72DD577A40470AC670AB58F7F5E59F92&_cf_rc=1'
home = 'https://dl.acm.org/'

r = requests.get(url, headers=headers, proxies=proxies)

bsObj = BeautifulSoup(r.text, 'html.parser')

with open("csur.csv","w") as csvfile:
	writer = csv.writer(csvfile)

	for link in bsObj.findAll("a"):
		if 'href' in link.attrs:
			# print(link.text)
			id = link.attrs['href'].split('=')[-1]
			rs = requests.get(url2, params={'id': id}, headers=headers, proxies=proxies)
			bsObj2 = BeautifulSoup(rs.text, 'html.parser')
			for line in bsObj2.findAll('a', href=re.compile('citation.*[0-9]$')):
				# print(line.text)
				writer.writerow([link.text, line.text, home+line.attrs['href']])



			


