import csv
import os
import networkx as nx

from karateclub.community_detection.non_overlapping import LabelPropagation, EdMot, GEMSEC, SCD
from karateclub.dataset.dataset_reader import GraphReader


def run(model,graph):
    l={}
    model.fit(graph)
    cluster_membership = model.get_memberships()
    for key in sorted(cluster_membership.keys()):
        try:
            l[cluster_membership[key]].add(key)
        except:
            l[cluster_membership[key]]={key}
    ret=[]
    for key in sorted(l.keys()):
        ret.append(l[key])
    return ret

nums=[802,810,822,834,844,853, 863,878, 883, 999]
for num in nums:
    reader = GraphReader("snapshot_%s"%num)
    graph = reader.get_graph()
    target = reader.get_target()
    d={}
    model = LabelPropagation()
    comms=run(model,graph)
    modularity= nx.algorithms.community.modularity(graph,comms)
    d['label']=modularity
    model = EdMot()
    comms = run(model, graph)
    modularity = nx.algorithms.community.modularity(graph, comms)
    d['edmot'] = modularity
    model = GEMSEC()
    comms = run(model, graph)
    modularity = nx.algorithms.community.modularity(graph, comms)
    d['gemsec'] = modularity
    model = SCD()
    comms = run(model, graph)
    modularity = nx.algorithms.community.modularity(graph, comms)
    d['scd'] = modularity
    print(d)
    path=os.getcwd()
    #os.makedirs(str(path)+str(os.sep)+"scores")
    file=open(str(path)+"/scores/modularity-%s.csv" % num, "w")
    cs=csv.writer(file)
    cs.writerow(['graph',"algo","modularity"])
    for key in d.keys():
        cs.writerow([num,key,d[key]])
    file.flush()
    file.close()
