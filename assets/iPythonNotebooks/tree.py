#!/usr/bin/env python

a = 5
class Foo:
    def __init__(self):
        self.x = a
class Bar:
    a = 6 # will be object attribute: .a
    b = ["u","v"]
    def __init__(self):
        self.x = a

class Edge:
    """Edge class, to contain a directed edge of a tree or directed graph.
    attributes parent and child: index of parent and child node in the graph.
    """

    def __init__ (self, parent, child, length=None):
        """create a new Edge object, linking nodes
        with indices parent and child."""
        print("starting __init__ for new Edge object/instance")
        self.parent = parent
        self.child = child
        self.length = length

    def __str__(self):
        res = "edge from " + str(self.parent) + " to " + str(self.child)
        if self.length:
            res += ", length=" + str(self.length)
        return res

class Tree:
    """ Tree, described by its list of edges."""
    def __init__(self, edgelist):
        """create a new Tree object from a list of existing Edges"""
        self.edge = edgelist
        self.update_node2edge() # creates attributes node2edge and root

    def __str__(self):
        res = "parent -> child:"
        for e in self.edge:
            res += "\n" + str(e.parent) + " " + str(e.child)
        return res

    def add_edge(self, ed):
        """add an edge to the tree"""
        self.edge.append(ed)
        self.update_node2edge()

    def new_edge(self, parent, child):
        """add to the tree a new edge from parent to child (node indices)"""
        self.add_edge( Edge(parent,child) )

    def update_node2edge(self):
        """dictionary child node index -> edge for fast access to edges.
        also add/update root attribute."""
        self.node2edge = {e.child : e for e in self.edge}
        childrenset = set(self.node2edge.keys())
        rootset = set(e.parent for e in self.edge).difference(childrenset)
        if len(rootset) > 1:
            warn("there should be a single root: " + str(rootset))
        if len(rootset) == 0:
            raise Exception("there should be at least one root!")
        self.root = rootset.pop()

    def get_dist2root(self, i):
        """distance of node index i to the root"""
        # check if e is root: if so: distance 0
        if i==self.root:
            return 0
        else:
            e = self.node2edge[i]
            return 1 + self.get_dist2root(e.parent)

    def get_path2root(self, i):
        """list of nodes from the root to i (in this order)"""
        if i==self.root:
            return [i]
        else:
            e = self.node2edge[i]
            res = self.get_path2root(e.parent)
            res.append(i)
            return res

    def get_MRCA(self, i, j):
        """return most recent common ancestor between nodes i and j"""
        pathi = self.get_path2root(i)
        pathj = self.get_path2root(j)
        while pathi and pathj:
            if pathi[0]==pathj[0]:
                res = pathi.pop(0)
                pathj.pop(0)
            else:
                break
        return res

    def get_nodedist(self, i, j):
        """tree distance between node i and node j"""
        pathi = self.get_path2root(i)
        pathj = self.get_path2root(j)
        while pathi and pathj:
            if pathi[0]==pathj[0]:
                pathi.pop(0)
                pathj.pop(0)
            else:
                break
        return len(pathi)+len(pathj)
