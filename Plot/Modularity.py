import matplotlib.pyplot as plt
import csv
x =[]
for i in range(1,11):
	x.append(i)
#print(x)

nums= [802,810,822,834,844,853,863,878,883,999]
label=[]
edmot=[]
gemsec=[]
scd=[]

file_name= "modularity-"
for num in nums:
	fil= file_name+ str(num)+".csv"
	with open(fil) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter= ',')
		cnt=0
		for row in csv_reader:
			print(row)
			print('\n')
			if cnt== 0:
				cnt+=1
			else:
				if cnt==1:
					label.append(float(row[2]))
				elif cnt==2:
					edmot.append(float(row[2]))
				elif cnt==3:
					gemsec.append(float(row[2]))
				else:
					scd.append(float(row[2]))
				cnt+=1
	csv_file.close()

#print(edmot)

plt.plot(x, edmot, color='aqua', linestyle='dashed', linewidth = 2,
		marker='o', markerfacecolor='aqua', markersize=12,label="EdMot")

plt.plot(x, gemsec, color='green', linestyle='dashed', linewidth = 2,
		marker='o', markerfacecolor='lightgreen', markersize=12, label="GEMSEC")

plt.plot(x, label, color='steelblue', linestyle='dashed', linewidth = 2,
		marker='o', markerfacecolor='steelblue', markersize=12,label="Label Propagation")

plt.plot(x, scd, color='khaki', linestyle='solid', linewidth = 2,
		marker='o', markerfacecolor='khaki', markersize=12,label="SCD")

plt.xlabel('Time')
plt.ylabel('Modularity')
plt.title('Modularity With Time')

plt.legend()

plt.show()