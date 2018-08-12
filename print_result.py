import pickle

with open ('zone_list.txt', 'rb') as fp:
    zone = pickle.load(fp)
with open ('department_list.txt', 'rb') as fp:
    department = pickle.load(fp)
c=0
for i in range(0,len(zone)):
	if zone[i]=="No zone found":
		print(zone[i])
		c=c+1
	else:
		print(zone[i]+","+department[i])
#print(c)