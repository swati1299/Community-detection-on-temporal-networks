import csv
import os
import networkx as nx
from karateclub.community_detection.non_overlapping import LabelPropagation, EdMot, GEMSEC, SCD
from karateclub.dataset.dataset_reader import GraphReader
sum=0
nums=[802,810,822,834,844,853, 863,878, 883, 999]
algs=['label','edmot','gemsec','scd']

for alg_name in algs:
    path=str(os.getcwd())+"/scores/"+str(alg_name)
    if not os.path.exists(str(path)):
        os.makedirs(path)
    prev_num=802
    for num in nums:
        if num!=802:
            file = open(str(path)+str(os.sep)+"comm_map_after_slice"+str(prev_num)+".csv", "w")
            csvwriter = csv.writer(file)
            csvwriter.writerow(['comm_from', 'comm_to'])
        reader = GraphReader("twitch%s" % num)
        graph = reader.get_graph()
        if alg_name=='label':
            model=LabelPropagation()
        elif alg_name=='edmot':
            model=EdMot()
        elif alg_name=='gemsec':
            model=GEMSEC()
        else:
            model=SCD()
        l = {}
        model.fit(graph)
        cluster_membership = model.get_memberships()
        #print(cluster_membership)
        for key in sorted(cluster_membership.keys()):
            try:
                l[cluster_membership[key]].add(key)
            except:
                l[cluster_membership[key]] = {key}
        if num==802:
            prev_l=l
        else:
            #kaam yaha write ka
            for comm_num in sorted(prev_l.keys()):
                if comm_num in l.keys():
                    csvwriter.writerow([comm_num,comm_num])
                else:
                    mergewith=0
                    max_common=-1
                    for o_comm_num in sorted(l.keys()):
                        common=prev_l[comm_num].intersection(l[o_comm_num])
                        if len(common)>max_common:
                            mergewith=o_comm_num
                            max_common=len(common)
                    csvwriter.writerow([comm_num,mergewith])
            prev_l=l
            prev_num=num
        if num!=802:
            file.flush()
            file.close()
    exit()
