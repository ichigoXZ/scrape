# -*- coding: utf-8 -*-

import requests
import json
import csv

title = ['序号', 'WOS', '论文标题', '作者', 'source', 
	'research fields','times cited', '是否属于research fronts', 'Research fronts名称',
	'top papers', 'cites to top paper', 'cites/top paper', 'mean year']

keys = ['rowSeq', 'articleUT', 'docTitle', 'authors', 'sourceOfBIB',
	'researchFieldName', 'citations']

ft_keys = ['researchFront', 'topPapers', 'citesTopPapers', 
	'citesPerPaper', 'meanYear']

params = { '_dc': '1544667120140',
			'type': 'grid',
			'groupBy': 'ResearchFronts',
			'filterBy': 'ResearchFronts',
			'filterValues': '',
			'docType': 'Top',
			'page': '1',
			'start': '0',
			'sort': '[{"property":"highPapers","direction":"DESC"}]'}



s = requests.Session()
s.get("https://esi.incites.thomsonreuters.com/DocumentsAction.action")

r = s.get('https://esi.incites.thomsonreuters.com/IndicatorsDataAction.action?_dc=1544620436028&type=documents&author=&researchField=&institution=HUAZHONG%20UNIVERSITY%20OF%20SCIENCE%20%26%20TECHNOLOGY&journal=&territory=&article_UT=&researchFront=&articleTitle=&docType=Top&year=&page=1&start=0&sort=%5B%7B%22property%22%3A%22citations%22%2C%22direction%22%3A%22DESC%22%7D%5D')
js = r.json()


with open("topPapers.csv","w") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerow(title)

    for item in js['data']:
		row = []
		for key in keys:
			row.append(item[key])
		if 'researchFrontName' in item.keys():
			row.append('Y')
			params['filterValues'] = item['researchFrontName']
			ft = s.get("https://esi.incites.thomsonreuters.com/IndicatorsDataAction.action",params=params).json()
			front = ft['data'][0]
			for key in ft_keys:
				row.append(front[key])
		else:
			row.append('N')
		writer.writerow(row)
		print(item['rowSeq'])
