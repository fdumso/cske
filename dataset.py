# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON, XML
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
    """%(entity_id, entity_id)
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)['results']['bindings']
    return [result['category']['value'] for result in results]


def get_types(entity_id):
    """
    Get types of an entity from DB-pedia and YAGO.
    :param entity_id: universal identifier of the entity
    :return: <list> of entity, each is a type of the target entity
    """
    dbpedia_sql = """
PREFIX dbo: <http://dbpedia.org/ontology>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?type
WHERE {
   {<%s> dbo:type ?type .}
   UNION
   {<%s> rdf:type ?type .}
}
ORDER BY ?type
    """% (entity_id, entity_id)
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)['results']['bindings']
    return [result['type']['value'] for result in results]

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
    """% (entity_id)
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)['results']['bindings']
    return [(result['p']['value'], result['o']['value']) for result in results]

def get_csks(entity_id):
    """
    Get common sense knowledge from ConceptNet.
    :param entity_id: universal identifier of the entity
    :return: <list> of (property, value)
    """
    # TODO
    pass

def get_all_so(property_id):
    dbpedia_sql = """
SELECT ?s
WHERE{
    ?s <%s> ?o .
}
    """%(property_id)
    results = __execute_sparql(DBPEDIA_ENDPOINT, dbpedia_sql)['results']['bindings']
    return [ result['s']['value'] for result in results ]

def __execute_sparql(endpoint, sql):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sql)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

if __name__ == '__main__':
    print "---category---"
    for cate in get_categories('http://dbpedia.org/resource/Eiffel_Tower'):
        print cate
    print "---type---"
    for type in get_types('http://dbpedia.org/resource/Eiffel_Tower'):
        print type
    print "---pv pairs---"
    for pair in get_pv_pairs('http://dbpedia.org/resource/Eiffel_Tower'):
        print pair
    print "---'abstract'_is_multi_value---"
    pairs = get_all_so(u'http://dbpedia.org/ontology/abstract')
    print len(pairs) > len(set(pairs))
