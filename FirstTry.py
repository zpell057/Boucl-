import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
def cutGraph(G,minX,maxX,minY,maxY):
    nodesToKeep = [n for n, data in G.nodes(data=True) if (data['y'] > minY and data['y']<maxY and data['x']<maxX and data['x']>minX)]  
    out = G.subgraph(nodesToKeep)
    return(out)
def kmToDeg(inp):
    return(inp*0.0089932)
def cutGraphAround(G,posX,posY,dist):
    d=kmToDeg(dist)
    return(cutGraph(G,posX-d,posX+d,posY-d,posY+d))
inputCoord = [-75.682316,45.421816]
distanceWanted = 10
directionAngle = 2*math.pi*random.random()
tempDirection = [inputCoord[0]+kmToDeg(distanceWanted)*math.cos(directionAngle)/1.8,inputCoord[1]+kmToDeg(distanceWanted)*math.sin(directionAngle)/1.8]
G = ox.load_graphml(filepath='ottawaWithEnjoyabilityFixed.graphml')
print("Loaded")
G = cutGraphAround(G,inputCoord[0],inputCoord[1],distanceWanted*0.55)
for u, v, data in G.edges(data=True):
            data['enjoyability'] = float(data['enjoyability'])
orig = ox.distance.nearest_nodes(G,inputCoord[0],inputCoord[1])  
dest = ox.distance.nearest_nodes(G,tempDirection[0],tempDirection[1])  # CBY -75.679709,45.419708

shortest_path = nx.shortest_path(G, orig, dest, weight='enjoyability')
print("Shortest path found")

fig, ax = ox.plot_graph_route(G, shortest_path, route_linewidth=6, node_size=0, bgcolor='k', route_color='cyan')
plt.show()