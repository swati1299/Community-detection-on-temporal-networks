import matplotlib.pyplot as plt
import csv
x =[]
for i in range(0,980):
	x.append(i)
#print(x)

cc=[]
import os
fil= "coeff"+str(os.sep)+'cluster_coeff.csv'

with open(fil) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter= ',')
	cnt=0
	for row in csv_reader:
		print(row)
		print('\n')
		if cnt== 0:
			cnt+=1
		else:
			cc.append(float(row[1]))
			cnt+=1
	csv_file.close()

print(cc)

plt.plot(x, cc, color='blue', linewidth = 1,
		marker='o', markerfacecolor='blue', markersize=4,label="TILES")



plt.xlabel('Time')
plt.ylabel('Average Cluster Coefficients')
plt.title('TILES: Cluster Coefficients With Time')

plt.show()
