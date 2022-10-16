#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

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
            pathEdges.append((prevEdge.src.loc, prevEdge.dest.loc, str(round(prevEdge.length))))
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

    
########## Heap Implementation of Priority Queue ##########

    def djikstraHeap(self, srcIndex):
        pqHeap = []
        nodeDict = {}

        self.makeQueueHeap(pqHeap, nodeDict)
        pqHeap[srcIndex].distance = 0.0

        while len(nodeDict) > 0:
            u = self.deleteMinHeap(pqHeap, nodeDict)
            for edge in u.neighbors:
                if edge.dest.distance > u.distance + edge.length:
                    edge.dest.distance = u.distance + edge.length
                    edge.dest.prev = edge
                    self.decreaseKeyHeap(pqHeap, edge.dest, nodeDict)
                    
    
    def makeQueueHeap(self, pqHeap, nodeDict):
        for i in range(len(self.network.nodes)):
            pqHeap.append(self.network.nodes[i])
            nodeDict[self.network.nodes[i]] = i
            pqHeap[i].distance = float('inf')
            pqHeap[i].prev = None
            nodeDict[pqHeap[i]] = i
            self.bubbleUpHeap(pqHeap, i, nodeDict)



    def deleteMinHeap(self, pqHeap, nodeDict):
        data = pqHeap[0]
        pqHeap[0] = pqHeap[len(pqHeap) - 1]
        nodeDict[pqHeap[0]] = 0
        pqHeap.pop(-1)
        nodeDict.pop(data)
        self.heapifyDown(pqHeap, 0, nodeDict)
        return data


    def bubbleUpHeap(self, pqHeap, index, nodeDict):
        if(index == 0 or index == None):
            return

        print("BUBBLE UP index: ", index)
        print("BUBBLE UP parent index: ", self.getParentIndex(index))
        print("length of pqHeap: ", len(pqHeap))
        if self.hasParent(index):
             if pqHeap[self.getParentIndex(index)].distance > pqHeap[index].distance:
                self.swap(pqHeap, self.getParentIndex(index), index, nodeDict)
                self.bubbleUpHeap(pqHeap, self.getParentIndex(index), nodeDict)


    def decreaseKeyHeap(self, pqHeap, node, nodeDict):
        self.bubbleUpHeap(pqHeap, nodeDict.get(node), nodeDict)
        return


    def heapifyDown(self, pqHeap, index, nodeDict):
        smallest = index
        if self.hasLeftChild(index, pqHeap) and pqHeap[smallest].distance > pqHeap[self.getLeftChildIndex(index)].distance:
            smallest = self.getLeftChildIndex(index)
        if self.hasRightChild(index, pqHeap) and pqHeap[smallest].distance > pqHeap[self.getRightChildIndex(index)].distance:
            smallest = self.getRightChildIndex(index)

        if(smallest != index):
            self.swap(pqHeap, index, smallest, nodeDict)
            self.heapifyDown(pqHeap, smallest, nodeDict)


    def swap(self, pqHeap, index1, index2, nodeDict):
        temp = pqHeap[index1]
        pqHeap[index1] = pqHeap[index2]
        pqHeap[index2] = temp

        # Update nodeDict
        temp = nodeDict[pqHeap[index1]]
        nodeDict[pqHeap[index1]] = nodeDict[pqHeap[index2]]
        nodeDict[pqHeap[index2]] = temp


    def getParentIndex(self, index):
        return (index - 1) // 2
    
    def getLeftChildIndex(self, index):
        return index * 2 + 1

    def getRightChildIndex(self, index):
        return index * 2 + 2
    
    def hasParent(self, index):
        if(index == 0 or index == None):
            return False
        return self.getParentIndex(index) >= 0

    def hasLeftChild(self, index, pqHeap):
        if(index < 0 or index == None):
            return False
        return self.getLeftChildIndex(index) < len(pqHeap)

    def hasRightChild(self, index, pqHeap):
        if(index < 0 or index == None):
            return False
        return self.getRightChildIndex(index) < len(pqHeap)