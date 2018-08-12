import json
import pickle
#all station list to search sttaion names in corpus
with open('station_list.txt') as f:
    temp = f.read().splitlines()
with open('station_to_station_code.txt', 'r') as f:
    data = json.load(f)
with open('station_code_to_zone.txt', 'r') as f:
    data_2 = json.load(f)
with open('train_to_station.txt', 'r') as f:
    data_3 = json.load(f)
    #dictinaries of railways zone
new_dict={"Northern railway" : "NR","North Eastern Railway":"NER","Northeast Frontier Railway":"NFR","Eastern Railway":"ER","South Eastern Railway":"SER","South Central Railway":"SCR","Southern Railway":"SR","Central Railway":"CR","Western Railway":"WR","South Western Railway":"SWR","North Western Railway":"NWR","West Central Railway":"WCR","North Central Railway":"NCR","South East Central Railway":"SECR","East Coast Railway":"ECoR","East Central Railway":"ECR","Metro Railway":"MTP","Konkan Railway":"KR"}
ndict=new_dict = dict (zip(new_dict.values(),new_dict.keys()))
itemlist=[]
d=open("testing_body.txt")
for line in d.readlines():
    itemlist.append(line)

import re
t = re.compile(r'\b\d{5}\b')
p = re.compile(r'\b\d{10}\b')    



#print(itemlist)
zone_list=[]
#first append no zone to all data.
for i in range(0,len(itemlist)):
    zone_list.append("No zone found")
number=[]
for i in range(0,len(itemlist)):
    number.append("")

# for smooth search convert ganga pur to ganga_pur
def find_str(s, char):
    index = 0

    if char in s and len(char)>0:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    if index==0 and s[index+len(char)+1]=='_':
                        return True
                    if s[index-1]=='_' and s[index+len(char)+1]=='_':
                        return True
            index += 1
    return False

# to search train no / pnr no/ or any station name mentioned in 
# corpus
for e in range(0,len(itemlist)): 
    #print(e)
    h=0
    z=re.findall(r"\b\d{5}\b", str(itemlist[e]))
    #print(z)
    #print(e)
    # train no of 5 length
    if len(z)!=0:
        h=1
        number[e]=str(z[0])
    else:
        z=re.findall(r"\b\d{10}\b", str(itemlist[e]))
        if len(z)!=0:
            g=0
            while g<len(z):
                if z[g][0]=='9' or z[g][0]=='8' or z[g][0]=='7':
                    g=g+1
            if g!=len(z):
                number[i]=str(z[g])
# searching for name if no train no or pnr no is found
    if h==0:
        #print(e)
        #print(-1)
        stat=[]
        line=itemlist[e]
        for i in temp: #temp station list
            j=i.lower()
            j=j.replace(" junction","")
            j=j.replace(" main","")
            j=j.replace(" ","_")
            line=line.lower()
            line=line.replace(" ","_")

            if find_str(line,j):
                stat.append(str(i))
        #print(stat)
        if len(stat)!=0:
            if len(stat[0])!=0:
                #print(stat[0])
                #print(e)
                if str(stat[0]) in data and data[str(stat[0])] in data_2 and data_2[data[str(stat[0])]] in ndict: 
                    zone_list[e]=ndict[data_2[data[str(stat[0])]]]

# function for text cleaning and processing
import requests
from bs4 import BeautifulSoup
from time import sleep
import io
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#print(number)
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)

# get the status of pnr no online from railyatri website to find train no
for i in range(0,len(number)):
    if number[i]!=0 and len(number[i])==10:
        #print(number[i])
        url = 'http://www.railyatri.in/pnr-status/' + str(number[i])
        page = requests.get(url)
        page
        soup = BeautifulSoup(page.content, 'html.parser')
        soup=(soup.find_all( 'div',class_=' col-xs-12 train-info'))
        s=str(soup) 
        #print(s)
        line=s
        words=cleanhtml(line)
        stop_words = set(stopwords.words('english'))
        line = words
        #print(words)
        line=remove_urls(line)
        words = line.split()
        f=0
        stre=""
        for r in words:
            if not r in stop_words:
                f=0
                for l in r:
                    if l=='[':
                        f=1
                        break
                if f==0:
                    stre=stre+str(r)
        #print(stre)
        line=stre
        train_no=""
        for s in line.split():
            for r in s:
                if r.isdigit():
                    train_no=train_no+str(r)
        number[i]=str(train_no)

import requests
import json
import types
# finding zone from train no to zone dictionaries
for i in range(0,len(number)):
    print(i+1)
    if len(number[i])==0:
        #print(itemlist[i])
        #print(zone_list[i]) 
        #print(i+1) 
        continue
    if zone_list[i]!="No zone found":
        #print(itemlist[i])
        
        #print(zone_list[i]) 
        #print(i+1) 
        continue
    if str (number[i]) in data_3:
        z=data_3[number[i]]
        if z in data_2:
            zone_list[i]=ndict[data_2[z]]
            #print(itemlist[i])
        
            #print(zone_list[i])
            #print(i+1)
            continue
#getting schedule of train online from travel khana and saving in file
    url_to_scrape = "https://www.travelkhana.com/travelkhana/utilities/trainStations.jsp?train="+str(number[i])
    r = requests.get(url_to_scrape)
    soup = BeautifulSoup(r.text,"lxml")
    inmates_list = []
    f=open("station_shedule.txt","w+")
    for table_row in soup.select("table.table-bordered.table-train  tr"):
        cells = table_row.findAll('td')
        stat=table_row.findAll('th',class_='station-name')
        if len(cells) > 0:
            f.write("%s "%stat)

    f.close()
# finding zone list from station schedule
# using dictionaries of station code to zone and zone code 
    d=open("station_shedule.txt")
    line=d.read()
    words=cleanhtml(line)
    d.close()
    f=open("station_shedule.txt","w+")
    f.write("%s"%words)
    f.close()
    with open('zone_list.txt', 'w') as f:
        json.dump(new_dict, f)
    with open('station_code_to_zone.txt', 'r') as f:
        data = json.load(f)
    
    with open("station_shedule.txt") as f:
        flag=0
                  
        for line in f.readlines():
            z=re.findall('\(([^)]+)', line)
            for word in z:
                #print((ndict[data[word]]))
                #print(word)
                if word in data_2 and data_2[word] in ndict:
                    zone_list[i]=(ndict[data_2[word]])
                    flag=1

                    break

            if flag==1:
                break
    #print(itemlist[i])
        
    #print(zone_list[i]) 
    #print("")
    #print(i+1)  
with open('zone_list.txt', 'wb') as fp:
    pickle.dump(zone_list, fp)


#print(itemlist[0]+","+zone_list[0])