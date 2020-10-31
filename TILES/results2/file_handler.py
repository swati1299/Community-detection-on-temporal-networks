import gzip
import networkx as nx
import os
import csv

file=open("coeff/cluster_coeff.csv","w")
cwriter=csv.writer(file)
cwriter.writerow(["graph","avg_clus_coeff"])
file2=open("coeff/NUM_COMMS.csv","w")
comwrite=csv.writer(file2)
comwrite.writerow(["graph","num_comms"])
file3=open("coeff/NUM_NODES.csv","w")
nodewrite=csv.writer(file3)
nodewrite.writerow(["graph","num_nodes"])
for num in range(0,980):
    cond={}
    fin=gzip.open("graph-%s.gz"%num,"r")
    G=nx.Graph()
    for line in fin:
        s,d,w=line.split()
        G.add_edge(s,d)
    fin.close()
    nodewrite.writerow([num,nx.number_of_nodes(G)])
    clus_coeff=nx.average_clustering(G)
    cwriter.writerow([num,clus_coeff])
    cin=gzip.open("strong-communities-%s.gz"%num,"r")
    data=cin.read()
    numcom=data.split(b'\n')
    comwrite.writerow([num,len(numcom)])
    cin.close()
file2.flush()
file.flush()
file3.flush()
file2.close()
file.close()
file3.close()