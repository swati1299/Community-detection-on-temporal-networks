import csv
import os
import networkx as nx

from sklearn.metrics.cluster import normalized_mutual_info_score

from karateclub.community_detection.non_overlapping import LabelPropagation, EdMot, GEMSEC, SCD
from karateclub.dataset.dataset_reader import GraphReader


def run(model,graph):
    model.fit(graph)
    cluster_membership = model.get_memberships()
    cluster_membership = [cluster_membership[node] for node in range(len(cluster_membership))]
    return cluster_membership

nums=[802,810,822,834,844,853, 863,878, 883, 999]
for num in nums:
    reader = GraphReader("snapshot_%s"%num)
    graph = reader.get_graph()
    target = reader.get_target()
    d={}
    model = LabelPropagation()
    cluster_membership=run(model,graph)
    nmi = normalized_mutual_info_score(target,cluster_membership)
    d['label']=nmi
    model = EdMot()
    cluster_membership = run(model, graph)
    nmi = normalized_mutual_info_score(target, cluster_membership)
    d['edmot'] = nmi

    model = GEMSEC()
    cluster_membership = run(model, graph)
    nmi = normalized_mutual_info_score(target, cluster_membership)
    d['gemsec'] = nmi

    model = SCD()
    cluster_membership = run(model, graph)
    nmi = normalized_mutual_info_score(target, cluster_membership)
    d['scd'] = nmi

    print(d)
    path=os.getcwd()
    #os.makedirs(str(path)+str(os.sep)+"scores")
    file=open(str(path)+"/scores/nmi-%s.csv" % num, "w")
    cs=csv.writer(file)
    cs.writerow(['graph',"algo","nmi"])
    for key in d.keys():
        cs.writerow([num,key,d[key]])
    file.flush()
    file.close()
