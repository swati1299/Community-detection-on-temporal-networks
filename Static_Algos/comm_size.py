import csv
import os
import networkx as nx
from karateclub.community_detection.non_overlapping import LabelPropagation, EdMot, GEMSEC, SCD
from karateclub.dataset.dataset_reader import GraphReader

nums=[802,810,822,834,844,853, 863,878, 883, 999]
algs=['label','edmot','gemsec','scd']
for alg_name in algs:
    path=str(os.getcwd())+"/scores/"+str(alg_name)
    if not os.path.exists(str(path)):
        os.makedirs(path)
    for num in nums:
        file = open(str(path)+str(os.sep)+str(alg_name)+"_"+str(num)+".csv", "w")
        csvwriter = csv.writer(file)
        csvwriter.writerow(['comm', 'size'])
        reader = GraphReader("twitch%s" % num)
        graph = reader.get_graph()
        if alg_name=='label':
            model=LabelPropagation()
        elif alg_name=='edmot':
            model=EdMot()
        elif alg_name=='gemsec':
            model=GEMSEC()
        elif alg_name=='scd':
            model=SCD()
        l = {}
        model.fit(graph)
        cluster_membership = model.get_memberships()
        for key in sorted(cluster_membership.keys()):
            try:
                l[cluster_membership[key]].add(key)
            except:
                l[cluster_membership[key]] = {key}
        tot=0
        for key in sorted(l.keys()):
            csvwriter.writerow([key,len(l[key])])
            tot+=len(l[key])
        print(tot)
        file.flush()
        file.close()