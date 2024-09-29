import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
def cutGraph(G,minX,maxX,minY,maxY):
    nodesToKeep = [n for n, data in G.nodes(data=True) if (data['y'] > minY and data['y']<maxY and data['x']<maxX and data['x']>minX)]  # Example condition
    out = G.subgraph(nodesToKeep)
    return(out)
def kmToDeg(inp):
    return(inp*0.0089932)
def cutGraphAround(G,posX,posY,dist):
    d=kmToDeg(dist)
    return(cutGraph(G,posX-d,posX+d,posY-d,posY+d))
inputCoord = [-75.682316,45.421816]
distanceWanted = 3
G = ox.load_graphml(filepath='ottawaWithEnjoyabilityFixed.graphml')
print("Loaded")
G = cutGraph(G,inputCoord[0]-distanceWanted,inputCoord[0]+distanceWanted,inputCoord[1]-distanceWanted,inputCoord[1]+distanceWanted)
for u, v, data in G.edges(data=True):
            data['enjoyability'] = float(data['enjoyability'])
orig = ox.distance.nearest_nodes(G,inputCoord[0],inputCoord[1])  
dest = ox.distance.nearest_nodes(G,-75.679709,45.419708)  # CBY

shortest_path = nx.shortest_path(G, orig, dest, weight='enjoyability')
print("Shortest path found")

fig, ax = ox.plot_graph_route(G, shortest_path, route_linewidth=6, node_size=0, bgcolor='k', route_color='cyan')
plt.show()