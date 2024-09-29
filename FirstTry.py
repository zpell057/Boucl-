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
def sabotageFirstPath(G, pathOfNodesToSabotage):
    for i in range(len(pathOfNodesToSabotage)-1):
        G[pathOfNodesToSabotage[i]][pathOfNodesToSabotage[i+1]][0]['enjoyability'] = 0.0
    return(G)
G = ox.load_graphml(filepath='ottawaWithEnjoyabilityFixed.graphml')
for u, v, data in G.edges(data=True):
            data['enjoyability'] = float(data['enjoyability'])

def showLoop(G,inputCoord,distanceWanted):
    #inputCoord = [-75.682316,45.421816]
    #distanceWanted = 10
    directionAngle = 2*math.pi*random.random()
    tempDirection = [inputCoord[0]+kmToDeg(distanceWanted)*math.cos(directionAngle)/3.1,inputCoord[1]+kmToDeg(distanceWanted)*math.sin(directionAngle)/3.1]
    tempDirection2 = [tempDirection[0]+kmToDeg(distanceWanted)*math.cos(directionAngle+math.pi/2)/3.1,inputCoord[1]+kmToDeg(distanceWanted)*math.sin(directionAngle+math.pi/2)/3.1]
    coords = [inputCoord,tempDirection,tempDirection2]
    maxX=max(coords, key=lambda x: x[0])[0]
    maxY=max(coords, key=lambda x: x[1])[1]
    minX=min(coords, key=lambda x: x[0])[0]
    minY=min(coords, key=lambda x: x[1])[1]
    print("Loaded")
    G = cutGraphAround(G,inputCoord[0],inputCoord[1],distanceWanted*0.55)
    orig = ox.distance.nearest_nodes(G,inputCoord[0],inputCoord[1])  
    dest = ox.distance.nearest_nodes(G,tempDirection[0],tempDirection[1])  # CBY -75.679709,45.419708
    nodeOfTemp2 = ox.distance.nearest_nodes(G,tempDirection2[0],tempDirection2[1])

    pathToRandomDirectionPoint = nx.shortest_path(G, orig, dest, weight='enjoyability')
    print("First path found")
    pathToSecondDirection = nx.shortest_path(G, dest, nodeOfTemp2, weight='enjoyability')
    gettingBackToOrigin = nx.shortest_path(G, nodeOfTemp2, orig, weight='enjoyability')
    finalLoop = pathToRandomDirectionPoint +pathToSecondDirection[1:]+ gettingBackToOrigin[1:]

    F = cutGraph(G,minX-kmToDeg(0.5),maxX+kmToDeg(0.5),minY-kmToDeg(0.5),maxY+kmToDeg(0.5))

    fig, ax = ox.plot_graph_route(F, finalLoop, route_linewidth=6, node_size=0, bgcolor='k', route_color='cyan')
    plt.show()
def tryShowLoop(inputCoord,distanceWanted):
    
    try:
        out=showLoop(G,inputCoord,distanceWanted)
    except:
        tryShowLoop(inputCoord,distanceWanted)
