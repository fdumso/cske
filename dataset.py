# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import pprint
import re

from SPARQLWrapper import SPARQLWrapper, JSON

"""
    
"""

__author__ = "freemso"

DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"


def get_categories(entity_id):
    """
    Get all the categories of an entity from YAGO and DB-pedia.
    :param entity_id: universal identifier of the entity
    :return: <list> of entity, each is a category of the target entity
    """
    dbpedia_sql = """
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX dbo: <http://dbpedia.org/ontology>
        SELECT DISTINCT ?category
        WHERE {
            {<%s> dcterms:subject ?category .}
            UNION
            {<%s> dbo:category ?category .}
        }
        ORDER BY ?category
    """ % (entity_id, entity_id)
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)["results"]["bindings"]
    return [result["category"]["value"] for result in results]


def get_types(entity_id):
    """
    Get types of an entity from DB-pedia and YAGO.
    :param entity_id: universal identifier of the entity
    :return: <list> of entity, each is a type of the target entity
    """
    dbpedia_sql = """
        PREFIX dbo: <http://dbpedia.org/ontology>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dbr: <http://dbpedia.org/resource>
        SELECT DISTINCT ?type
        WHERE {
           {<%s> dbo:type ?type .}
           UNION
           {<%s> rdf:type ?type .}
           UNION
           {<%s> owl:type ?type .}
           UNION
           {<%s> dbr:type ?type .}
        }
        ORDER BY ?type
    """ % (entity_id,entity_id,entity_id,entity_id)
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)["results"]["bindings"]
    return [result["type"]["value"] for result in results]

def get_subjects(entity_id):
    dbpedia_sql = """
        PREFIX dct:<http://purl.org/dc/terms/>
        SELECT DISTINCT ?subject
        WHERE {
           <%s> dct:subject ?subject .
        }
        ORDER BY ?subject
    """ % entity_id
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)["results"]["bindings"]
    return [result["subject"]["value"] for result in results]

def get_pv_pairs(entity_id):
    """
    Get property-value pairs of the target entity from YAGO and DB-pedia.
    :param entity_id: universal identifier of the entity
    :return: <list> of (property, value)
    """
    dbpedia_sql = """
        SELECT DISTINCT ?p ?o
        WHERE {
            <%s> ?p ?o
        }
        ORDER BY ?p
    """ % entity_id
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)["results"]["bindings"]
    return [(result["p"]["value"], result["o"]["value"]) for result in results]


def get_csks(entity_id):
    """
    Get common sense knowledge from ConceptNet.
    :param entity_id: universal identifier of the entity
    :return: <list> of (property, value)
    """
    # TODO
    return []


def get_all_subjects(property_id):
    dbpedia_sql = """
        SELECT ?s
        WHERE{
            ?s <%s> ?o .
        }
    """ % property_id
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)["results"]["bindings"]
    return [result["s"]["value"] for result in results]


def get_all_type_member(type_id):
    dbpedia_sql = """
        PREFIX dbo: <http://dbpedia.org/ontology>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?subject
        WHERE {
           {?subject dbo:type <%s> .}
           UNION
           {?subject rdf:type <%s> .}
        }
        ORDER BY ?type
    """ % (type_id, type_id)
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)["results"]["bindings"]
    return [result["subject"]["value"] for result in results]


def get_resource_name(res_id):
    dbpedia_sql = """
        PREFIX dbo: <http://dbpedia.org/ontology>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?name
        WHERE {
            {<%s> foaf:name ?name . }
            UNION
            {<%s> rdfs:label ?name . }
        }
    """ % (res_id, res_id)
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)["results"]["bindings"]
    return [result["name"]["value"] for result in results]


def get_parent_class(class_id):
    dbpedia_sql = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?o
        FROM NAMED <http://dbpedia.org/resource/classes#>
        WHERE {
            GRAPH <http://dbpedia.org/resource/classes#>{
                <%s> rdfs:subClassOf ?o
            }
        }
    """ % class_id
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)["results"]["bindings"]
    return [result["o"]["value"] for result in results]


def filter_get_ontology(all_types):
    s=set()
    for x in all_types:
        pattern = re.compile('http://dbpedia.org/ontology/.+')
        match = pattern.match(x)
        if not match:
            s.add(x)
    return all_types-s

def __execute_sparql(endpoint, sql):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sql)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s")
    logging.root.setLevel(level=logging.INFO)

    all_subjects=get_subjects("http://dbpedia.org/resource/Tiger")
    print all_subjects

    superclass=get_parent_class("http://dbpedia.org/ontology/Town")[0]
    print superclass

    # print "---category---"
    # for cate in get_categories("http://dbpedia.org/resource/Eiffel_Tower"):
    #    print cate
    # print "---type---"
    # for type in get_types("http://dbpedia.org/resource/Eiffel_Tower"):
    #    print type
    # print "---pv pairs---"
    # for pair in get_pv_pairs("http://dbpedia.org/resource/Eiffel_Tower"):
    #    print pair
    # print "---"abstract"_is_multi_value---"
    # pairs = get_all_subjects(u"http://dbpedia.org/ontology/abstract")
    # print len(pairs) > len(set(pairs))
    # print("---Arch structure type member---")
    # for m in get_all_type_member("http://dbpedia.org/ontology/ArchitecturalStructure"):
    #     print(m)
