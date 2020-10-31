import io
import os
import json
import numpy as np
import pandas as pd
import networkx as nx
from typing import List
from six.moves import urllib
from scipy.sparse import coo_matrix
import csv


class GraphReader(object):
    r"""Class to read benchmark datasets for the community detection or node embedding task.

    Args:
        dataset (str): Dataset of interest, one of: 
            (:obj:`"facebook"`, :obj:`"twitch"`, :obj:`"wikipedia"`, :obj:`"github"`, :obj:`"lastfm"`, :obj:`"deezer"`). Default is 'wikipedia'.
    """
    def __init__(self, dataset: str="wikipedia"):
        self.dataset = dataset
        self.path='/home/doge/Desktop/karateclub/dataset/node_level/'

    def _dataset_reader(self, end):
        """
        Reading the dataset from the web.
        """
        path=self.path+self.dataset+"/"+end
        data=pd.read_csv(path)
        return data
   
    def get_graph(self) -> nx.classes.graph.Graph:
        r"""Getting the graph.

        Return types:
            * **graph** *(NetworkX graph)* - Graph of interest.
        """
        data = self._dataset_reader("edges.csv")
        graph = nx.convert_matrix.from_pandas_edgelist(data, "id_1", "id_2")
        return graph

    def get_features(self) -> coo_matrix:
        r"""Getting the node features Scipy matrix.

        Return types:
            * **features** *(COO Scipy array)* - Node feature matrix.
        """
        data = self._dataset_reader("features.csv")
        row = np.array(data["node_id"])
        col = np.array(data["feature_id"])
        values = np.array(data["value"])
        node_count = max(row) + 1
        feature_count = max(col) + 1
        shape = (node_count, feature_count)
        features = coo_matrix((values, (row, col)), shape=shape)
        return features

    def get_target(self) -> np.array:
        r"""Getting the class membership of nodes.

        Return types:
            * **target** *(Numpy array)* - Class membership vector.
        """
        data = self._dataset_reader("target.csv")
        target = np.array(data["target"])
        return target

