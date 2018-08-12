
import requests
from bs4 import BeautifulSoup
url_to_scrape = 'https://www.travelkhana.com/travelkhana/utilities/trainStations.jsp?train='+str(12294)

r = requests.get(url_to_scrape)
soup = BeautifulSoup(r.text,"lxml")
inmates_list = []
f=open("station_shedule.txt","w+")
for table_row in soup.select("table.table-bordered.table-train  tr"):
	cells = table_row.findAll('td')
	stat=table_row.findAll('th',class_='station-name')
	if len(cells) > 0:
		end = cells[1].text.strip()
		start = cells[0].text.strip()
		inmate = {'start': start, 'end': end}
		f.write("%s "%stat)
		f.write("%s\n"%inmate)
		inmates_list.append(inmate)

f.close()
import io
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

d=open("station_shedule.txt")

line=d.read()
words=cleanhtml(line)

d.close()

f=open("station_shedule.txt","w+")

f.write("%s"%words)

f.close()

import re
import json
import types
new_dict={"Northern railway" : "NR","North Eastern Railway":"NER","Northeast Frontier Railway":"NFR","Eastern Railway":"ER","South Eastern Railway":"SER","South Central Railway":"SCR","Southern Railway":"SR","Central Railway":"CR","Western Railway":"WR","South Western Railway":"SWR","North Western Railway":"NWR","West Central Railway":"WCR","North Central Railway":"NCR","South East Central Railway":"SECR","East Coast Railway":"ECoR","East Central Railway":"ECR","Metro Railway":"MTP","Konkan Railway":"KR"}
ndict=new_dict = dict (zip(new_dict.values(),new_dict.keys()))
with open('zone_list.txt', 'w') as f:
     json.dump(new_dict, f)
with open('station_code_to_zone.txt', 'r') as f:
     data = json.load(f)
with open('zone_list.txt', 'r') as f:
     zone = json.load(f)
with open("station_shedule.txt") as f:
	p = re.compile(r'\b\d{5}\b')
	flag=0
                  
	for line in f:
		for word in re.findall('\(([^)]+)', line):
			print(zone[data[word]])
			flag=1
			break

		if flag==1:
			break	