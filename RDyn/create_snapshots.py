import os
import csv
base=os.getcwd()

size = 1000
iterations = 1000
avg_deg = 15
sigma = 0.7
renewal = 0.8
max_evts = 1
quality_threshold=0.3

nums=[802,810,822,834,844,853, 863,878, 883, 999]
output_dir = str(base)+str(os.sep)+"results"+str(os.sep)+ str(size)+str(iterations)+ str(avg_deg)+ str(sigma)+ str(renewal)+str(quality_threshold)+str(max_evts)
com_files=output_dir+str(os.sep)+"communities-"
suff=".txt"
target_dir=output_dir+str(os.sep)+"ready"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
print(target_dir)
node_to_com={}
all_nodes=[]
for num in nums:
    commfile=open(str(com_files)+str(num)+suff,"r")
    for line in commfile:
        x=line.split('\t')
        comID=int(x[0])
        nodelist=x[1].replace('[',' ')
        nodelist=nodelist.replace(']',' ')
        nodelist=nodelist.replace('\n',' ')
        nodelist=nodelist.replace(',',' ')
        nodelist=list(map(int,nodelist.split()))
        all_nodes+=nodelist
        for node in nodelist:
            node_to_com[node]=comID
    target_file=open(str(target_dir)+str(os.sep)+"target-"+str(num)+".csv","w")
    csvwriter=csv.writer(target_file)
    csvwriter.writerow(['id','target'])
    for node in set(all_nodes):
        csvwriter.writerow([node,node_to_com[node]])
    commfile.flush()
    commfile.close()
    target_file.flush()
    target_file.close()
'''
for num in nums:
    graph_file=open(str(target_dir)+str(os.sep)+"graph-%s.csv"%num,"w")
    csvwriter=csv.writer(graph_file)
    csvwriter.writerow(['id_1','id_2'])
    graph_in=open(str(output_dir)+str(os.sep)+"graph-%s.txt"%num,"r")
    for line in graph_in:
        x,y=line.split()
        csvwriter.writerow([x,y])
    graph_file.close()
    graph_in.close()
'''