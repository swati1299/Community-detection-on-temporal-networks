import gzip
import networkx as nx
import os
import csv
from sklearn.metrics.cluster import normalized_mutual_info_score as NMI

# 0 to 2799
nums=[207, 292, 377, 462, 547, 632, 717, 802, 887, 979]
file=open("coeff/tiles_modularity.csv","w")
cwriter=csv.writer(file)
cwriter.writerow(["graph","modularity"])
for num in range(0,980):
    cond={}
    fin=gzip.open("graph-%s.gz"%num,"r")
    G=nx.Graph()
    for line in fin:
        s,d,w=map(int,line.split())
        G.add_edge(s,d)
    fin.close()
    num_edges=G.number_of_edges()
    node_to_comm={}
    modularity=0
    #cwriter.writerow([num,clus_coeff])
    cin=gzip.open("strong-communities-%s.gz"%num,"r")
    data=cin.read()
    allcom=data.split(b'\n')
    for row in allcom:
        if row!=b'':
            row=row.split(b'\t')
            comm_ID=int(row[0])
            row=row[1].replace(b'[',b'')
            row=row.replace(b']',b'')
            row=row.replace(b',',b'')
            members=list(map(int,row.split(b' ')))
            #print(G.nodes,members)
            subG=G.subgraph(members)
            deg_sum=0
            for node in members:
                deg_sum+=G.degree[node]
            modularity += (subG.number_of_edges()-((deg_sum*deg_sum)/(4*num_edges)))
    cin.close()
    cwriter.writerow([num,modularity/num_edges])
file.flush()
file.close()
