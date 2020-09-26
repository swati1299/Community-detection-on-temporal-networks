import os
import networkx as nx
import random as rd
import future.utils
import argparse
class RDyn(object):
    def __init__(self, size=1000, iterations=100, avg_deg=15, sigma=.6,
                 lambdad=1, alpha=2.5, paction=1, prenewal=.8,
                 quality_threshold=.2, new_node=.0, del_node=.0, max_evts=1):

        # set the network generator parameters
        self.size = size
        self.iterations = iterations
        self.avg_deg = avg_deg
        self.sigma = sigma
        self.lambdad = lambdad
        self.exponent = alpha
        self.paction = paction
        self.renewal = prenewal
        self.new_node = new_node
        self.del_node = del_node
        self.max_evts = max_evts

        # event targets
        self.communities_involved = []

        # initialize communities data structures
        self.communities = {}
        self.node_to_com = [i for i in range(0, size)]
        self.total_coms = 0
        self.performed_community_action = "START\n"
        self.quality_threshold = quality_threshold
        self.exp_node_degs = []

        # initialize the graph
        self.graph = nx.empty_graph(self.size)

        self.base = os.getcwd()

        # initialize output files
        self.output_dir = str(self.base)+str(os.sep)+"results"+str(os.sep)+ str(self.size)+str(self.iterations)+ str(self.avg_deg)+ str(self.sigma)+ str(self.renewal)+str(self.quality_threshold)+str(self.max_evts)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.out_interactions = open(str(self.output_dir)+str(os.sep)+"interactions.txt", "w")
        self.out_events = open(str(self.output_dir)+str(os.sep)+"events.txt", "w")
        self.stable = 0

        self.it = 0
        self.count = 0

    
    def __add_node(self):
        #node emerges
        nid = self.size
        self.graph.add_node(nid)
        cid = rd.sample(list(self.communities.keys()), 1)[0]
        self.communities[cid].append(nid)
        self.node_to_com.append(cid)
        deg = rd.sample(range(2, int((len(self.communities[cid])-1) +
                                  (len(self.communities[cid])-1)*(1-self.sigma))), 1)[0]
        if deg == 0:
            deg = 1
        self.exp_node_degs.append(deg)
        self.size += 1
        
    def __remove_node(self):
        #node vanishes
        com_sel = [c for c, v in future.utils.iteritems(self.communities) if len(v) > 3]
        if len(com_sel) > 0:
            cid = rd.sample(com_sel, 1)[0]
            s = self.graph.subgraph(self.communities[cid])
            sd = dict(s.degree)
            min_value = min(sd.values())
            candidates = [k for k in sd if sd[k] == min_value]
            nid = rd.sample(candidates, 1)[0]
            eds = list(self.graph.edges([nid]))
            for e in eds:
                self.count += 1
                self.out_interactions.write("%s\t%s\t-\t%s\t%s\n" % (self.it, self.count, e[0], e[1]))
                self.graph.remove_edge(e[0], e[1])

            self.exp_node_degs[nid] = 0
            self.node_to_com[nid] = -1
            nodes = set(self.communities[cid])
            self.communities[cid] = list(nodes - {nid})
            self.graph.remove_node(nid)  


    def __get_nodes(self):
        #all vertices of the graph
        if len(self.communities_involved) == 0:
            return self.graph.nodes()
        else:
            nodes = {}
            for cid in self.communities_involved:
                for nid in self.communities[cid]:
                    nodes[nid] = None
            return list(nodes.keys())        
    def __get_vanished_edges(self,node):
        #deleted edges of node 'node'
        edges=[]
        neighbors=nx.all_neighbors(self.graph,node)
        if len(self.communities)>= nx.number_connected_components(self.graph):
            for neighbor in neighbors:
                delay=self.graph.get_edge_data(node,neighbor)['d']
                if delay==self.it:
                    edges.append(neighbor)
        return edges

    def execute(self, simplified=True):
        #start the algo
        # generate degree sequence (allot degrees to nodes)
        self.__get_degree_seq()
        # generate community size distrib (allot sizes to communities)
        allot_com_size=self.__distrib_community_size()
        # make the initial node assignments according to community sizes
        self.__allot_initial_nodes()

        #iterations start here
        for self.it in range(0,self.iterations):
            #community checks if cool generate event
            disjoint_parts=nx.number_connected_components(self.graph)
            if disjoint_parts<=len(self.communities):
                #check test
                if self.__check_test():
                    self.__generate_event(simplified)
            
            #node vanishing if probability
            ar=rd.random()
            if ar<self.del_node:
                self.__remove_node()
            
            #node creation if probability
            ar=rd.random()
            if ar<self.new_node:
                self.__add_node()
            
            #all nodes in communities
            nodes=self.__get_nodes()

            #for all nodes
            for node in nodes:
                #if deleted remove it
                if self.node_to_com[node]==-1:
                    continue
                #get vanished edges
                vanished=self.__get_vanished_edges(node)
                #removal phase
            



    
if __name__ == '__main__':
    argset = argparse.ArgumentParser()
    argset.add_argument('size', type=int, help='Number of nodes', default=1000)
    argset.add_argument('iterations', type=int, help='Number of iterations', default=1000)
    argset.add_argument('simplified', type=bool, help='Simplified execution', default=True)
    argset.add_argument('-d', '--avg_degree', type=int, help='Average node degree', default=15)
    argset.add_argument('-s', '--sigma', type=float, help='Sigma', default=0.7)
    argset.add_argument('-l', '--lbd', type=float, help='Lambda community size distribution', default=1)
    argset.add_argument('-a', '--alpha', type=int, help='Alpha degree distribution', default=2.5)
    argset.add_argument('-p', '--prob_action', type=float, help='Probability of node action', default=1)
    argset.add_argument('-r', '--prob_renewal', type=float, help='Probability of edge renewal', default=0.8)
    argset.add_argument('-q', '--quality_threshold', type=float, help='Conductance quality threshold', default=0.3)
    argset.add_argument('-n', '--new_nodes', type=float, help='Probability of node appearance', default=0)
    argset.add_argument('-j', '--delete_nodes', type=float, help='Probability of node vanishing', default=0)
    argset.add_argument('-e', '--max_events', type=int, help='Max number of community events for stable iteration', default=1)

    arguments = argset.parse_args()
    rdyn = RDyn(size=arguments.size, iterations=arguments.iterations, avg_deg=arguments.avg_degree,
                sigma=arguments.sigma, lambdad=arguments.lbd, alpha=arguments.alpha, paction=arguments.prob_action,
                prenewal=arguments.prob_renewal, quality_threshold=arguments.quality_threshold,
                new_node=arguments.new_nodes, del_node=arguments.delete_nodes, max_evts=arguments.max_events)
    rdyn.execute(simplified=arguments.simplified)
