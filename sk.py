# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup 
import csv

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

# 华中科技大学 300条记录
# url= u'http://fz.people.com.cn/skygb/sk/index.php/Index/seach?gzdw=%E5%8D%8E%E4%B8%AD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6'
# page = 15 
# 图书馆 278条记录
# url = u'http://fz.people.com.cn/skygb/sk/index.php/Index/seach?gzdw=%E5%9B%BE%E4%B9%A6%E9%A6%86'
# page = 14
# 图书馆分类 1842条记录
url = u'http://fz.people.com.cn/skygb/sk/index.php/Index/seach?xktype=%E5%9B%BE%E4%B9%A6%E9%A6%86%E3%80%81%E6%83%85%E6%8A%A5%E4%B8%8E%E6%96%87%E7%8C%AE%E5%AD%A6'
page = 93

s = requests.session()
r = s.get(url)

bsObj = BeautifulSoup(r.text, 'lxml')
table = bsObj.find('table').find_all('table')[1]
head = ['']
with open("libentry.csv","w") as csvfile:
	writer = csv.writer(csvfile)
	for th in table.find('tr').find_all('th'):
		head.append(th.get_text())
	writer.writerow(head)
	no = 1
	p = 1
	while True:
		for item in table.find_all('tr')[1:]:
			# print(item)
			pro = [no]
			for td in item.find_all('td'):
				# print(td.get_text())
				pro.append(td.get_text())
			writer.writerow(pro)
			no = no + 1
		p = p + 1
		if p > page:
			break
		next_url = url + '&p=' + str(p)
		r = s.get(next_url)
		bsObj = BeautifulSoup(r.text, 'lxml')
		table = bsObj.find('table').find_all('table')[1]
	


# print(table)

# with open("csur.csv","w") as csvfile:
# 	writer = csv.writer(csvfile)