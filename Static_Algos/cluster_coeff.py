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
    return l

nums=[802,810,822,834,844,853, 863,878, 883, 999]
for num in nums:
    reader = GraphReader("twitch%s"%num)
    graph = reader.get_graph()
    target = reader.get_target()
    d={}
    model = LabelPropagation()
    comms=run(model,graph)
    coeffs=[]
    for key in sorted(comms.keys()):
        sub=graph.subgraph(list(comms[key]))
        coeff=nx.average_clustering(sub)
        coeffs.append(coeff)
    avg_coeff=sum(coeffs)/len(coeffs)
    d['label']=avg_coeff


    model = EdMot()
    comms = run(model, graph)
    coeffs = []
    for key in sorted(comms.keys()):
        sub = graph.subgraph(list(comms[key]))
        coeff = nx.average_clustering(sub)
        coeffs.append(coeff)
    avg_coeff = sum(coeffs) / len(coeffs)
    d['edmot'] = avg_coeff


    model = GEMSEC()
    comms = run(model, graph)
    coeffs = []
    for key in sorted(comms.keys()):
        sub = graph.subgraph(list(comms[key]))
        coeff = nx.average_clustering(sub)
        coeffs.append(coeff)
    avg_coeff = sum(coeffs) / len(coeffs)
    d['gemsec'] = avg_coeff


    model = SCD()
    comms = run(model, graph)
    coeffs = []
    for key in sorted(comms.keys()):
        sub = graph.subgraph(list(comms[key]))
        coeff = nx.average_clustering(sub)
        coeffs.append(coeff)
    avg_coeff = sum(coeffs) / len(coeffs)
    d['scd'] = avg_coeff
    print(d)
    path=os.getcwd()
    #os.makedirs(str(path)+str(os.sep)+"scores")
    file=open(str(path)+"/scores/cluster_coeff-%s.csv" % num, "w")
    cs=csv.writer(file)
    cs.writerow(['graph',"algo","cluster_coeff"])
    for key in d.keys():
        cs.writerow([num,key,d[key]])
    file.flush()
    file.close()
