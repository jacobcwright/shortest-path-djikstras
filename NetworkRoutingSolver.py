#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

    pqHeap = []

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        pathEdges = []
        totalLength = 0
       
        destNode = self.network.nodes[self.dest]
        prevNode = destNode

        while prevNode.prev is not None:
            prevEdge = prevNode.prev
            pathEdges.append((prevEdge.src.loc, prevEdge.dest.loc, str(int(prevEdge.length))))
            totalLength += prevEdge.length
            prevNode = prevEdge.src

        return {'cost':totalLength, 'path':pathEdges}

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
        pqArray = self.makeQueueArray()
        for node in pqArray:
            node.distance = float('inf')
            node.prev = None
        pqArray[srcIndex].distance = 0.0
        
        while len(pqArray) > 0:
            u = self.deleteMinArray(pqArray)
            for edge in u.neighbors:
                if edge.dest.distance > u.distance + edge.length:
                    edge.dest.distance = u.distance + edge.length
                    edge.dest.prev = edge


    def makeQueueArray(self):
        return self.network.nodes.copy()

    def deleteMinArray(self, pqArray):
        minNode = None
        minIndex = None
        for i in range(len(pqArray)):
            if minNode is None or pqArray[i].distance < minNode.distance:
                minNode = pqArray[i]
                minIndex = i
        
        pqArray.pop(minIndex)
        return minNode

    