#!/usr/bin/env python
import os.path
import sys

import maven

def pom_visitor(poms, dirname, names):
    if 'pom.xml' in names:
        pom = '%s/pom.xml' % dirname
        poms.append(maven.parse(pom))

def dependency_edges(pom, group = None):
    if group is None:
        group_filter = lambda d: True
    else:
        group_filter = lambda d: d.groupId.startswith(group)
    edges = set()
    for dependency in filter(group_filter, pom['dependencies']):
        edges.add((pom['artifact'].artifactId, dependency.artifactId))
    return edges

def print_graph(edges):
    print 'digraph dependencies {'
    for edge in edges:
        a, b = edge
        print '  "%s" -> "%s";' % (a, b) 
    print '}'

if __name__ == '__main__':
    directory = sys.argv[1]
    group = sys.argv[2] 
    poms = []
    os.path.walk(directory, pom_visitor, poms)
    edges = set()
    for pom in poms:
        edges = edges | dependency_edges(pom, group)
    print_graph(edges)
