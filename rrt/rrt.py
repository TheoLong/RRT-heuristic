# Author: Theo Long
# credit to pythonRobotics. Some ideas are refrerence from https://github.com/AtsushiSakai/PythonRobotics
import matplotlib.pyplot as plt
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import random
import math
import copy
import time

# node class for rrt
class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

# rrt class
class RRT():
    def __init__(self, start, goal, obs, polyObs,
                 randArea, stepRadius=1, goalSampleRate=80, improved = True):
        """
        start:  Start Position [x,y]
        goal:   Goal Position [x,y]
        obs:    obstacles in list of vertexs [[x1,y1],[x2,y2], ...]
        polyObs:    obstacles in polygon [poly1, poly2, ...]
        randArea:   Ramdom Samping Area [min,max]
        stepRadius: distance between nodes e.g. 1
        goalSampleRate: probability of using goal as next point
        spaced_distance:  spaced distance between new node and old nodes

        """
        self.polyObs = polyObs
        self.start = Node(start[0], start[1])
        self.goal = Node(goal[0], goal[1])
        self.minrand = randArea[0]
        self.maxrand = randArea[1]
        self.stepRadius = stepRadius
        self.goalSampleRate = goalSampleRate
        self.obs = obs
        self.path = [[self.goal.x, self.goal.y]]
        self.timelaps = 0
        self.nodeList = [self.start]
        self.improved = improved

    # rrt iteration main loop
    def plan(self):
        # log time elapes
        start_time = time.time()
        self.hit_count = 0
        numOfExpansion = 10
        while 1:
            # sample random point. goal sample rate controls rates to set goal as exploration
            # if random.randint(0, 100) > 0:
            validPoints = []
            while len(validPoints) < numOfExpansion:
                randomPoint = self.nextRandomPoint()
                
                # get nearest node
                neighbor = self.nearestNode(randomPoint)

                # grow the tree
                nearestNode = self.nodeList[neighbor]
                theta = math.atan2(randomPoint[1] - nearestNode.y, randomPoint[0] - nearestNode.x)

                # connect nearest node with random point in the radius of expansion
                newNode = copy.deepcopy(nearestNode)
                newNode.x += self.stepRadius * math.cos(theta)
                newNode.y += self.stepRadius * math.sin(theta)
                newNode.parent = neighbor

                # if neighbor colide in polygon or not spaced out from old nodes, skip this node
                if not self.collide(newNode)or not self.spaced(newNode):
                    self.hit_count +=1
                    continue

                validPoints.append(newNode)
            if self.improved:
                bestNode = self.bestStep(validPoints)
            else:
                bestNode = validPoints[0]

            # update node count:
            self.nodeList.append(bestNode)
            print 'Num of nodes: ', str(len(self.nodeList))

            # check goal
            if self.goaled():
                self.timelaps = time.time() - start_time
                break

            # draw the graph
            self.DrawGraph((bestNode.x,bestNode.y))

        # generate path and highlight the path with red line
        self.generatePath()
        self.DrawGraph(path = self.path)
        plt.grid(True)

    # generate path from goal to start
    def generatePath(self):
        # connect goal to its parent all the way back to start
        lastIndex = len(self.nodeList) - 1
        while self.nodeList[lastIndex].parent is not None:
            node = self.nodeList[lastIndex]
            self.path.append([node.x, node.y])
            lastIndex = node.parent
        self.path.append([self.start.x, self.start.y])

    # update the graph
    def DrawGraph(self, rnd=None, path=None):
        # clear graphj
        plt.clf()
        if rnd is not None:
            plt.plot(rnd[0], rnd[1], "bo")

        # redraw the graph
        for node in self.nodeList:
            if node.parent is not None:
                plt.plot([node.x, self.nodeList[node.parent].x], [
                         node.y, self.nodeList[node.parent].y], "-k")

        # draw all obsticle
        for o in self.obs:
            x,y = zip(*o)
            plt.fill(x,y)

        # if path is generated, highlight it with red
        if path:
            plt.plot([x for x, y in path], [y for x, y in path], 'r-')

        plt.plot(self.start.x, self.start.y, "ro")
        plt.plot(self.goal.x, self.goal.y, "go")
        plt.axis([self.minrand, self.maxrand, self.minrand, self.maxrand])
        plt.grid(True)
        plt.pause(0.01)

    # get nearest node
    def nearestNode(self, randomPoint):
        distance = []
        # p = multiprocessing.Pool(processes = multiprocessing.cpu_count()-1)
        for node in self.nodeList:
            distance += [self.dist(node,Node(randomPoint[0],randomPoint[1]))]
        bestNeighbor = distance.index(min(distance))
        return bestNeighbor

    # check for collision
    def collide(self, node):
        for obs in self.polyObs:
            if obs.contains(Point(node.x,node.y)):
                return False #collision
        return True  # safe

    # check for spacing between new nodes and old nodes
    def spaced(self,node):
        for n in self.nodeList:
            if self.dist(n,node) < self.stepRadius-0.01:
                return False
        return True

    # check if latest node reached the goal
    def goaled(self):
        if self.dist(self.nodeList[-1],self.goal) <= self.stepRadius:
            print '====> Path found'
            return True
        return False

    # euclidian distance
    def dist(self,a,b):
        return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

    # path finding statistic
    def pathStat(self):
        numNode = len(self.nodeList)
        steps = len(self.path)
        pathCost = steps * self.stepRadius

        print '================================='
        print '======== RRT statistics ========='
        print '================================='
        print 'Nodes generated:', str(numNode)
        print 'Num of nodes in path:', str(steps)
        print 'Path length:', str(pathCost)
        print 'Time used:', str(self.timelaps),'s'

    def nextRandomPoint(self):
        if random.randint(0, 100) > 50 or not self.improved or self.hit_count >= 5:
            randomPoint = [random.uniform(self.minrand, self.maxrand),random.uniform(self.minrand, self.maxrand)]
            self.hit_count = 0
        else: 
            randomPoint = [self.goal.x, self.goal.y]
        return randomPoint

    def bestStep(self,nodes):
        distance = []
        for n in nodes:
            distance.append(self.dist(n,self.goal))
        bestI = distance.index(min(distance))
        return nodes[bestI]