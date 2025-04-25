# compute the average element edge length for a mesh.
# Used to find h values for Richardson extrapolation equations

from abaqus import *
from abaqusConstants import *

# get assembly instance mesh
model = mdb.models['Convergence-Analysis-1000']
assembly = model.rootAssembly
instance = assembly.instances['convergence-1000']  
elements = instance.elements

# initialize counters
total_edge_length = 0.0
edge_count = 0

for elem in elements:
    coords = [node.coordinates for node in elem.getNodes()]
    num_nodes = len(coords)

    if num_nodes < 2:
        continue

    for i in range(num_nodes):
        p1 = coords[i]  # get coordinates of edge endpoints
        p2 = coords[(i+1) % num_nodes]
        edge_length = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5    # compute distance between points
        total_edge_length += edge_length
        edge_count += 1

# print result
if edge_count > 0:
    avg_length = total_edge_length / edge_count
    print("Average edge length:", avg_length)
else:
    print("No valid edges found.")
