#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

    pqArray = []
    pqHeap = []

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3

        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()

        if use_heap:
            self.djikstraHeap(srcIndex)
        else:
            self.djikstraArray(srcIndex)

        t2 = time.time()
        return (t2-t1)


########## Array Implementation of Priority Queue ##########

    def djikstraArray(self, srcIndex):
        self.makeQueueArray()
        self.decreaseKeyArray(srcIndex, 0)
        
        

    def makeQueueArray(self):
        for node in self.network.nodes:
            self.pqArray.append(node)
            self.pqArray[node.node_id].distance = float('inf')
        for node in self.pqArray:
            print(node)
            print(node.distance)


    def insertArray(self, node, distance):
        self.pqArray[node] = distance

    def deleteMinArray(self):
        minNode = None
        minDistance = float('inf')
        for node in self.pqArray:
            if self.pqArray[node] is not None and self.pqArray[node] < minDistance:
                minNode = node
                minDistance = self.pqArray[node]
        
        self.pqArray.pop(minNode)
        return minNode

    def decreaseKeyArray(self, nodeIndex, distance):
        self.pqArray[nodeIndex].distance = distance
        print(self.pqArray[nodeIndex])
        print(self.pqArray[nodeIndex].distance)

    