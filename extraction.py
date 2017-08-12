# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    
"""
from collections import Counter

from . import dataset

import numpy
__author__ = "freemso"


class Extractor(object):
    """
    Common sense knowledge extractor
    """
    def __init__(self, alpha):
        self.alpha = alpha
        self.id2node = {}

    def get_node(self, uuid):
        """
        Get the node of id
        :param uuid: universal identifier of the node
        :return: <Node>
        """
        if uuid in self.id2node:
            return self.id2node[uuid]
        else:
            node = Node(uuid)
            self.id2node[uuid] = node
            return node

    def extract(self, target_uuid):
        target_node = self.get_node(target_uuid)
        parents = target_node.get_parents()
        siblings = target_node.get_siblings()
        target_attributes = target_node.get_attributes()
        num_parent = len(parents)
        num_sibling = len(siblings)
        parents_attributes_counter = self.count_nodes_attributes(parents)
        siblings_attributes_counter = self.count_nodes_attributes(siblings)

        # Inference from sibling
        for attribute in siblings_attributes_counter:
            if siblings_attributes_counter[attribute] < num_sibling ** self.alpha:
                pass
                # TODO



    @staticmethod
    def count_nodes_attributes(nodes):
        """
        Count the attributes of a list of nodes
        :param nodes: <list> of <Node>
        :return: <Counter> of attributes with their occurrences
        """
        attributes_counter = Counter()
        for node in nodes:
            attributes = node.get_attributes()
            for attribute in attributes:
                attributes_counter[attribute] += 1
        return attributes_counter


class Node(object):
    """
    Node of the knowledge graph.
    Entity, category, type and value in PV-pair are all nodes.
    """
    def __init__(self, uuid):
        """
        :param uuid: universal identifier
        """
        self.uuid = uuid # uri
        self.parents = None
        self.siblings = None
        self.attributes = None  # CSK from ConceptNet and PV-pairs from DB-pedia are all considered as attributes
        self.extracted_attributes = None  # Newly extracted attributes during this extraction process
        self.extracted_correct_attributes = None  # Attributes that are considered as correct after validation

    def __eq__(self, other):
        return hasattr(other, "uuid") and self.uuid == other.uuid

    def __hash__(self):
        return hash(self.uuid)

    def get_name(self):
        """
        Get a human readable name of the node
        :return: <str>
        """
        names = dataset.get_resource_name(self.uuid)
        return names[0] if len(names)>0 else self.uuid

    def get_parents(self):
        """
        Get parent nodes of the target node
        :return: <list> of <Node>
        """
        if not self.parents:
            all = [Node(id) for id in dataset.get_types(self.uuid)]
            self.parents = all[:]
            for p in all:
                subClassOf = dataset.get_parent_class(p.uuid)
                self.parents = [p for p in self.parents if p.uuid not in subClassOf]
        return self.parents

    def get_siblings(self):
        """
        Get sibling nodes of the target node
        :return: <list> of <Node>
        """
        if not self.siblings:
            self.siblings = []
            for p in self.parents:
                children = dataset.get_all_type_member(p.uuid)
                self.siblings.append([Node(c) for c in children])
        return self.siblings

    def get_attributes(self):
        """
        Get the valid attributes of the node
        :return: <list> of (property<Edge>, value<Node>)
        """
        if not self.attributes:
            # Get PV-pairs and CSK from database
            pv_pairs = dataset.get_pv_pairs(self.uuid)
            csks = dataset.get_csks(self.uuid)
            # Merge duplicated attributes
            self.attributes = list(set(pv_pairs + csks))

        if self.extracted_correct_attributes:
            return self.attributes + self.extracted_correct_attributes
        else:
            return self.attributes


class Edge(object):
    """
    Edge of the knowledge graph.
    Property in PV-pair and relation in CSK are both edges.
    """
    def __init__(self, uuid, name):
        """
        :param uuid: universal identifier
        :param name: human readable name
        """
        self.uuid = uuid
        self.name = name

    def __hash__(self):
        return hash(self.uuid)

    def is_multi_valued(self):
        """
        Check if the edge is multi-valued.
        Calculate all predicates of <SPO> in DB-pedia, those objectives values of
        predicates that occur more than once are treated as multi-value attributes.
        :return: <bool>
        """
        pairs = dataset.get_all_subjects(self.uuid)
        return len(pairs) > len(set(pairs))

def immediate_category_filter(category_nodes):
    """
    Filter out those categories who are at a higher level in the hierarchy.
    Hierarchy information is available in DB-pedia Ontology.
    :param category_nodes: <list> of <Node>
    :return: <list> of <Node>, with no hierarchy conflict(granularity)
    """
    origin = category_nodes[:]
    result = category_nodes[:]

    for id in origin:
        cur_cate = dataset.get_categories(id) # Does Category has parent category?
        result = list( set(result) - (set(result) & set(cur_cate)) )
    return result

if __name__ == '__main__':
    pass
