from shapely.geometry.polygon import Polygon
from shapely.geometry import Point


class processFiles():
    def __init__(self,fileName):
        self.fileName = fileName

    def pc(self):
        s,g,obs = self.readFile(self.fileName)
        polyObs = self.genPolys(obs)
        return [s,g,obs,polyObs]


    def readFile(self,fileName):
        #open file and read lines
        f = open(fileName,'r')
        lines = f.readlines()

        #extract start and goal
        start = [float(x) for x in lines.pop(0).split()]
        goal = [float(x) for x in lines.pop(0).split()]
        obs = []

        #extract obstacle one by one
        while lines:
            l = lines.pop(0).split(',')
            vs = []
            for p in l:
                vs.append([float(x) for x in p.split()])
            obs.append(vs)
        return start,goal,obs

    # generate obstacle in polygon format
    def genPolys(self,obs):
        polys = []
        for points in obs:
            vs = []
            for p in points:
                vs.append(tuple(p))
            ring_mixed = Polygon(vs)
            polys.append(ring_mixed)
        return polys
